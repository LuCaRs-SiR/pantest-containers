<script lang="ts">
  import type { Component } from 'svelte';
  import Button from './Button.svelte';

  let {
    title,
    description,
    icon,
    variant = 'accent',
    onstart
  }: {
    title: string;
    description: string;
    icon: Component;
    variant?: 'accent' | 'pink';
    onstart?: () => void;
  } = $props();

  const variantClass = variant === 'pink' ? 'panel-pink' : 'panel-accent';
</script>

<div class="dashboard-panel glow-card {variantClass}">
  <div class="flex items-start justify-between">
    <div>
      <h2 class="panel-title">{title}</h2>
      <p class="panel-desc">{description}</p>
    </div>
    <div class="panel-icon">
      <svelte:component this={icon} size={32} />
    </div>
  </div>
  <div class="mt-4">
    <Button variant="primary" onclick={onstart}>Start</Button>
  </div>
</div>

<style>
  .dashboard-panel {
    @apply p-6 flex flex-col justify-between min-h-[180px];
  }
  .panel-title {
    @apply text-xl font-black text-cockpit-text mb-1;
  }
  .panel-desc {
    @apply text-sm text-cockpit-muted;
  }
  .panel-icon {
    @apply p-3 rounded-lg bg-cockpit-panel-light text-cockpit-accent;
  }
  .panel-accent:hover .panel-icon {
    @apply text-cockpit-accent shadow-glow-accent;
  }
  .panel-pink .panel-icon {
    @apply text-cockpit-pink;
  }
  .panel-pink:hover .panel-icon {
    @apply shadow-glow-pink;
  }
  .panel-pink:hover {
    @apply border-cockpit-pink/40 shadow-glow-pink;
  }
</style>
