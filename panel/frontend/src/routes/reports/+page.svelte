<script lang="ts">
  import { onMount } from 'svelte';
  import { getStatus, getReports, getReport } from '$lib/services';
  import type { StatusResponse, ReportListItem, AssistantReport } from '$lib/types';

  let status = $state<StatusResponse | null>(null);
  let reports = $state<ReportListItem[]>([]);
  let activeReport = $state<AssistantReport | null>(null);
  let loading = $state(true);
  let loadingReports = $state(false);
  let loadingReportDetails = $state(false);
  let error = $state('');
  let reportsError = $state('');
  const REPORTS_LIMIT = 10;

  const issues = $derived.by(() => {
    if (!status) return [];
    return Object.entries(status.containers)
      .map(([name, item]) => ({ name, item }))
      .filter(
        ({ item }) =>
          !item.exists ||
          !item.running ||
          item.status === 'restarting' ||
          (item.restart_count ?? 0) > 0 ||
          Boolean(item.error)
      );
  });

  const healthy = $derived.by(() => {
    if (!status) return 0;
    return Object.values(status.containers).filter((x) => x.running).length;
  });

  const total = $derived.by(() => {
    if (!status) return 0;
    return Object.keys(status.containers).length;
  });

  const visibleReports = $derived.by(() => reports.slice(0, REPORTS_LIMIT));

  function isActiveReport(reportId: string) {
    return activeReport?.id === reportId;
  }

  async function refresh() {
    loading = true;
    error = '';
    try {
      status = await getStatus();
    } catch (err: any) {
      error = err.message ?? 'Nie udało się pobrać statusu.';
    } finally {
      loading = false;
    }
  }

  async function refreshReports() {
    loadingReports = true;
    reportsError = '';
    try {
      const data = await getReports();
      reports = data.reports;
    } catch (err: any) {
      reportsError = err.message ?? 'Nie udało się pobrać raportów.';
    } finally {
      loadingReports = false;
    }
  }

  async function openReport(reportId: string) {
    loadingReportDetails = true;
    reportsError = '';
    try {
      activeReport = await getReport(reportId);
    } catch (err: any) {
      reportsError = err.message ?? 'Nie udało się pobrać szczegółów raportu.';
    } finally {
      loadingReportDetails = false;
    }
  }

  async function toggleReport(reportId: string) {
    if (isActiveReport(reportId)) {
      activeReport = null;
      return;
    }
    await openReport(reportId);
  }

  onMount(async () => {
    await refresh();
    await refreshReports();
  });
</script>

<h1 class="text-3xl font-black text-cockpit-accent mb-6">Status Kontenerów</h1>

<button class="neon-glow mb-4" onclick={refresh} disabled={loading}>
  {loading ? 'Odświeżanie...' : 'Odśwież'}
</button>

