import { create } from 'zustand';
import { TodayData, BacklogSummary, ProjectStatus, DSASummary, PlacementPointsSummary } from '../types';
import { api, addToOfflineQueue, flushOfflineQueue } from '../services/api';

interface DashboardState {
  today: TodayData | null;
  backlog: BacklogSummary | null;
  projectStatus: ProjectStatus | null;
  dsaSummary: DSASummary | null;
  pointsSummary: PlacementPointsSummary | null;
  isOffline: boolean;
  saveStatus: 'Saved' | 'Saving...' | 'Offline' | 'Sync pending';
  loading: boolean;
  error: string | null;

  fetchToday: () => Promise<void>;
  fetchBacklog: () => Promise<void>;
  fetchProjectStatus: () => Promise<void>;
  fetchDSASummary: () => Promise<void>;
  fetchPointsSummary: () => Promise<void>;
  completeTask: (taskId: string, actualMinutes: number, status: string, notes?: string) => Promise<void>;
}

export const useDashboardStore = create<DashboardState>((set, get) => ({
  today: null,
  backlog: null,
  projectStatus: null,
  dsaSummary: null,
  pointsSummary: null,
  isOffline: !navigator.onLine,
  saveStatus: 'Saved',
  loading: false,
  error: null,

  fetchToday: async () => {
    try {
      set({ loading: true });
      const res = await api.get('/planner/today');
      set({ today: res.data, loading: false, isOffline: false, saveStatus: 'Saved' });
    } catch (e: any) {
      set({ isOffline: true, saveStatus: 'Offline', loading: false, error: 'Failed to load today data' });
    }
  },

  fetchBacklog: async () => {
    try {
      const res = await api.get('/tasks/backlog');
      set({ backlog: res.data });
    } catch (e) {
      console.error('Backlog fetch failed');
    }
  },

  fetchProjectStatus: async () => {
    try {
      const res = await api.get('/project/status');
      set({ projectStatus: res.data });
    } catch (e) {
      console.error('Project status fetch failed');
    }
  },

  fetchDSASummary: async () => {
    try {
      const res = await api.get('/dsa/summary');
      set({ dsaSummary: res.data });
    } catch (e) {
      console.error('DSA summary fetch failed');
    }
  },

  fetchPointsSummary: async () => {
    try {
      const res = await api.get('/placement-points/summary');
      set({ pointsSummary: res.data });
    } catch (e) {
      console.error('Placement points summary fetch failed');
    }
  },

  completeTask: async (taskId: string, actualMinutes: number, status: string, notes?: string) => {
    const todayData = get().today;
    const date = todayData ? todayData.today_date : new Date().toISOString().split('T')[0];

    const payload = {
      task_id: taskId,
      date,
      actual_minutes: actualMinutes,
      status,
      completion_percentage: status === 'COMPLETED' ? 100.0 : (status === 'PARTIALLY_COMPLETED' ? 50.0 : 0.0),
      notes
    };

    set({ saveStatus: 'Saving...' });

    // Optimistically update local state
    if (todayData) {
      const updatedTasks = todayData.tasks.map(t => {
        if (t.id === taskId) {
          return {
            ...t,
            actual_minutes: actualMinutes,
            status: status as any,
            completion_percentage: payload.completion_percentage,
            notes
          };
        }
        return t;
      });
      set({ today: { ...todayData, tasks: updatedTasks } });
    }

    try {
      await api.post(`/tasks/${taskId}/complete`, payload);
      set({ saveStatus: 'Saved', isOffline: false });
      get().fetchToday();
    } catch (e) {
      // Queue offline change
      addToOfflineQueue({ type: 'TASK_COMPLETE', taskId, payload });
      set({ saveStatus: 'Sync pending', isOffline: true });
    }
  }
}));

// Listen for network reconnect
window.addEventListener('online', async () => {
  useDashboardStore.setState({ isOffline: false, saveStatus: 'Saving...' });
  await flushOfflineQueue();
  useDashboardStore.getState().fetchToday();
});

window.addEventListener('offline', () => {
  useDashboardStore.setState({ isOffline: true, saveStatus: 'Offline' });
});
