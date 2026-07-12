<script lang="ts">
  let { logs = [] }: { logs?: string[] } = $props();
</script>

<div class="log-viewer cockpit-scrollbar">
  {#each logs as log}
    <div class="log-line">{log}</div>
  {/each}
</div>

<style>
  .log-viewer {
    @apply bg-cockpit-terminal p-4 rounded-lg font-mono text-sm max-h-96 overflow-y-auto border border-cockpit-accent/30;
  }
  .log-line {
    @apply text-cockpit-terminal-green border-b border-white/5 py-1;
  }
</style>
