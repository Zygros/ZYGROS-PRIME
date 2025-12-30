import { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { Button } from './ui/button';
import { cn } from '@/lib/utils';

interface MobileNavProps {
  onNavigate: (id: string) => void;
}

export default function MobileNav({ onNavigate }: MobileNavProps) {
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { id: 'executive', label: 'Executive Summary' },
    { id: 'frameworks', label: 'Core Frameworks' },
    { id: 'pathways', label: 'AGI Pathways' },
    { id: 'absolute-agi', label: 'Absolute AGI' },
    { id: 'system-architecture', label: 'System Architecture' },
    { id: 'api-capabilities', label: 'API Capabilities' },
    { id: 'roadmap', label: 'Roadmap' },
  ];

  const handleNavigate = (id: string) => {
    onNavigate(id);
    setIsOpen(false);
  };

  return (
    <div className="md:hidden">
      {/* Hamburger Button */}
      <Button
        variant="ghost"
        size="icon"
        onClick={() => setIsOpen(!isOpen)}
        className="relative z-50"
        aria-label="Toggle menu"
      >
        {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </Button>

      {/* Mobile Menu Overlay */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
            onClick={() => setIsOpen(false)}
          />

          {/* Menu Panel */}
          <div className="fixed top-[80px] right-0 bottom-0 w-[280px] bg-background/95 backdrop-blur-md border-l border-border z-40 animate-in slide-in-from-right">
            <nav className="flex flex-col p-6 gap-2">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => handleNavigate(item.id)}
                  className={cn(
                    "text-left px-4 py-3 rounded-lg text-base font-medium",
                    "hover:bg-primary/10 hover:text-primary",
                    "transition-colors duration-200",
                    "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background"
                  )}
                >
                  {item.label}
                </button>
              ))}
            </nav>
          </div>
        </>
      )}
    </div>
  );
}
