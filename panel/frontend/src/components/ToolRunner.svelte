<script lang="ts">
  import Button from './Button.svelte';
  import Input from './Input.svelte';
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

<h1 class="text-3xl font-black text-cockpit-accent mb-6">{title}</h1>
<div class="flex gap-2 mb-4">
  <Input bind:value {placeholder} />
  <Button onclick={run}>Uruchom</Button>
</div>
<Terminal {output} />
