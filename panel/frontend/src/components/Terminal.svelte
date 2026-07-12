<script lang="ts">
  let { output = '' }: { output?: string } = $props();
</script>

<pre class="terminal cockpit-scrollbar" aria-label="Terminal output"><code>{output || '$ ready...'}</code></pre>

<style>
  .terminal {
    @apply bg-cockpit-terminal text-cockpit-terminal-green p-4 rounded-lg font-mono text-sm whitespace-pre-wrap border border-cockpit-accent/30 overflow-auto max-h-96;
  }
</style>
