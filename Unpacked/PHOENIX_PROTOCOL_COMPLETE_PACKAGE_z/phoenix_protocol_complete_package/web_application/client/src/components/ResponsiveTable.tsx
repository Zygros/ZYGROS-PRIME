import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface ResponsiveTableProps {
  children: ReactNode;
  className?: string;
}

export default function ResponsiveTable({ children, className }: ResponsiveTableProps) {
  return (
    <div className="relative">
      {/* Scroll indicator for mobile */}
      <div className="md:hidden absolute right-0 top-0 bottom-0 w-8 bg-gradient-to-l from-background to-transparent pointer-events-none z-10" />
      
      {/* Scrollable container */}
      <div className={cn(
        "overflow-x-auto -mx-4 px-4 md:mx-0 md:px-0",
        "scrollbar-thin scrollbar-thumb-primary/20 scrollbar-track-transparent",
        className
      )}>
        {children}
      </div>
      
      {/* Mobile hint */}
      <p className="md:hidden text-xs text-muted-foreground mt-2 text-center">
        ← Scroll horizontally to view all columns →
      </p>
    </div>
  );
}
