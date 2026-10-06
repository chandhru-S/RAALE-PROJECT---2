import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { ReadinessBadge } from './ReadinessBadge';
import { X, UserCheck, Users, Wrench, PackageCheck, AlertCircle, ShieldAlert, CheckCircle2, Clock } from 'lucide-react';

interface Props {
  surgeryId: string | null;
  onClose: () => void;
}

export const SurgeryDetailModal: React.FC<Props> = ({ surgeryId, onClose }) => {
  const [detail, setDetail] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!surgeryId) return;
    setLoading(true);
    api.getSurgeryDetail(surgeryId)
      .then(res => setDetail(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [surgeryId]);

  if (!surgeryId) return null;

  const assessment = detail?.latest_assessment;
  const sched = detail?.schedule;
  const patient = detail?.patient_readiness;
  const supplies = detail?.sterile_supply;
  const staff = detail?.staff_members || [];
  const equipment = detail?.equipment || [];

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-[#1C2541] border border-slate-700 w-full max-w-3xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-700/80 flex items-center justify-between bg-slate-900/60">
          <div>
            <div className="flex items-center gap-3">
              <h2 className="text-xl font-bold text-slate-100 font-mono">{surgeryId}</h2>
              {assessment && <ReadinessBadge status={assessment.overall_status} score={assessment.readiness_score} confidence={assessment.confidence_score} />}
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              {sched?.department} • {sched?.procedure_type} • Theatre {sched?.theatre_id}
            </p>
          </div>
          <button onClick={onClose} className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        {loading ? (
          <div className="p-12 text-center text-slate-400 animate-pulse font-mono">Loading surgical assessment data...</div>
        ) : (
          <div className="p-6 space-y-6 overflow-y-auto">
            {/* Top Score Cards */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700">
                <div className="text-xs text-slate-400 uppercase font-semibold mb-1">Overall Readiness Score</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-blue-400 font-mono">{assessment?.readiness_score || 0}%</span>
                  <span className="text-xs text-slate-400">Target: 100%</span>
                </div>
              </div>
              <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700">
                <div className="text-xs text-slate-400 uppercase font-semibold mb-1">Data Confidence Score</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-cyan-400 font-mono">{assessment?.confidence_score || 0}%</span>
                  <span className="text-xs text-slate-400">Quality: High</span>
                </div>
              </div>
            </div>

            {/* Readiness Domains breakdown */}
            <div className="space-y-3">
              <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Readiness Checkpoints Breakdown</h3>
              <div className="grid grid-cols-2 gap-3">
                {/* Patient */}
                <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2 text-xs font-semibold text-slate-200">
                      <UserCheck className="w-4 h-4 text-emerald-400" />
                      <span>Patient Preparation</span>
                    </div>
                    <span className="text-xs font-mono text-emerald-400">{patient?.patient_ready ? 'READY' : 'NOT READY'}</span>
                  </div>
                  <div className="text-[11px] text-slate-400 space-y-1 font-mono">
                    <div>Consent Form: {patient?.consent_complete ? '✅ Complete' : '❌ Incomplete'}</div>
                    <div>Fasting Status: {patient?.fasting_complete ? '✅ Confirmed' : '❌ Pending'}</div>
                    <div>Vitals: {patient?.vitals_status || 'NORMAL'}</div>
                  </div>
                </div>

                {/* Staff */}
                <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2 text-xs font-semibold text-slate-200">
                      <Users className="w-4 h-4 text-blue-400" />
                      <span>Staff Roster</span>
                    </div>
                    <span className="text-xs font-mono text-blue-400">ASSIGNED</span>
                  </div>
                  <div className="text-[11px] text-slate-400 space-y-1 font-mono">
                    {staff.map((s: any, idx: number) => (
                      <div key={idx}>
                        {s.role}: <span className={s.availability_status === 'AVAILABLE' ? 'text-emerald-400' : 'text-amber-400'}>{s.availability_status || 'NULL'}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Equipment */}
                <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2 text-xs font-semibold text-slate-200">
                      <Wrench className="w-4 h-4 text-amber-400" />
                      <span>Equipment Status</span>
                    </div>
                    <span className={`text-xs font-mono ${equipment.length > 0 && equipment.every((eq: any) => eq.status === 'READY') ? 'text-emerald-400' : 'text-amber-400'}`}>
                      {equipment.length > 0 && equipment.every((eq: any) => eq.status === 'READY') ? 'ALL READY' : 'CHECK REQUIRED'}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400 space-y-1 font-mono">
                    {equipment.length > 0 ? equipment.map((eq: any, idx: number) => (
                      <div key={idx}>
                        {eq.equipment_name}: <span className={eq.status === 'READY' ? 'text-emerald-400' : eq.status === 'FAULTY' ? 'text-rose-400' : 'text-amber-400'}>{eq.status}</span>
                      </div>
                    )) : (
                      <div>No equipment records logged</div>
                    )}
                  </div>
                </div>

                {/* Supplies */}
                <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2 text-xs font-semibold text-slate-200">
                      <PackageCheck className="w-4 h-4 text-purple-400" />
                      <span>Sterile Supplies</span>
                    </div>
                    <span className="text-xs font-mono text-purple-400">{supplies?.status || 'AVAILABLE'}</span>
                  </div>
                  <div className="text-[11px] text-slate-400 space-y-1 font-mono">
                    <div>Sterility: {supplies?.sterility_confirmed ? '✅ Confirmed' : '❌ Pending'}</div>
                    <div>Qty: {supplies?.available_quantity || 0} / {supplies?.required_quantity || 0} Trays</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Blocking Issues & Recommended Action */}
            {assessment?.blocking_issues && assessment.blocking_issues !== 'None' && (
              <div className="bg-rose-500/10 border border-rose-500/30 p-4 rounded-xl space-y-2">
                <div className="flex items-center gap-2 text-rose-400 text-xs font-bold uppercase tracking-wider">
                  <ShieldAlert className="w-4 h-4" />
                  <span>Blocking Operational Issues</span>
                </div>
                <p className="text-xs text-rose-200 font-mono leading-relaxed">{assessment.blocking_issues}</p>
              </div>
            )}

            <div className="bg-blue-500/10 border border-blue-500/30 p-4 rounded-xl space-y-2">
              <div className="flex items-center gap-2 text-blue-400 text-xs font-bold uppercase tracking-wider">
                <CheckCircle2 className="w-4 h-4" />
                <span>Recommended Action Plan</span>
              </div>
              <p className="text-xs text-blue-200 font-mono leading-relaxed">
                {assessment?.recommended_actions || 'Proceed with scheduled surgery.'}
              </p>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-700/80 bg-slate-900/60 flex justify-end">
          <button onClick={onClose} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium transition">
            Close Modal
          </button>
        </div>
      </div>
    </div>
  );
};
