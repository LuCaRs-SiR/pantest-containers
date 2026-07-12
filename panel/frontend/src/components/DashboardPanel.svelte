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

  const Icon = $derived(icon);
</script>

<div class="dashboard-panel glow-card {variant === 'pink' ? 'panel-pink' : 'panel-accent'} animate-fade-in-up">
  <div class="flex items-start justify-between">
    <div class="flex-1">
      <h2 class="panel-title font-display">{title}</h2>
      <p class="panel-desc">{description}</p>
    </div>
    <div class="panel-icon {variant === 'pink' ? 'icon-glow-pink' : 'icon-glow'}">
      <Icon size={32} />
    </div>
  </div>
  <div class="mt-5">
    <Button variant="primary" onclick={onstart}>Start</Button>
  </div>
</div>

<style>
  .dashboard-panel {
    @apply relative p-6 flex flex-col justify-between min-h-[180px] overflow-hidden;
  }
  .panel-title {
    @apply text-xl font-black text-cockpit-text mb-1 tracking-wide;
  }
  .panel-desc {
    @apply text-sm text-cockpit-muted;
  }
  .panel-icon {
    @apply p-3 rounded-lg bg-cockpit-panel-light/70 text-cockpit-accent border border-white/10;
  }
  .icon-glow {
    filter: drop-shadow(0 0 8px var(--cockpit-accent-glow));
  }
  .icon-glow-pink {
    @apply text-cockpit-pink;
    filter: drop-shadow(0 0 8px var(--cockpit-pink-glow));
  }
  .panel-pink:hover {
    border-color: rgba(255, 0, 160, 0.55);
    box-shadow:
      0 0 0 1px rgba(0, 0, 0, 0.35),
      0 8px 32px rgba(255, 0, 160, 0.18),
      inset 0 1px 0 rgba(255, 255, 255, 0.08);
  }
  .panel-pink:hover .panel-icon {
    @apply border-cockpit-pink/40;
    box-shadow: 0 0 14px rgba(255, 0, 160, 0.25);
  }
</style>
