import React, { useState } from 'react';
import { api } from '../services/api';
import { SimulationResult } from '../types';
import { ReadinessBadge } from '../components/ReadinessBadge';
import { FlaskConical, Users, Wrench, UserX, PackageX, Clock, Siren, RefreshCw, Terminal, CheckCircle2 } from 'lucide-react';

interface Props {
  onRefreshAlerts?: () => void;
}

export const FailureSimulatorPage: React.FC<Props> = ({ onRefreshAlerts }) => {
  const [loading, setLoading] = useState(false);
  const [activeTest, setActiveTest] = useState<string | null>(null);
  const [log, setLog] = useState<SimulationResult | null>(null);
  const [resetMessage, setResetMessage] = useState<string | null>(null);

  const runSim = async (name: string, fn: () => Promise<SimulationResult>) => {
    setLoading(true);
    setActiveTest(name);
    setResetMessage(null);
    try {
      const res = await fn();
      setLog(res);
      if (onRefreshAlerts) onRefreshAlerts();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    setLoading(true);
    try {
      const res = await api.simulate.reset();
      setResetMessage(res.message);
      setLog(null);
      if (onRefreshAlerts) onRefreshAlerts();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const buttons = [
    {
      id: 'staff',
      title: '1. Simulate Missing Staff',
      subtitle: 'Anaesthetist status set to NULL',
      icon: Users,
      color: 'from-amber-600 to-orange-600',
      action: () => api.simulate.staffMissing('OT001')
    },
    {
      id: 'equipment',
      title: '2. Simulate Equipment Failure',
      subtitle: 'Surgical tower changes READY -> FAULTY',
      icon: Wrench,
      color: 'from-rose-600 to-red-600',
      action: () => api.simulate.equipmentFailure('OT002')
    },
    {
      id: 'patient',
      title: '3. Simulate Patient Not Ready',
      subtitle: 'Consent form incomplete / unconfirmed',
      icon: UserX,
      color: 'from-pink-600 to-rose-600',
      action: () => api.simulate.patientNotReady('OT003')
    },
    {
      id: 'supply',
      title: '4. Simulate Supply Missing',
      subtitle: 'Sterile surgical tray missing from CSSD',
      icon: PackageX,
      color: 'from-purple-600 to-indigo-600',
      action: () => api.simulate.supplyMissing('OT004')
    },
    {
      id: 'overrun',
      title: '5. Simulate Surgery Overrun',
      subtitle: 'Prior theatre session exceeds scheduled time',
      icon: Clock,
      color: 'from-blue-600 to-cyan-600',
      action: () => api.simulate.overrun('OT005')
    },
    {
      id: 'emergency',
      title: '6. Simulate Emergency Preemption',
      subtitle: 'Trauma emergency preempts OT-06',
      icon: Siren,
      color: 'from-red-600 to-rose-700',
      action: () => api.simulate.emergency('OT006')
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">Interactive Failure Scenario Simulator</h2>
          <p className="text-xs text-slate-400">Stress-test system readiness rules, safety overrides, and alert generation live</p>
        </div>
        <button
          onClick={handleReset}
          disabled={loading}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold border border-slate-700 flex items-center gap-2 transition"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          <span>Reset Environment</span>
        </button>
      </div>

      {/* Simulator Control Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {buttons.map((btn) => {
          const Icon = btn.icon;
          return (
            <button
              key={btn.id}
              onClick={() => runSim(btn.title, btn.action)}
              disabled={loading}
              className={`p-5 rounded-xl text-left bg-gradient-to-br ${btn.color} hover:brightness-110 shadow-lg shadow-black/40 transition-all border border-white/10 flex flex-col justify-between space-y-4 text-white group`}
            >
              <div className="flex items-center justify-between">
                <Icon className="w-6 h-6 group-hover:scale-110 transition-transform" />
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider bg-black/30 px-2 py-0.5 rounded">Trigger Scenario</span>
              </div>
              <div>
                <div className="font-bold text-sm">{btn.title}</div>
                <div className="text-xs opacity-80 font-mono mt-1">{btn.subtitle}</div>
              </div>
            </button>
          );
        })}
      </div>

      {resetMessage && (
        <div className="bg-emerald-500/10 border border-emerald-500/30 p-4 rounded-xl text-emerald-400 text-xs font-mono flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{resetMessage}</span>
        </div>
      )}

      {/* Output Console / Log Panel */}
      {log && (
        <div className="glass-panel p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider font-mono">{log.test_name} Execution Log</h3>
            </div>
            <ReadinessBadge status={log.overall_status} score={log.readiness_score} confidence={log.confidence_score} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
            <div className="bg-slate-900/80 p-4 rounded-lg border border-slate-800 space-y-2">
              <div className="text-slate-400 font-semibold uppercase text-[10px]">Target Parameters</div>
              <div>Surgery ID: <span className="text-blue-400 font-bold">{log.surgery_id}</span></div>
              <div>Theatre ID: <span className="text-slate-200 font-bold">{log.theatre_id}</span></div>
              <div>Readiness Score: <span className="text-emerald-400 font-bold">{log.readiness_score}%</span></div>
              <div>Confidence Score: <span className="text-cyan-400 font-bold">{log.confidence_score}%</span></div>
            </div>

            <div className="bg-slate-900/80 p-4 rounded-lg border border-slate-800 space-y-2">
              <div className="text-slate-400 font-semibold uppercase text-[10px]">Alert & Recommendation Engine</div>
              <div>Generated Alert: <span className="text-rose-400 font-bold">{log.alert_created || 'None'}</span></div>
              <div>Recommended Action: <span className="text-blue-300">{log.recommended_actions}</span></div>
            </div>
          </div>

          <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-[11px] font-mono text-slate-300">
            <div className="text-slate-500 uppercase text-[10px] mb-1 font-bold">Detected Operational Blocking Issues</div>
            <div className="text-amber-300">{log.blocking_issues}</div>
          </div>
        </div>
      )}
    </div>
  );
};
