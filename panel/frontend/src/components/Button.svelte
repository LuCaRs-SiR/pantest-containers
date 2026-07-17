<script lang="ts">
  let {
    type = 'button',
    variant = 'primary',
    disabled = false,
    onclick,
    children
  }: {
    type?: 'button' | 'submit';
    variant?: 'primary' | 'danger' | 'ghost';
    disabled?: boolean;
    onclick?: (event: MouseEvent) => void;
    children?: () => any;
  } = $props();
</script>

<button {type} {disabled} {onclick} class="btn {variant}">
  {#if children}
    {@render children()}
  {/if}
</button>

<style lang="postcss">
  .btn {
    @apply relative px-6 py-2.5 rounded-lg font-display font-bold text-sm tracking-wider uppercase overflow-hidden transition-all duration-300;
  }
  .btn:disabled {
    @apply opacity-50 cursor-not-allowed;
  }
  .primary {
    @apply text-cockpit-bg;
    background: linear-gradient(135deg, var(--cockpit-accent), #0088cc);
    border: 1px solid rgba(0, 175, 255, 0.5);
    box-shadow: 0 0 14px rgba(0, 175, 255, 0.3);
  }
  .primary:hover:not(:disabled) {
    box-shadow: 0 0 24px rgba(0, 175, 255, 0.55);
    transform: translateY(-1px);
  }
  .danger {
    @apply text-white;
    background: linear-gradient(135deg, var(--cockpit-danger), #cc0044);
    border: 1px solid rgba(255, 0, 85, 0.5);
    box-shadow: 0 0 14px rgba(255, 0, 85, 0.3);
  }
  .danger:hover:not(:disabled) {
    box-shadow: 0 0 24px rgba(255, 0, 85, 0.55);
  }
  .ghost {
    @apply text-cockpit-accent border border-cockpit-accent/40 bg-transparent;
  }
  .ghost:hover:not(:disabled) {
    @apply bg-cockpit-accent/10;
    box-shadow: 0 0 14px rgba(0, 175, 255, 0.25);
  }
</style>
