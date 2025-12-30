import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { NotificationProvider, useNotifications } from '../NotificationContext';
import { ReactNode } from 'react';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value; },
    clear: () => { store = {}; },
    removeItem: (key: string) => { delete store[key]; },
  };
})();

global.localStorage = localStorageMock as any;

// Mock Notification API
global.Notification = {
  permission: 'default',
  requestPermission: vi.fn().mockResolvedValue('granted'),
} as any;

// Mock AudioContext
global.AudioContext = vi.fn().mockImplementation(() => ({
  createOscillator: vi.fn().mockReturnValue({
    connect: vi.fn(),
    start: vi.fn(),
    stop: vi.fn(),
    frequency: { value: 0 },
    type: 'sine',
  }),
  createGain: vi.fn().mockReturnValue({
    connect: vi.fn(),
    gain: {
      setValueAtTime: vi.fn(),
      exponentialRampToValueAtTime: vi.fn(),
    },
  }),
  destination: {},
  currentTime: 0,
})) as any;

describe('NotificationContext', () => {
  const wrapper = ({ children }: { children: ReactNode }) => (
    <NotificationProvider>{children}</NotificationProvider>
  );

  beforeEach(() => {
    localStorage.clear();
  });

  it('should initialize with empty notifications', () => {
    const { result } = renderHook(() => useNotifications(), { wrapper });
    
    expect(result.current.notifications).toEqual([]);
    expect(result.current.unreadCount).toBe(0);
  });

  it('should add a notification', () => {
    const { result } = renderHook(() => useNotifications(), { wrapper });
    
    act(() => {
      result.current.addNotification({
        type: 'success',
        title: 'Test Notification',
        message: 'This is a test',
      });
    });

    expect(result.current.notifications).toHaveLength(1);
    expect(result.current.notifications[0].title).toBe('Test Notification');
    expect(result.current.notifications[0].type).toBe('success');
    expect(result.current.unreadCount).toBe(1);
  });

  it('should mark notification as read', () => {
    const { result } = renderHook(() => useNotifications(), { wrapper });
    
    act(() => {
      result.current.addNotification({
        type: 'info',
        title: 'Test',
        message: 'Test message',
      });
    });

    const notificationId = result.current.notifications[0].id;

    act(() => {
      result.current.markAsRead(notificationId);
    });

    expect(result.current.notifications[0].read).toBe(true);
    expect(result.current.unreadCount).toBe(0);
  });

  it('should clear a notification', () => {
    const { result } = renderHook(() => useNotifications(), { wrapper });
    
    act(() => {
      result.current.addNotification({
        type: 'warning',
        title: 'Warning',
        message: 'Test warning',
      });
    });

    const notificationId = result.current.notifications[0].id;

    act(() => {
      result.current.clearNotification(notificationId);
    });

    expect(result.current.notifications).toHaveLength(0);
  });

  it('should mark all notifications as read', () => {
    const { result } = renderHook(() => useNotifications(), { wrapper });
    
    act(() => {
      result.current.addNotification({
        type: 'info',
        title: 'Test 1',
        message: 'Message 1',
      });
      result.current.addNotification({
        type: 'success',
        title: 'Test 2',
        message: 'Message 2',
      });
    });

    expect(result.current.unreadCount).toBe(2);

    act(() => {
      result.current.markAllAsRead();
    });

    expect(result.current.unreadCount).toBe(0);
    expect(result.current.notifications.every((n: any) => n.read)).toBe(true);
  });

  it('should clear all notifications', () => {
    const { result } = renderHook(() => useNotifications(), { wrapper });
    
    act(() => {
      result.current.addNotification({
        type: 'error',
        title: 'Error 1',
        message: 'Message 1',
      });
      result.current.addNotification({
        type: 'phoenix',
        title: 'Phoenix',
        message: 'Phoenix message',
      });
    });

    expect(result.current.notifications).toHaveLength(2);

    act(() => {
      result.current.clearAll();
    });

    expect(result.current.notifications).toHaveLength(0);
  });

  it('should persist notifications to localStorage', () => {
    const { result } = renderHook(() => useNotifications(), { wrapper });
    
    act(() => {
      result.current.addNotification({
        type: 'success',
        title: 'Persistent Test',
        message: 'Should be saved',
      });
    });

    const stored = localStorage.getItem('phoenix_notifications');
    expect(stored).toBeTruthy();
    
    const parsed = JSON.parse(stored!);
    expect(parsed).toHaveLength(1);
    expect(parsed[0].title).toBe('Persistent Test');
  });

  it('should handle different notification types', () => {
    const { result } = renderHook(() => useNotifications(), { wrapper });
    
    const types: Array<'success' | 'error' | 'warning' | 'info' | 'phoenix'> = [
      'success',
      'error',
      'warning',
      'info',
      'phoenix',
    ];

    act(() => {
      types.forEach((type, index) => {
        result.current.addNotification({
          type,
          title: `${type} notification`,
          message: `Test ${index}`,
        });
      });
    });

    expect(result.current.notifications).toHaveLength(5);
    // Notifications are added in reverse order (newest first)
    types.forEach((type, index) => {
      expect(result.current.notifications[types.length - 1 - index].type).toBe(type);
    });
  });
});
