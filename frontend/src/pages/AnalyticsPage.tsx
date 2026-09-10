import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, Legend } from 'recharts';
import { BarChart3, Clock, AlertTriangle, ShieldCheck, Database, Layers } from 'lucide-react';

export const AnalyticsPage: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAnalytics()
      .then(res => setData(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-400 font-mono animate-pulse">Computing real-time analytics...</div>;
  }

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-100 tracking-tight">ORRS Analytics & Performance Intelligence</h2>
        <p className="text-xs text-slate-400">Data-driven performance evaluation and operational delay breakdown</p>
      </div>

      {/* KPI Cards Banner */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-4 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 font-semibold uppercase">Baseline Avg Idle</div>
          <div className="text-2xl font-bold text-slate-200 font-mono mt-1">{data?.summary?.baseline_avg_idle} mins</div>
          <div className="text-[11px] text-slate-500 mt-0.5">T-0m Manual Check</div>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 font-semibold uppercase">Prototype Avg Idle</div>
          <div className="text-2xl font-bold text-emerald-400 font-mono mt-1">{data?.summary?.prototype_avg_idle} mins</div>
          <div className="text-[11px] text-emerald-500 mt-0.5">-{data?.summary?.reduction_pct}% Idle Reduction</div>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 font-semibold uppercase">Early Detection Rate</div>
          <div className="text-2xl font-bold text-cyan-400 font-mono mt-1">{data?.summary?.early_detection_rate}%</div>
          <div className="text-[11px] text-cyan-500 mt-0.5">Target: &ge;70%</div>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 font-semibold uppercase">Alert Precision</div>
          <div className="text-2xl font-bold text-blue-400 font-mono mt-1">{data?.summary?.alert_precision}%</div>
          <div className="text-[11px] text-blue-500 mt-0.5">High Severity Signal</div>
        </div>
      </div>

      {/* Grid of 6 Recharts Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Theatre Idle Time Baseline vs Prototype */}
        <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-blue-400" />
            <h3 className="text-sm font-semibold text-slate-200 uppercase">1. Avoidable Idle Minutes: Baseline vs Prototype</h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.theatre_performance || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="theatre" stroke="#94A3B8" fontSize={11} />
                <YAxis stroke="#94A3B8" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#F8FAFC' }} />
                <Legend />
                <Bar dataKey="baseline_idle_mins" name="Baseline (Manual)" fill="#EF4444" radius={[4, 4, 0, 0]} />
                <Bar dataKey="prototype_idle_mins" name="Prototype (ORRS)" fill="#10B981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Delay Reasons Pie */}
        <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <h3 className="text-sm font-semibold text-slate-200 uppercase">2. Delay Category Breakdown</h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data?.delay_breakdown || []} dataKey="count" nameKey="category" cx="50%" cy="50%" outerRadius={80} label>
                  {(data?.delay_breakdown || []).map((_: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#F8FAFC' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 3: Department On-Time Rate */}
        <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-semibold text-slate-200 uppercase">3. Department Performance & On-Time Rate</h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.department_performance || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="department" stroke="#94A3B8" fontSize={9} />
                <YAxis stroke="#94A3B8" fontSize={11} domain={[0, 100]} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#F8FAFC' }} />
                <Bar dataKey="on_time_rate" name="On-Time Start %" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 4: Readiness Checkpoint Timeline */}
        <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-semibold text-slate-200 uppercase">4. Readiness Score Progression Across Checkpoints</h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data?.readiness_timeline || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="checkpoint" stroke="#94A3B8" fontSize={11} />
                <YAxis stroke="#94A3B8" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#F8FAFC' }} />
                <Legend />
                <Line type="monotone" dataKey="ready" name="Ready %" stroke="#10B981" strokeWidth={3} />
                <Line type="monotone" dataKey="at_risk" name="At Risk %" stroke="#F59E0B" strokeWidth={2} />
                <Line type="monotone" dataKey="not_ready" name="Not Ready %" stroke="#EF4444" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 5: Data Quality & Missing Field Frequencies */}
        <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4 lg:col-span-2">
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-purple-400" />
            <h3 className="text-sm font-semibold text-slate-200 uppercase">5. Data Quality & Stale Information Frequency</h3>
          </div>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.missing_data_frequency || []} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis type="number" stroke="#94A3B8" fontSize={11} />
                <YAxis dataKey="type" type="category" stroke="#94A3B8" fontSize={10} width={180} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#F8FAFC' }} />
                <Bar dataKey="count" name="Frequency" fill="#8B5CF6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
