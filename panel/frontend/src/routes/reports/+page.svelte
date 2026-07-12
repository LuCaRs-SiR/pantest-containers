<script lang="ts">
  import LogViewer from '../../components/LogViewer.svelte';

  const logs = [
    '2026-07-12 00:00:00 - system ready',
    '2026-07-12 00:00:01 - connected to ai-gateway',
    '2026-07-12 00:00:02 - dashboard loaded'
  ];
</script>

<h1 class="text-3xl font-black text-cockpit-accent mb-6">Raporty</h1>

<LogViewer {logs} />
