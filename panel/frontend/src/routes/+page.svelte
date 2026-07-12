<script lang="ts">
  import ProgressDial from '../components/ProgressDial.svelte';
  import PriorityList from '../components/PriorityList.svelte';
  import TeamPerformance from '../components/TeamPerformance.svelte';
  import ChangeLog from '../components/ChangeLog.svelte';
  import AIProjectAssistant from '../components/AIProjectAssistant.svelte';
  import type { PriorityTask, TeamMember, LogEntry } from '$lib/types';

  const tasks: PriorityTask[] = [
    { name: 'Integracja API z modułem płatności', priority: 'critical' },
    { name: 'Poprawa wydajności dashboardu', priority: 'high' },
    { name: 'Aktualizacja dokumentacji', priority: 'medium' },
    { name: 'Testy jednostkowe modułu raportów', priority: 'low' }
  ];

  const team: TeamMember[] = [
    { name: 'Anna K.', value: 92 },
    { name: 'Marek W.', value: 78 },
    { name: 'Kasia L.', value: 85 },
    { name: 'Tomek Z.', value: 67 }
  ];

  const logEntries: LogEntry[] = [
    { time: '10:42', event: 'Zadanie #12 przesunięte do QA' },
    { time: '09:15', event: 'Dodano nowy moduł raportów' },
    { time: '08:30', event: 'Sprint 14 rozpoczęty' },
    { time: 'Wczoraj', event: 'Zamknięto 7 zgłoszeń' }
  ];
</script>

<h1 class="neon-text chromatic fade-in">PULPIT ZARZĄDZANIA PROJEKTEM</h1>

<div class="dashboard fade-in">
  <div class="top-row">
    <ProgressDial value={90} label="Progres Zadania" />
    <PriorityList title="Lista Priorytetów" {tasks} />
    <TeamPerformance members={team} />
  </div>

  <div class="bottom-row">
    <ChangeLog entries={logEntries} />
    <AIProjectAssistant />
  </div>
</div>

<style>
  h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 26px;
    margin-bottom: 25px;
  }

  .dashboard {
    display: flex;
    flex-direction: column;
    gap: 25px;
  }

  .top-row {
    display: grid;
    grid-template-columns: 1fr 1.2fr 1fr;
    gap: 25px;
  }

  .bottom-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
  }

  @media (max-width: 1200px) {
    .top-row {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (max-width: 900px) {
    .top-row,
    .bottom-row {
      grid-template-columns: 1fr;
    }
  }
</style>
