import React from 'react';
import { ReadinessStatus } from '../types';
import { CheckCircle2, AlertTriangle, XCircle, HelpCircle } from 'lucide-react';

interface Props {
  status: ReadinessStatus;
  score?: number;
  confidence?: number;
  showIcon?: boolean;
}

export const ReadinessBadge: React.FC<Props> = ({ status, score, confidence, showIcon = true }) => {
  let badgeStyle = '';
  let Icon = CheckCircle2;
  let label = status.replace('_', ' ');

  switch (status) {
    case 'READY':
      badgeStyle = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      Icon = CheckCircle2;
      break;
    case 'AT_RISK':
      badgeStyle = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      Icon = AlertTriangle;
      break;
    case 'NOT_READY':
      badgeStyle = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      Icon = XCircle;
      break;
    case 'DATA_INCOMPLETE':
      badgeStyle = 'bg-slate-500/10 text-slate-400 border-slate-500/30';
      Icon = HelpCircle;
      break;
  }

  return (
    <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md border text-xs font-semibold tracking-wide uppercase ${badgeStyle}`}>
      {showIcon && <Icon className="w-3.5 h-3.5" />}
      <span>{label}</span>
      {score !== undefined && (
        <span className="ml-1 pl-1.5 border-l border-current/30 text-[11px] font-mono">
          {score}%
        </span>
      )}
      {confidence !== undefined && (
        <span className="text-[10px] opacity-75 font-mono">
          ({confidence}% conf)
        </span>
      )}
    </div>
  );
};
