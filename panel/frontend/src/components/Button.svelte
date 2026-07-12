<script lang="ts">
  let {
    type = 'button',
    variant = 'primary',
    disabled = false,
    onclick,
    children
  }: {
    type?: 'button' | 'submit';
    variant?: 'primary' | 'danger';
    disabled?: boolean;
    onclick?: (event: MouseEvent) => void;
    children?: () => any;
  } = $props();
</script>

<button {type} {disabled} {onclick} class:primary={variant === 'primary'} class:danger={variant === 'danger'}>
  {#if children}
    {@render children()}
  {/if}
</button>

<style>
  button {
    @apply px-5 py-2.5 rounded-lg font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed;
  }
  .primary {
    @apply bg-cockpit-accent text-cockpit-bg hover:shadow-[0_0_12px_#00AFFF];
  }
  .danger {
    @apply bg-cockpit-danger text-white hover:shadow-[0_0_12px_#FF0055];
  }
</style>
