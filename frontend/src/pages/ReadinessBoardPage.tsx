import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { ReadinessAssessment } from '../types';
import { ReadinessBadge } from '../components/ReadinessBadge';
import { Clock, Filter, Eye } from 'lucide-react';

interface Props {
  onSelectSurgery: (surgeryId: string) => void;
}

export const ReadinessBoardPage: React.FC<Props> = ({ onSelectSurgery }) => {
  const [assessments, setAssessments] = useState<ReadinessAssessment[]>([]);
  const [checkpoint, setCheckpoint] = useState('T-30m');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.getReadinessBoard(checkpoint)
      .then(res => setAssessments(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [checkpoint]);

  const filtered = assessments.filter(a => statusFilter === 'ALL' || a.overall_status === statusFilter);

  return (
    <div className="space-y-6">
      {/* Top Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">Theatre Readiness Synchronisation Board</h2>
          <p className="text-xs text-slate-400">Multi-checkpoint operational verification across scheduled surgeries</p>
        </div>

        <div className="flex items-center gap-3">
          {/* Checkpoint selector */}
          <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-lg border border-slate-800 text-xs font-mono">
            <Clock className="w-3.5 h-3.5 text-slate-400 ml-2" />
            {['T-60m', 'T-30m', 'T-15m', 'T-0m'].map(cp => (
              <button
                key={cp}
                onClick={() => setCheckpoint(cp)}
                className={`px-2.5 py-1 rounded-md transition ${checkpoint === cp ? 'bg-blue-600 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}`}
              >
                {cp}
              </button>
            ))}
          </div>

          {/* Status filter */}
          <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-lg border border-slate-800 text-xs font-mono">
            <Filter className="w-3.5 h-3.5 text-slate-400 ml-2" />
            {['ALL', 'READY', 'AT_RISK', 'NOT_READY', 'DATA_INCOMPLETE'].map(st => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-2 py-1 rounded-md transition ${statusFilter === st ? 'bg-slate-700 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}`}
              >
                {st.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Table */}
      <div className="glass-panel rounded-xl overflow-hidden border border-slate-800 shadow-xl">
        {loading ? (
          <div className="p-12 text-center text-slate-400 font-mono animate-pulse">Evaluating readiness engine rules...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-900/80 text-slate-400 uppercase text-[11px] border-b border-slate-800">
                <tr>
                  <th className="py-3.5 px-4 font-semibold">Theatre</th>
                  <th className="py-3.5 px-4 font-semibold">Surgery ID</th>
                  <th className="py-3.5 px-4 font-semibold">Department</th>
                  <th className="py-3.5 px-4 font-semibold">Patient</th>
                  <th className="py-3.5 px-4 font-semibold">Staff</th>
                  <th className="py-3.5 px-4 font-semibold">Equipment</th>
                  <th className="py-3.5 px-4 font-semibold">Supplies</th>
                  <th className="py-3.5 px-4 font-semibold">Readiness Score</th>
                  <th className="py-3.5 px-4 font-semibold">Confidence</th>
                  <th className="py-3.5 px-4 font-semibold">Overall Status</th>
                  <th className="py-3.5 px-4 font-semibold text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filtered.map((item) => (
                  <tr key={item.surgery_id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4 font-bold text-slate-100">{item.theatre_id}</td>
                    <td className="py-3 px-4 text-blue-400 font-bold">{item.surgery_id}</td>
                    <td className="py-3 px-4 text-slate-300">{item.department}</td>
                    <td className="py-3 px-4">
                      <span className={item.patient_status === 'READY' ? 'text-emerald-400' : 'text-rose-400 font-bold'}>
                        {item.patient_status}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={item.staff_status === 'READY' ? 'text-emerald-400' : 'text-amber-400 font-bold'}>
                        {item.staff_status}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={item.equipment_status === 'READY' ? 'text-emerald-400' : 'text-rose-400 font-bold'}>
                        {item.equipment_status}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={item.supply_status === 'READY' ? 'text-emerald-400' : 'text-amber-400 font-bold'}>
                        {item.supply_status}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-bold text-slate-100">{item.readiness_score}%</td>
                    <td className="py-3 px-4 text-cyan-400">{item.confidence_score}%</td>
                    <td className="py-3 px-4">
                      <ReadinessBadge status={item.overall_status} />
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => onSelectSurgery(item.surgery_id)}
                        className="p-1.5 rounded bg-blue-600/20 text-blue-400 hover:bg-blue-600 hover:text-white transition flex items-center gap-1 text-[11px] ml-auto"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Inspect</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
