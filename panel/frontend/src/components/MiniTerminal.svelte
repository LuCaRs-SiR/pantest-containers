<script lang="ts">
  let { output = '' }: { output?: string } = $props();
</script>

<div class="mini-terminal glow-card">
  <h3 class="section-title">Terminal Output</h3>
  <pre class="terminal cockpit-scrollbar"><code>{output || '$ ready...'}</code></pre>
</div>

<style>
  .mini-terminal {
    @apply p-4 h-full flex flex-col;
  }
  .section-title {
    @apply text-lg font-bold text-cockpit-text mb-3;
  }
  .terminal {
    @apply flex-1 bg-cockpit-terminal text-cockpit-terminal-green p-3 rounded-lg font-mono text-xs whitespace-pre-wrap overflow-auto border border-cockpit-accent/30;
  }
</style>
