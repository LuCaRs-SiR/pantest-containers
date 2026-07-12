<script lang="ts">
  let { output = '' }: { output?: string } = $props();
</script>

<div class="mini-terminal glow-card">
  <div class="header">
    <div class="header-line header-line-green"></div>
    <h3 class="section-title font-display">Terminal Output</h3>
  </div>
  <pre class="terminal cockpit-scrollbar font-mono"><code>{output || '$ ready...'}</code></pre>
</div>

<style>
  .mini-terminal {
    @apply p-4 h-full flex flex-col;
  }
  .header {
    @apply flex items-center gap-3 mb-3;
  }
  .header-line {
    @apply w-1 h-5 rounded-full;
  }
  .header-line-green {
    @apply bg-cockpit-terminal-green;
    box-shadow: 0 0 8px var(--cockpit-terminal-green);
  }
  .section-title {
    @apply text-lg font-bold text-cockpit-text tracking-wide;
  }
  .terminal {
    @apply flex-1 p-3 rounded-lg text-xs whitespace-pre-wrap overflow-auto;
    background: rgba(0, 0, 0, 0.7);
    color: var(--cockpit-terminal-green);
    border: 1px solid rgba(0, 255, 127, 0.25);
    box-shadow: inset 0 0 20px rgba(0, 255, 127, 0.05);
    text-shadow: 0 0 4px rgba(0, 255, 127, 0.3);
  }
</style>
