import { useState, useEffect } from 'react';
import { X, Flame, AlertCircle, AlertTriangle, Info, CheckCircle2 } from 'lucide-react';
import { Button } from './ui/button';
import { cn } from '@/lib/utils';
import { NotificationType } from '@/contexts/NotificationContext';

export interface BannerConfig {
  id: string;
  type: NotificationType;
  message: string;
  dismissible?: boolean;
  persistent?: boolean;
  action?: {
    label: string;
    onClick: () => void;
  };
}

interface BannerNotificationProps {
  banners: BannerConfig[];
  onDismiss: (id: string) => void;
}

export default function BannerNotification({ banners, onDismiss }: BannerNotificationProps) {
  const [visibleBanners, setVisibleBanners] = useState<string[]>([]);

  useEffect(() => {
    // Load dismissed banners from localStorage
    const dismissed = localStorage.getItem('phoenix_dismissed_banners');
    const dismissedIds = dismissed ? JSON.parse(dismissed) : [];
    
    // Show only non-dismissed banners
    setVisibleBanners(
      banners
        .filter(b => b.persistent || !dismissedIds.includes(b.id))
        .map(b => b.id)
    );
  }, [banners]);

  const handleDismiss = (id: string, persistent?: boolean) => {
    setVisibleBanners(prev => prev.filter(bid => bid !== id));
    onDismiss(id);

    if (!persistent) {
      // Save to localStorage
      const dismissed = localStorage.getItem('phoenix_dismissed_banners');
      const dismissedIds = dismissed ? JSON.parse(dismissed) : [];
      localStorage.setItem(
        'phoenix_dismissed_banners',
        JSON.stringify([...dismissedIds, id])
      );
    }
  };

  const getIcon = (type: NotificationType) => {
    switch (type) {
      case 'success':
        return <CheckCircle2 className="w-5 h-5" />;
      case 'error':
        return <AlertCircle className="w-5 h-5" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5" />;
      case 'info':
        return <Info className="w-5 h-5" />;
      case 'phoenix':
        return <Flame className="w-5 h-5" />;
    }
  };

  const getStyles = (type: NotificationType) => {
    switch (type) {
      case 'success':
        return 'bg-green-500/10 text-green-500 border-green-500/20';
      case 'error':
        return 'bg-red-500/10 text-red-500 border-red-500/20';
      case 'warning':
        return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
      case 'info':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'phoenix':
        return 'bg-primary/10 text-primary border-primary/20';
    }
  };

  const activeBanners = banners.filter(b => visibleBanners.includes(b.id));

  if (activeBanners.length === 0) return null;

  return (
    <div className="fixed top-0 left-0 right-0 z-50">
      {activeBanners.map((banner) => (
        <div
          key={banner.id}
          className={cn(
            "border-b px-4 py-3 flex items-center justify-between gap-4 animate-in slide-in-from-top",
            getStyles(banner.type)
          )}
        >
          <div className="flex items-center gap-3 flex-1">
            {getIcon(banner.type)}
            <p className="text-sm font-medium">{banner.message}</p>
          </div>

          <div className="flex items-center gap-2">
            {banner.action && (
              <Button
                variant="ghost"
                size="sm"
                onClick={banner.action.onClick}
                className="h-8"
              >
                {banner.action.label}
              </Button>
            )}
            {banner.dismissible !== false && (
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={() => handleDismiss(banner.id, banner.persistent)}
              >
                <X className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

// Hook for managing banners
export function useBanners() {
  const [banners, setBanners] = useState<BannerConfig[]>([]);

  const addBanner = (banner: Omit<BannerConfig, 'id'>) => {
    const newBanner: BannerConfig = {
      ...banner,
      id: `banner_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    };
    setBanners(prev => [...prev, newBanner]);
    return newBanner.id;
  };

  const removeBanner = (id: string) => {
    setBanners(prev => prev.filter(b => b.id !== id));
  };

  const clearAll = () => {
    setBanners([]);
  };

  return {
    banners,
    addBanner,
    removeBanner,
    clearAll,
  };
}