{#if error}
  <p class="error">{error}</p>
{/if}

{#if status}
  <div class="summary glass neon-border">
    <div><strong>Backend:</strong> {status.backend}</div>
    <div><strong>Kontenery Running:</strong> {healthy}/{total}</div>
    <div><strong>AI Gateway:</strong> {status.ai_gateway.error ? status.ai_gateway.error : 'ok'}</div>
  </div>

  <div class="summary glass neon-border issues">
    <h2>Diagnostyka</h2>
    {#if issues.length === 0}
      <p>Brak wykrytych problemów z kontenerami.</p>
    {:else}
      {#each issues as row}
        <div class="issue-row">
          <strong>{row.name}</strong>
          <span>status={row.item.status}</span>
          <span>restarty={row.item.restart_count ?? 0}</span>
          {#if row.item.error}
            <span class="issue-error">{row.item.error}</span>
          {/if}
        </div>
      {/each}
    {/if}
  </div>

  <div class="grid">
    {#each Object.entries(status.containers) as [name, item]}
      <div class="card glass neon-border">
        <h3>{name}</h3>
        <p><strong>Status:</strong> {item.status}</p>
        <p><strong>State:</strong> {item.state_status ?? 'n/a'}</p>
        <p><strong>Running:</strong> {item.running ? 'tak' : 'nie'}</p>
        <p><strong>Exists:</strong> {item.exists ? 'tak' : 'nie'}</p>
        <p><strong>Restarts:</strong> {item.restart_count ?? 0}</p>
        <p><strong>Health:</strong> {item.health_status ?? 'n/a'}</p>
      </div>
    {/each}
  </div>
{/if}

<section class="summary glass neon-border report-box">
  <div class="report-head">
    <h2>Raporty Asystenta</h2>
    <button class="neon-glow" onclick={refreshReports} disabled={loadingReports}>
      {loadingReports ? 'Pobieranie...' : 'Odśwież raporty'}
    </button>
  </div>

  {#if reportsError}
    <p class="error">{reportsError}</p>
  {/if}

  {#if reports.length === 0}
    <p>Brak raportów. Uruchom zadanie w zakładce AI Assistant.</p>
  {:else}
    <p class="reports-caption">Wyświetlanie {Math.min(reports.length, REPORTS_LIMIT)} z {reports.length} ostatnich raportów.</p>
    <div class="reports-list">
      {#each visibleReports as report}
        <div class="report-item">
          <div class="report-meta">
            <div><strong>{report.task}</strong></div>
            <div>
              status={report.status} | kroki={report.steps_total} | błędy={report.steps_failed}
            </div>
            <div class="stamp">{report.created_at}</div>
          </div>
          <button
            class="toggle-icon"
            aria-label={isActiveReport(report.id) ? `Zwiń raport ${report.id}` : `Rozwiń raport ${report.id}`}
            title={isActiveReport(report.id) ? 'Zwiń szczegóły raportu' : 'Rozwiń szczegóły raportu'}
            onclick={() => toggleReport(report.id)}
          >
            {isActiveReport(report.id) ? '▾' : '▸'}
          </button>
        </div>
      {/each}
    </div>
  {/if}

  {#if loadingReportDetails}
    <p>Wczytywanie raportu...</p>
  {/if}

  {#if activeReport}
    <div class="active-report">
      <h3>Szczegóły raportu: {activeReport.id}</h3>
      <p><strong>Zadanie:</strong> {activeReport.task}</p>
      <p>
        <strong>Profile:</strong>
        {(activeReport.selected_profiles ?? []).join(', ') || 'brak'}
      </p>
      <p>
        <strong>Resolved input:</strong>
        target={activeReport.input_resolved?.target ?? '-'},
        domain={activeReport.input_resolved?.domain ?? '-'}
      </p>
      <p><strong>Wniosek:</strong> {activeReport.summary.conclusion}</p>

      {#if activeReport.professional_report}
        <div class="professional-report glass neon-border">
          <h4>Raport Profesjonalny</h4>
          <p>
            <strong>Typ:</strong> {activeReport.professional_report.meta.report_type}
            | <strong>Wersja:</strong> {activeReport.professional_report.meta.version}
            | <strong>Klasyfikacja:</strong> {activeReport.professional_report.meta.classification}
          </p>
          <p>
            <strong>Ryzyko ogólne:</strong>
            {activeReport.professional_report.executive_summary.overall_risk}
          </p>
          <p><strong>Cel audytu:</strong> {activeReport.professional_report.engagement.objective}</p>
          <p>
            <strong>Zakres:</strong>
            target={activeReport.professional_report.engagement.scope.target ?? '-'},
            domain={activeReport.professional_report.engagement.scope.domain ?? '-'}
          </p>

          <div class="pro-grid">
            <div>
              <h5>Metodologia</h5>
              <ul>
                {#each activeReport.professional_report.methodology.standard_reference as item}
                  <li>{item}</li>
                {/each}
              </ul>
            </div>
            <div>
              <h5>Kluczowe obserwacje</h5>
              <ul>
                {#each activeReport.professional_report.executive_summary.key_observations as item}
                  <li>{item}</li>
                {/each}
              </ul>
            </div>
          </div>

          <h5>Ustalenia</h5>
          <div class="findings-grid">
            {#each activeReport.professional_report.findings as finding}
              <div class="card glass neon-border finding-card">
                <h6>{finding.id} · {finding.title}</h6>
                <p><strong>Severity:</strong> {finding.severity}</p>
                <p><strong>Kategoria:</strong> {finding.category}</p>
                <p><strong>Asset:</strong> {finding.affected_asset}</p>
                <p><strong>Evidence:</strong> {finding.evidence}</p>
                <p><strong>Impact:</strong> {finding.impact}</p>
                <p><strong>Rekomendacja:</strong> {finding.recommendation}</p>
              </div>
            {/each}
          </div>

          <div class="pro-grid">
            <div>
              <h5>Rekomendacje natychmiastowe</h5>
              <ul>
                {#each activeReport.professional_report.recommendations.immediate as item}
                  <li>{item}</li>
                {/each}
              </ul>
            </div>
            <div>
              <h5>Ograniczenia raportu</h5>
              <ul>
                {#each activeReport.professional_report.limitations as item}
                  <li>{item}</li>
                {/each}
              </ul>
            </div>
          </div>

          {#if activeReport.professional_report.markdown}
            <h5>Wersja dokumentowa (Markdown)</h5>
            <pre class="markdown-preview">{activeReport.professional_report.markdown}</pre>
          {/if}
        </div>
      {/if}

      <div class="steps-grid">
        {#each activeReport.steps as step}
          <div class="card glass neon-border">
            <h4>{step.order}. {step.label}</h4>
            <p><strong>Narzędzie:</strong> {step.tool}</p>
            <p><strong>Status:</strong> {step.status}</p>
            <p><strong>Exit code:</strong> {step.exit_code}</p>
            <pre>{step.output}</pre>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</section>

<style>
  .summary {
    padding: 16px;
    margin-bottom: 16px;
    display: grid;
    gap: 8px;
  }

  .issues {
    border-color: rgba(255, 140, 0, 0.4);
  }

  .issues h2 {
    margin: 0;
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
  }

  .issue-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    font-size: 14px;
  }

  .issue-error {
    color: #ff6b6b;
    max-width: 100%;
    overflow-wrap: anywhere;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
  }

  .card {
    padding: 14px;
  }

  h3 {
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
  }

  p {
    margin: 4px 0;
  }

  .error {
    color: #ff6b6b;
    margin-bottom: 12px;
  }

  .report-box {
    margin-top: 20px;
  }

  .report-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
  }

  .report-head h2 {
    margin: 0;
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
  }

  .reports-list {
    display: grid;
    gap: 8px;
    margin-bottom: 14px;
  }

  .reports-caption {
    margin: 0 0 8px;
    color: var(--text-secondary);
    font-size: 13px;
  }

  .report-item {
    text-align: left;
    background: rgba(0, 229, 255, 0.08);
    border: 1px solid rgba(0, 229, 255, 0.2);
    border-radius: 8px;
    padding: 10px;
    color: var(--text-main);
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 10px;
    align-items: center;
  }

  .report-item:hover {
    box-shadow: 0 0 14px rgba(0, 229, 255, 0.15);
  }

  .report-meta {
    min-width: 0;
  }

  .toggle-icon {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    border: 1px solid rgba(0, 229, 255, 0.35);
    background: rgba(0, 229, 255, 0.16);
    color: var(--text-main);
    font-size: 18px;
    line-height: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.12s ease, box-shadow 0.12s ease;
  }

  .toggle-icon:hover {
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.22);
    transform: scale(1.05);
  }

  .stamp {
    margin-top: 3px;
    color: var(--text-secondary);
    font-size: 12px;
  }

  .active-report {
    border-top: 1px solid rgba(0, 229, 255, 0.2);
    padding-top: 12px;
  }

  .professional-report {
    margin: 14px 0;
    padding: 12px;
  }

  .professional-report h4,
  .professional-report h5,
  .professional-report h6 {
    margin: 0 0 8px;
    font-family: 'Orbitron', sans-serif;
  }

  .professional-report h5 {
    margin-top: 10px;
  }

  .pro-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 10px;
  }

  .professional-report ul {
    margin: 0;
    padding-left: 18px;
  }

  .findings-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 10px;
  }

  .finding-card h6 {
    margin-bottom: 6px;
  }

  .markdown-preview {
    max-height: 260px;
    overflow: auto;
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(0, 229, 255, 0.12);
    border-radius: 6px;
    padding: 10px;
    white-space: pre-wrap;
    font-size: 12px;
  }

  .active-report h3 {
    margin-bottom: 8px;
  }

  .steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 10px;
  }

  .steps-grid h4 {
    margin: 0 0 8px;
  }

  .steps-grid pre {
    max-height: 180px;
    overflow: auto;
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(0, 229, 255, 0.12);
    border-radius: 6px;
    padding: 8px;
    white-space: pre-wrap;
    font-size: 12px;
  }
</style>
