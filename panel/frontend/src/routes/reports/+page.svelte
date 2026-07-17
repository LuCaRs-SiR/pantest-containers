<script lang="ts">
  import { onMount } from 'svelte';
  import { getStatus } from '$lib/services';
  import type { StatusResponse } from '$lib/types';

  let status = $state<StatusResponse | null>(null);
  let loading = $state(true);
  let error = $state('');

  async function refresh() {
    loading = true;
    error = '';
    try {
      status = await getStatus();
    } catch (err: any) {
      error = err.message ?? 'Nie udało się pobrać statusu.';
    } finally {
      loading = false;
    }
  }

  onMount(refresh);
</script>

<h1 class="text-3xl font-black text-cockpit-accent mb-6">Status Kontenerów</h1>

<button class="neon-glow mb-4" onclick={refresh} disabled={loading}>
  {loading ? 'Odświeżanie...' : 'Odśwież'}
</button>

{#if error}
  <p class="error">{error}</p>
{/if}

{#if status}
  <div class="summary glass neon-border">
    <div><strong>Backend:</strong> {status.backend}</div>
    <div><strong>AI Gateway:</strong> {JSON.stringify(status.ai_gateway)}</div>
  </div>

  <div class="grid">
    {#each Object.entries(status.containers) as [name, item]}
      <div class="card glass neon-border">
        <h3>{name}</h3>
        <p><strong>Status:</strong> {item.status}</p>
        <p><strong>Running:</strong> {item.running ? 'tak' : 'nie'}</p>
        <p><strong>Exists:</strong> {item.exists ? 'tak' : 'nie'}</p>
      </div>
    {/each}
  </div>
{/if}

<style>
  .summary {
    padding: 16px;
    margin-bottom: 16px;
    display: grid;
    gap: 8px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
  }

  .card {
    padding: 14px;
  }

  h3 {
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
  }

  p {
    margin: 4px 0;
  }

  .error {
    color: #ff6b6b;
    margin-bottom: 12px;
  }
</style>
