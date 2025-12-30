import { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';
import { toast } from 'sonner';

export type NotificationType = 'success' | 'error' | 'warning' | 'info' | 'phoenix';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  timestamp: number;
  read: boolean;
  persistent?: boolean;
}

interface NotificationContextType {
  notifications: Notification[];
  unreadCount: number;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  clearNotification: (id: string) => void;
  clearAll: () => void;
  showToast: (type: NotificationType, title: string, message?: string) => void;
  requestPushPermission: () => Promise<boolean>;
  pushPermissionGranted: boolean;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [pushPermissionGranted, setPushPermissionGranted] = useState(false);

  // Load notifications from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('phoenix_notifications');
    if (stored) {
      try {
        setNotifications(JSON.parse(stored));
      } catch (e) {
        console.error('Failed to parse stored notifications', e);
      }
    }

    // Check push permission status
    if ('Notification' in window) {
      setPushPermissionGranted(Notification.permission === 'granted');
    }
  }, []);

  // Save notifications to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('phoenix_notifications', JSON.stringify(notifications));
  }, [notifications]);

  const unreadCount = notifications.filter(n => !n.read).length;

  const addNotification = useCallback((notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    const newNotification: Notification = {
      ...notification,
      id: `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      read: false,
    };

    setNotifications(prev => [newNotification, ...prev].slice(0, 100)); // Keep last 100

    // Show browser push notification if permission granted
    if (pushPermissionGranted && 'Notification' in window) {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        tag: newNotification.id,
      });
    }

    // Play notification sound
    playNotificationSound(notification.type);
  }, [pushPermissionGranted]);

  const markAsRead = useCallback((id: string) => {
    setNotifications(prev =>
      prev.map(n => n.id === id ? { ...n, read: true } : n)
    );
  }, []);

  const markAllAsRead = useCallback(() => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  }, []);

  const clearNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);

  const showToast = useCallback((type: NotificationType, title: string, message?: string) => {
    const content = message ? `${title}: ${message}` : title;
    
    switch (type) {
      case 'success':
        toast.success(content);
        break;
      case 'error':
        toast.error(content);
        break;
      case 'warning':
        toast.warning(content);
        break;
      case 'info':
        toast.info(content);
        break;
      case 'phoenix':
        toast(content, {
          icon: '🔥',
          className: 'phoenix-toast',
        });
        break;
    }

    // Also add to notification center
    addNotification({ type, title, message: message || '' });
  }, [addNotification]);

  const requestPushPermission = useCallback(async (): Promise<boolean> => {
    if (!('Notification' in window)) {
      console.warn('This browser does not support notifications');
      return false;
    }

    if (Notification.permission === 'granted') {
      setPushPermissionGranted(true);
      return true;
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission();
      const granted = permission === 'granted';
      setPushPermissionGranted(granted);
      return granted;
    }

    return false;
  }, []);

  const playNotificationSound = (type: NotificationType) => {
    // Create a simple beep sound using Web Audio API
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      // Different frequencies for different notification types
      const frequencies: Record<NotificationType, number> = {
        success: 800,
        error: 400,
        warning: 600,
        info: 700,
        phoenix: 900,
      };

      oscillator.frequency.value = frequencies[type];
      oscillator.type = 'sine';

      gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);

      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
      // Silently fail if audio context is not available
    }
  };

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        unreadCount,
        addNotification,
        markAsRead,
        markAllAsRead,
        clearNotification,
        clearAll,
        showToast,
        requestPushPermission,
        pushPermissionGranted,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotifications() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be used within NotificationProvider');
  }
  return context;
}
