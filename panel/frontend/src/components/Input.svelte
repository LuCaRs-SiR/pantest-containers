<script lang="ts">
  let {
    value = $bindable(''),
    placeholder = '',
    label = '',
    onkeydown,
    id = Math.random().toString(36).slice(2)
  }: {
    value?: string;
    placeholder?: string;
    label?: string;
    onkeydown?: (event: KeyboardEvent) => void;
    id?: string;
  } = $props();
</script>

<div class="w-full">
  {#if label}
    <label for={id} class="block text-sm text-cockpit-muted mb-1">{label}</label>
  {/if}
  <input bind:value {id} {placeholder} {onkeydown} class="input" />
</div>

<style>
  .input {
    @apply w-full px-4 py-2.5 bg-cockpit-bg border border-white/10 rounded-lg text-cockpit-text placeholder-cockpit-muted focus:border-cockpit-accent focus:outline-none focus:ring-1 focus:ring-cockpit-accent;
  }
</style>
