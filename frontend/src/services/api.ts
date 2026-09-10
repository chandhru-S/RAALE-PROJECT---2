import axios from 'axios';
import { SystemSummary, TheatreSummary, ReadinessAssessment, AlertItem, ExperimentMetrics, SimulationResult } from '../types';

const API_BASE = '/api';

export const api = {
  getTheatres: async (): Promise<{ summary: SystemSummary; theatres: TheatreSummary[] }> => {
    const res = await axios.get(`${API_BASE}/theatres`);
    return res.data;
  },

  getSurgeries: async () => {
    const res = await axios.get(`${API_BASE}/surgeries`);
    return res.data;
  },

  getSurgeryDetail: async (surgeryId: string) => {
    const res = await axios.get(`${API_BASE}/surgeries/${surgeryId}`);
    return res.data;
  },

  getReadinessBoard: async (checkpoint: string = 'T-30m'): Promise<ReadinessAssessment[]> => {
    const res = await axios.get(`${API_BASE}/readiness`, { params: { checkpoint } });
    return res.data;
  },

  getAlerts: async (status: string = 'ALL'): Promise<AlertItem[]> => {
    const res = await axios.get(`${API_BASE}/alerts`, { params: { status } });
    return res.data;
  },

  acknowledgeAlert: async (alertId: string) => {
    const res = await axios.post(`${API_BASE}/alerts/${alertId}/acknowledge`);
    return res.data;
  },

  getAnalytics: async () => {
    const res = await axios.get(`${API_BASE}/analytics`);
    return res.data;
  },

  getExperimentResults: async (): Promise<ExperimentMetrics> => {
    const res = await axios.get(`${API_BASE}/experiments`);
    return res.data;
  },

  runExperiment: async (): Promise<{ results: ExperimentMetrics }> => {
    const res = await axios.post(`${API_BASE}/run-experiment`);
    return res.data;
  },

  simulate: {
    staffMissing: async (theatreId: string = 'OT001'): Promise<SimulationResult> => {
      const res = await axios.post(`${API_BASE}/simulate/staff-missing`, null, { params: { theatre_id: theatreId } });
      return res.data;
    },
    equipmentFailure: async (theatreId: string = 'OT002'): Promise<SimulationResult> => {
      const res = await axios.post(`${API_BASE}/simulate/equipment-failure`, null, { params: { theatre_id: theatreId } });
      return res.data;
    },
    patientNotReady: async (theatreId: string = 'OT003'): Promise<SimulationResult> => {
      const res = await axios.post(`${API_BASE}/simulate/patient-not-ready`, null, { params: { theatre_id: theatreId } });
      return res.data;
    },
    supplyMissing: async (theatreId: string = 'OT004'): Promise<SimulationResult> => {
      const res = await axios.post(`${API_BASE}/simulate/supply-missing`, null, { params: { theatre_id: theatreId } });
      return res.data;
    },
    overrun: async (theatreId: string = 'OT005'): Promise<SimulationResult> => {
      const res = await axios.post(`${API_BASE}/simulate/overrun`, null, { params: { theatre_id: theatreId } });
      return res.data;
    },
    emergency: async (theatreId: string = 'OT006'): Promise<SimulationResult> => {
      const res = await axios.post(`${API_BASE}/simulate/emergency`, null, { params: { theatre_id: theatreId } });
      return res.data;
    },
    reset: async () => {
      const res = await axios.post(`${API_BASE}/simulate/reset`);
      return res.data;
    }
  }
};
