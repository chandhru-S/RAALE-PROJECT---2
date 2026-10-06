import React, { useState, useEffect, useCallback } from 'react';
import { Navbar } from './components/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { ReadinessBoardPage } from './pages/ReadinessBoardPage';
import { AlertsPage } from './pages/AlertsPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { FailureSimulatorPage } from './pages/FailureSimulatorPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { SurgeryDetailModal } from './components/SurgeryDetailModal';
import { api } from './services/api';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedSurgeryId, setSelectedSurgeryId] = useState<string | null>(null);
  const [activeAlertCount, setActiveAlertCount] = useState(0);

  const fetchAlertCount = useCallback(() => {
    api.getAlerts('ACTIVE')
      .then(alerts => setActiveAlertCount(alerts.length))
      .catch(() => setActiveAlertCount(0));
  }, []);

  useEffect(() => {
    fetchAlertCount();
    const interval = setInterval(fetchAlertCount, 30000);
    return () => clearInterval(interval);
  }, [fetchAlertCount]);

  return (
    <div className="min-h-screen bg-[#0B132B] text-slate-100 flex flex-col font-sans">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} activeAlertCount={activeAlertCount} />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6">
        {activeTab === 'dashboard' && (
          <DashboardPage
            onSelectSurgery={(id) => setSelectedSurgeryId(id)}
            onNavigateTab={(tab) => setActiveTab(tab)}
          />
        )}
        {activeTab === 'readiness' && (
          <ReadinessBoardPage onSelectSurgery={(id) => setSelectedSurgeryId(id)} />
        )}
        {activeTab === 'alerts' && (
          <AlertsPage
            onSelectSurgery={(id) => setSelectedSurgeryId(id)}
            onRefreshAlerts={fetchAlertCount}
          />
        )}
        {activeTab === 'analytics' && <AnalyticsPage />}
        {activeTab === 'simulator' && <FailureSimulatorPage onRefreshAlerts={fetchAlertCount} />}
        {activeTab === 'evaluation' && <EvaluationPage />}
      </main>

      <footer className="border-t border-slate-800/80 bg-slate-950 py-4 px-6 text-center text-xs text-slate-500 font-mono">
        ORRS Operational Synchroniser • Multi-Specialty Operating Theatre Command Engine • De-identified Synthetic Data Only
      </footer>

      {/* Drilldown Modal */}
      <SurgeryDetailModal
        surgeryId={selectedSurgeryId}
        onClose={() => setSelectedSurgeryId(null)}
      />
    </div>
  );
};

export default App;
