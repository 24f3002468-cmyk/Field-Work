#!/usr/bin/env python3
import sys
import os
import subprocess
import json

def run_step(step_name, command, cwd="."):
    print(f"\n[RUNNING] {step_name}...")
    try:
        res = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[PASS] {step_name}")
            return True
        else:
            print(f"[FAIL] {step_name}")
            if res.stdout:
                print("STDOUT:", res.stdout.strip())
            if res.stderr:
                print("STDERR:", res.stderr.strip())
            return False
    except Exception as e:
        print(f"[ERROR] {step_name}: {e}")
        return False

def main():
    print("========================================")
    print("200-DAY DASHBOARD VERIFICATION SUITE")
    print("========================================")

    py_exe = sys.executable
    results = {}

    # 1. Planner Data Integrity
    results["Planner Data"] = run_step(
        "Planner Seed & Integrity Check",
        f'"{py_exe}" planner/seed_planner.py'
    )

    # 2. Pytest Suite (Database, API, Planner rules)
    results["Backend & API Tests"] = run_step(
        "Backend Pytest Test Suite",
        f'"{py_exe}" -m pytest backend/tests'
    )

    # 3. Direct API Data Integrity Verification Subprocess
    audit_code = (
        "import sys, os; "
        "sys.path.insert(0, 'backend'); "
        "from app.core.database import SessionLocal; "
        "from app.services.verification import run_data_integrity_check; "
        "db = SessionLocal(); "
        "report = run_data_integrity_check(db); "
        "db.close(); "
        "print('[PASS] Direct DB Data Integrity Audit: 200 days verified clean.' if report['status'] == 'PASS' else f'[FAIL] {report[\"issues\"]}'); "
        "sys.exit(0 if report['status'] == 'PASS' else 1)"
    )
    
    results["Database Integrity"] = run_step(
        "Direct DB Data Integrity Audit",
        f'"{py_exe}" -c "{audit_code}"'
    )

    # Print Summary Report
    print("\n========================================")
    print("VERIFICATION RESULTS SUMMARY")
    print("========================================")
    
    all_pass = True
    for name, ok in results.items():
        status_str = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"{name:<25}: {status_str}")

    print("----------------------------------------")
    if all_pass:
        print("RESULT: SYSTEM VERIFIED (ALL TESTS PASSED)")
        print("========================================")
        sys.exit(0)
    else:
        print("RESULT: VERIFICATION FAILED")
        print("========================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
