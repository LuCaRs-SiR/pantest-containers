<script lang="ts">
  let { logs = [] }: { logs?: string[] } = $props();
</script>

<div class="system-logs glow-card">
  <div class="header">
    <div class="header-line"></div>
    <h3 class="section-title font-display">System Logs</h3>
  </div>
  <div class="logs cockpit-scrollbar">
    {#each logs as log}
      <div class="log-line font-mono">{log}</div>
    {/each}
  </div>
</div>

<style lang="postcss">
  .system-logs {
    @apply p-4 h-full flex flex-col;
  }
  .header {
    @apply flex items-center gap-3 mb-3;
  }
  .header-line {
    @apply w-1 h-5 rounded-full bg-cockpit-accent;
    box-shadow: 0 0 8px var(--cockpit-accent-glow);
  }
  .section-title {
    @apply text-lg font-bold text-cockpit-text tracking-wide;
  }
  .logs {
    @apply flex-1 p-3 rounded-lg overflow-y-auto;
    background: rgba(0, 0, 0, 0.45);
    border: 1px solid rgba(0, 175, 255, 0.15);
  }
  .log-line {
    @apply text-cockpit-muted border-b border-white/5 py-1.5 text-xs;
  }
</style>
