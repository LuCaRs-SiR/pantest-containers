<script lang="ts">
  let { logs = [] }: { logs?: string[] } = $props();
</script>

<div class="system-logs glow-card">
  <h3 class="section-title">System Logs</h3>
  <div class="logs cockpit-scrollbar">
    {#each logs as log}
      <div class="log-line">{log}</div>
    {/each}
  </div>
</div>

<style>
  .system-logs {
    @apply p-4 h-full flex flex-col;
  }
  .section-title {
    @apply text-lg font-bold text-cockpit-text mb-3;
  }
  .logs {
    @apply flex-1 bg-cockpit-terminal/50 p-3 rounded-lg font-mono text-xs overflow-y-auto;
  }
  .log-line {
    @apply text-cockpit-muted border-b border-white/5 py-1;
  }
</style>
