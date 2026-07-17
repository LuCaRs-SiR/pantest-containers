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
    <label for={id} class="block text-sm text-cockpit-muted mb-1 font-ui">{label}</label>
  {/if}
  <input bind:value {id} {placeholder} {onkeydown} class="input" />
</div>

<style lang="postcss">
  .input {
    @apply w-full px-4 py-2.5 bg-cockpit-bg/80 border border-white/10 rounded-lg text-cockpit-text placeholder-cockpit-muted/60 focus:border-cockpit-accent focus:outline-none font-ui;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
  }
  .input:focus {
    box-shadow: 0 0 12px rgba(0, 175, 255, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.04);
  }
</style>
