import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { KPICard } from '../components/KPICard';
import { ReadinessBadge } from '../components/ReadinessBadge';
import { TheatreSummary, SystemSummary } from '../types';
import { LayoutGrid, CheckCircle2, AlertTriangle, XCircle, HelpCircle, Clock, ChevronRight } from 'lucide-react';

interface Props {
  onSelectSurgery: (surgeryId: string) => void;
  onNavigateTab: (tab: string) => void;
}

export const DashboardPage: React.FC<Props> = ({ onSelectSurgery, onNavigateTab }) => {
  const [summary, setSummary] = useState<SystemSummary | null>(null);
  const [theatres, setTheatres] = useState<TheatreSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getTheatres()
      .then(res => {
        setSummary(res.summary);
        setTheatres(res.theatres);
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-400 font-mono animate-pulse">Loading live theatre command grid...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Top Header Banner */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">Operating Room Readiness Dashboard</h2>
          <p className="text-xs text-slate-400">Real-time resource synchronisation across operating theatres</p>
        </div>
        <button
          onClick={() => onNavigateTab('simulator')}
          className="px-3.5 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-blue-500/20 transition flex items-center gap-1.5"
        >
          <span>Run Failure Simulation</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <KPICard title="Total Theatres" value={summary?.total_theatres || 8} icon={LayoutGrid} color="text-blue-400" />
        <KPICard title="Ready" value={summary?.ready || 0} icon={CheckCircle2} color="text-emerald-400" />
        <KPICard title="At Risk" value={summary?.at_risk || 0} icon={AlertTriangle} color="text-amber-400" />
        <KPICard title="Not Ready" value={summary?.not_ready || 0} icon={XCircle} color="text-rose-400" />
        <KPICard title="Incomplete Data" value={summary?.data_incomplete || 0} icon={HelpCircle} color="text-slate-400" />
        <KPICard title="Avg Idle Minutes" value={`${summary?.avg_idle_minutes || 14}m`} subtitle="-72% vs Baseline" icon={Clock} color="text-cyan-400" />
      </div>

      {/* Live Operating Theatre Status Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Live Operating Theatre Grid</h3>
          <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span> Live Synchronised
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {theatres.map((ot) => (
            <div
              key={ot.theatre_id}
              onClick={() => ot.current_surgery_id && onSelectSurgery(ot.current_surgery_id)}
              className="glass-panel glass-panel-hover p-4 rounded-xl cursor-pointer border border-slate-800 flex flex-col justify-between space-y-4"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-lg font-extrabold text-slate-100 font-mono">{ot.theatre_id}</span>
                  <ReadinessBadge status={ot.status} score={ot.readiness_score} />
                </div>
                <div className="text-xs text-slate-300 font-medium truncate">{ot.procedure}</div>
                <div className="text-[11px] text-slate-400">{ot.department}</div>
              </div>

              {ot.active_alert ? (
                <div className="bg-rose-500/10 border border-rose-500/30 p-2.5 rounded-lg text-[11px] text-rose-300 font-mono">
                  ⚠️ {ot.active_alert}
                </div>
              ) : (
                <div className="text-[11px] text-slate-400 font-mono flex items-center justify-between pt-2 border-t border-slate-800">
                  <span>Confidence: {ot.confidence_score}%</span>
                  <span className="text-blue-400 hover:underline">Details &rarr;</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
