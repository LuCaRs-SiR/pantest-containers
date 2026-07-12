<script lang="ts">
  import type { LogEntry } from '$lib/types';

  let { entries = [] }: { entries?: LogEntry[] } = $props();
</script>

<div class="log neon-card glass">
  <h3 class="log-title">Dziennik Zmian</h3>
  <ul class="log-list">
    {#each entries as entry}
      <li class="log-item">
        <span class="log-time">{entry.time}</span>
        <span class="log-event">{entry.event}</span>
      </li>
    {/each}
  </ul>
</div>

<style>
  .log {
    padding: 20px;
  }

  .log-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
    margin-bottom: 15px;
    color: var(--text-main);
  }

  .log-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 180px;
    overflow-y: auto;
  }

  .log-item {
    display: flex;
    gap: 12px;
    padding: 10px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
  }

  .log-time {
    color: var(--accent-cyan);
    white-space: nowrap;
  }

  .log-event {
    color: var(--text-secondary);
  }
</style>
