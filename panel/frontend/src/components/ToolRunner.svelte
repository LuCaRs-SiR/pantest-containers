<script lang="ts">
  import Terminal from './Terminal.svelte';
  import { api } from '$lib/api';

  let {
    title,
    endpoint,
    placeholder,
    paramName = 'target'
  }: {
    title: string;
    endpoint: string;
    placeholder: string;
    paramName?: string;
  } = $props();

  let value = $state('');
  let output = $state('');

  async function run() {
    if (!value.trim()) return;
    output = `Running ${title.toLowerCase()}...`;
    try {
      const res = await api<{ output: string }>(endpoint, 'POST', { [paramName]: value });
      output = res.output;
    } catch (err: any) {
      output = `Error: ${err.message}`;
    }
  }
</script>

<h1 class="neon-text fade-in">{title}</h1>
<div class="tool fade-in">
  <input bind:value {placeholder} />
  <button class="neon-glow" onclick={run}>Uruchom</button>
</div>
<Terminal {output} />

<style>
  h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 28px;
    margin-bottom: 25px;
  }

  .tool {
    display: flex;
    gap: 15px;
    margin-bottom: 25px;
  }

  input {
    flex: 1;
  }
</style>
