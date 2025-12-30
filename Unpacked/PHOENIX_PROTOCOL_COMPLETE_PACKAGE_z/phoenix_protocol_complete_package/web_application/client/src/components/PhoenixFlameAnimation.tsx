/**
 * Phoenix Flame Animation Component
 * Synchronized flame effects for collaboration mode
 */

import React, { useEffect, useRef, useState } from 'react';
import { flameSynchronizer } from '@/lib/collaboration';

interface PhoenixFlameAnimationProps {
  intensity?: number;
  color?: string;
  size?: 'small' | 'medium' | 'large';
  synchronized?: boolean;
}

export default function PhoenixFlameAnimation({
  intensity = 0.5,
  color = '#ff6b35',
  size = 'medium',
  synchronized = false
}: PhoenixFlameAnimationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number | undefined>(undefined);
  const [flameState, setFlameState] = useState(() => ({ intensity, color }));

  // Subscribe to flame synchronization if enabled
  useEffect(() => {
    if (synchronized) {
      const handleSync = (state: any) => {
        setFlameState(state);
      };
      flameSynchronizer.onSync(handleSync);
    }
  }, [synchronized]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // Flame particle system
    interface Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      life: number;
      maxLife: number;
      size: number;
      color: string;
    }

    const particles: Particle[] = [];
    const maxParticles = size === 'small' ? 20 : size === 'medium' ? 40 : 60;

    const createParticle = () => {
      const currentIntensity = synchronized ? flameState.intensity : intensity;
      const currentColor = synchronized ? flameState.color : color;
      
      return {
        x: width / 2 + (Math.random() - 0.5) * 20,
        y: height,
        vx: (Math.random() - 0.5) * 2,
        vy: -2 - Math.random() * 2 * currentIntensity,
        life: 1,
        maxLife: 0.5 + Math.random() * 0.5,
        size: 2 + Math.random() * 4 * currentIntensity,
        color: currentColor
      };
    };

    const updateParticles = () => {
      // Add new particles
      while (particles.length < maxParticles) {
        particles.push(createParticle());
      }

      // Update existing particles
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        
        p.x += p.vx;
        p.y += p.vy;
        p.vy -= 0.05; // Gravity (upward)
        p.life -= 0.02;
        
        // Remove dead particles
        if (p.life <= 0) {
          particles.splice(i, 1);
        }
      }
    };

    const drawParticles = () => {
      ctx.clearRect(0, 0, width, height);
      
      particles.forEach(p => {
        const alpha = p.life;
        
        // Draw glow
        ctx.save();
        ctx.globalAlpha = alpha * 0.3;
        ctx.fillStyle = p.color;
        ctx.filter = 'blur(8px)';
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
        
        // Draw core
        ctx.save();
        ctx.globalAlpha = alpha;
        const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size);
        gradient.addColorStop(0, '#ffffff');
        gradient.addColorStop(0.3, p.color);
        gradient.addColorStop(1, 'transparent');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      });
    };

    const animate = () => {
      updateParticles();
      drawParticles();
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [intensity, color, size, synchronized, flameState]);

  const sizeMap = {
    small: { width: 60, height: 80 },
    medium: { width: 100, height: 120 },
    large: { width: 150, height: 180 }
  };

  const dimensions = sizeMap[size];

  return (
    <canvas
      ref={canvasRef}
      width={dimensions.width}
      height={dimensions.height}
      className="pointer-events-none"
      style={{ width: dimensions.width, height: dimensions.height }}
    />
  );
}

/**
 * Phoenix Ember Effect Component
 * Floating ember particles for ambient effects
 */

interface PhoenixEmberEffectProps {
  count?: number;
  color?: string;
}

export function PhoenixEmberEffect({ count = 10, color = '#ff6b35' }: PhoenixEmberEffectProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const embers: HTMLDivElement[] = [];

    for (let i = 0; i < count; i++) {
      const ember = document.createElement('div');
      ember.className = 'phoenix-ember';
      ember.style.cssText = `
        position: absolute;
        width: ${2 + Math.random() * 4}px;
        height: ${2 + Math.random() * 4}px;
        background: ${color};
        border-radius: 50%;
        pointer-events: none;
        opacity: ${0.3 + Math.random() * 0.4};
        box-shadow: 0 0 ${4 + Math.random() * 8}px ${color};
        animation: float-ember ${10 + Math.random() * 10}s linear infinite;
        animation-delay: ${Math.random() * 5}s;
        left: ${Math.random() * 100}%;
        bottom: -10px;
      `;
      container.appendChild(ember);
      embers.push(ember);
    }

    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
      @keyframes float-ember {
        0% {
          transform: translateY(0) translateX(0);
          opacity: 0;
        }
        10% {
          opacity: 0.7;
        }
        90% {
          opacity: 0.7;
        }
        100% {
          transform: translateY(-100vh) translateX(${-50 + Math.random() * 100}px);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);

    return () => {
      embers.forEach(ember => ember.remove());
      style.remove();
    };
  }, [count, color]);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ overflow: 'hidden' }}
    />
  );
}

/**
 * Phoenix Wing Transition Component
 * Animated wing effect for transitions
 */

interface PhoenixWingTransitionProps {
  isActive: boolean;
  onComplete?: () => void;
}

export function PhoenixWingTransition({ isActive, onComplete }: PhoenixWingTransitionProps) {
  useEffect(() => {
    if (isActive && onComplete) {
      const timer = setTimeout(onComplete, 1000);
      return () => clearTimeout(timer);
    }
  }, [isActive, onComplete]);

  if (!isActive) return null;

  return (
    <div className="fixed inset-0 z-50 pointer-events-none">
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="phoenix-wing-left" />
        <div className="phoenix-wing-right" />
      </div>
      <style>{`
        .phoenix-wing-left,
        .phoenix-wing-right {
          position: absolute;
          width: 50vw;
          height: 100vh;
          background: linear-gradient(90deg, 
            oklch(0.65 0.15 30) 0%,
            oklch(0.7 0.15 40) 50%,
            transparent 100%
          );
          animation: wing-sweep 1s ease-in-out;
        }
        
        .phoenix-wing-left {
          left: 0;
          transform-origin: left center;
        }
        
        .phoenix-wing-right {
          right: 0;
          transform-origin: right center;
          transform: scaleX(-1);
        }
        
        @keyframes wing-sweep {
          0% {
            transform: scaleX(0);
            opacity: 0;
          }
          50% {
            transform: scaleX(1);
            opacity: 1;
          }
          100% {
            transform: scaleX(0);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}
