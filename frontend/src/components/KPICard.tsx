import React from 'react';
import { LucideIcon } from 'lucide-react';

interface Props {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  color?: string;
  trend?: string;
}

export const KPICard: React.FC<Props> = ({ title, value, subtitle, icon: Icon, color = 'text-blue-400' }) => {
  return (
    <div className="glass-panel p-5 rounded-xl border border-slate-700/50 hover:border-slate-600 transition-all shadow-lg">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        <div className={`p-2 rounded-lg bg-slate-800/80 ${color}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div className="flex items-baseline justify-between">
        <div className="text-2xl font-bold text-slate-100 font-mono tracking-tight">{value}</div>
      </div>
      {subtitle && <div className="mt-1 text-xs text-slate-400">{subtitle}</div>}
    </div>
  );
};
