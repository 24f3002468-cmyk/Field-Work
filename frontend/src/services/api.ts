import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Offline sync queue helper
const QUEUE_KEY = 'ml_dashboard_offline_queue';

export function getOfflineQueue(): any[] {
  try {
    const data = localStorage.getItem(QUEUE_KEY);
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

export function addToOfflineQueue(item: any) {
  const queue = getOfflineQueue();
  queue.push(item);
  localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
}

export function clearOfflineQueue() {
  localStorage.removeItem(QUEUE_KEY);
}

export async function flushOfflineQueue() {
  const queue = getOfflineQueue();
  if (queue.length === 0) return;

  for (const item of queue) {
    try {
      if (item.type === 'TASK_COMPLETE') {
        await api.post(`/tasks/${item.taskId}/complete`, item.payload);
      } else if (item.type === 'DAILY_LOG') {
        await api.post('/daily-logs', item.payload);
      }
    } catch (e) {
      console.error('Error syncing offline item', item, e);
    }
  }
  clearOfflineQueue();
}
