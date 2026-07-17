<script lang="ts">
  import { onMount } from 'svelte';
  import { getStatus } from '$lib/services';

  let running = $state(0);
  let total = $state(0);
  let ai = $state('sprawdzanie...');

  async function refreshStatus() {
    try {
      const data = await getStatus();
      const containers = Object.values(data.containers ?? {});
      total = containers.length;
      running = containers.filter((x) => x.running).length;
      ai = data.ai_gateway?.error ? 'offline' : 'online';
    } catch {
      ai = 'offline';
    }
  }

  onMount(refreshStatus);
</script>

<div class="topbar neon-border glass">
  <div class="status-item">
    <span class="status-label">Tryb:</span>
    <span class="status-value">Panel Pentest</span>
    <span class="status-badge cyan">Aktywny</span>
  </div>
  <div class="status-item">
    <span class="status-label">Kontenery:</span>
    <span class="status-value">{running}/{total}</span>
  </div>
  <div class="status-item">
    <span class="status-label">AI Gateway:</span>
    <span class="status-value" class:green={ai === 'online'}>{ai}</span>
  </div>
</div>

<style>
  .topbar {
    display: flex;
    justify-content: space-between;
    padding: 15px 25px;
    margin-bottom: 20px;
    font-family: 'Orbitron', sans-serif;
    font-size: 14px;
  }

  .status-item {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .status-label {
    color: var(--text-secondary);
  }

  .status-value {
    color: var(--text-main);
    font-weight: bold;
    text-shadow: 0 0 8px var(--accent-cyan);
  }

  .status-value.green {
    color: var(--terminal-green);
    text-shadow: 0 0 8px var(--terminal-green);
  }

  .status-badge {
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: bold;
  }

  .status-badge.cyan {
    color: black;
    background: var(--accent-cyan);
    box-shadow: 0 0 10px var(--accent-cyan);
  }
</style>
