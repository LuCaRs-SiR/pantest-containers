<script lang="ts">
  let { output = '' }: { output?: string } = $props();
</script>

<pre class="terminal neon-border">{output}</pre>

<style>
  .terminal {
    background: black;
    color: var(--terminal-green);
    padding: 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 15px;
    border-radius: var(--radius);
    box-shadow: 0 0 20px var(--accent-cyan);
    white-space: pre-wrap;
    overflow: auto;
  }
</style>
