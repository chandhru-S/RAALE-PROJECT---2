import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { AlertItem } from '../types';
import { ShieldAlert, AlertTriangle, Bell, CheckCircle2, Clock } from 'lucide-react';

interface Props {
  onSelectSurgery: (surgeryId: string) => void;
  onRefreshAlerts?: () => void;
}

export const AlertsPage: React.FC<Props> = ({ onSelectSurgery, onRefreshAlerts }) => {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [filter, setFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);

  const fetchAlerts = () => {
    setLoading(true);
    api.getAlerts(filter)
      .then(res => setAlerts(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAlerts();
  }, [filter]);

  const handleAcknowledge = async (alertId: string) => {
    try {
      await api.acknowledgeAlert(alertId);
      fetchAlerts();
      if (onRefreshAlerts) onRefreshAlerts();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">Synchroniser Alert Command Feed</h2>
          <p className="text-xs text-slate-400">Actionable operational warnings and risk mitigations</p>
        </div>

        <div className="flex items-center gap-2 bg-slate-900 p-1 rounded-lg border border-slate-800 text-xs font-mono">
          {['ALL', 'ACTIVE', 'ACKNOWLEDGED'].map(st => (
            <button
              key={st}
              onClick={() => setFilter(st)}
              className={`px-3 py-1 rounded-md transition ${filter === st ? 'bg-blue-600 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 font-mono animate-pulse">Loading live alert feed...</div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {alerts.length === 0 ? (
            <div className="glass-panel p-8 rounded-xl text-center text-slate-400 font-mono">
              No alerts matching filter criteria.
            </div>
          ) : (
            alerts.map(a => {
              const isHigh = a.severity === 'HIGH';
              const isAck = a.status === 'ACKNOWLEDGED';

              return (
                <div
                  key={a.alert_id}
                  className={`glass-panel p-5 rounded-xl border transition flex flex-col md:flex-row md:items-center justify-between gap-4 ${
                    isAck ? 'opacity-60 border-slate-800' : isHigh ? 'border-rose-500/40 bg-rose-500/5' : 'border-amber-500/40 bg-amber-500/5'
                  }`}
                >
                  <div className="space-y-2 max-w-3xl">
                    <div className="flex items-center gap-3 flex-wrap">
                      <span className={`px-2.5 py-0.5 rounded text-[11px] font-bold font-mono uppercase ${
                        isHigh ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40' : 'bg-amber-500/20 text-amber-400 border border-amber-500/40'
                      }`}>
                        {a.severity} PRIORITY
                      </span>
                      <span className="text-sm font-bold text-slate-100 font-mono">{a.theatre_id}</span>
                      <button onClick={() => onSelectSurgery(a.surgery_id)} className="text-xs text-blue-400 font-mono hover:underline">
                        Surgery: {a.surgery_id}
                      </button>
                      <span className="text-xs text-slate-400 font-mono flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" />
                        {new Date(a.created_at).toLocaleTimeString()}
                      </span>
                    </div>

                    <div className="text-sm font-semibold text-slate-200">{a.issue}</div>
                    <div className="text-xs text-slate-300 font-mono bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                      💡 <span className="text-blue-300">Recommended Action:</span> {a.recommended_action}
                    </div>
                  </div>

                  <div className="flex flex-col items-end gap-2">
                    <div className="text-xs text-cyan-400 font-mono">Confidence: {a.confidence_score}%</div>
                    {isAck ? (
                      <span className="flex items-center gap-1 text-xs font-semibold text-emerald-400 font-mono bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/30">
                        <CheckCircle2 className="w-4 h-4" /> Acknowledged
                      </span>
                    ) : (
                      <button
                        onClick={() => handleAcknowledge(a.alert_id)}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg shadow-md transition"
                      >
                        Acknowledge Alert
                      </button>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      )}
    </div>
  );
};
