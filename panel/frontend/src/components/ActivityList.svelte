<script lang="ts">
  let {
    activities = []
  }: {
    activities?: { time: string; message: string; type?: 'info' | 'success' | 'warning' }[];
  } = $props();

  const dotColor = (type: string | undefined) => {
    switch (type) {
      case 'success': return 'dot-success';
      case 'warning': return 'dot-warning';
      default: return 'dot-info';
    }
  };
</script>

<div class="activity-list glow-card">
  <div class="header">
    <div class="header-line header-line-pink"></div>
    <h3 class="section-title font-display">Recent Activity</h3>
  </div>
  <ul class="flex flex-col gap-3 mt-3">
    {#each activities as activity}
      <li class="activity-item">
        <span class="activity-dot {dotColor(activity.type)}"></span>
        <div class="flex-1">
          <p class="activity-message">{activity.message}</p>
          <p class="activity-time">{activity.time}</p>
        </div>
      </li>
    {/each}
  </ul>
</div>

<style>
  .activity-list {
    @apply p-4 h-full;
  }
  .header {
    @apply flex items-center gap-3 mb-3;
  }
  .header-line {
    @apply w-1 h-5 rounded-full;
  }
  .header-line-pink {
    @apply bg-cockpit-pink;
    box-shadow: 0 0 8px var(--cockpit-pink-glow);
  }
  .section-title {
    @apply text-lg font-bold text-cockpit-text tracking-wide;
  }
  .activity-item {
    @apply flex items-start gap-3 text-sm p-2 rounded-lg transition-colors;
  }
  .activity-item:hover {
    background: rgba(255, 255, 255, 0.03);
  }
  .activity-dot {
    @apply w-2 h-2 rounded-full mt-1.5;
  }
  .dot-info {
    @apply bg-cockpit-accent;
    box-shadow: 0 0 6px var(--cockpit-accent-glow);
  }
  .dot-success {
    @apply bg-cockpit-terminal-green;
    box-shadow: 0 0 6px var(--cockpit-terminal-green);
  }
  .dot-warning {
    @apply bg-cockpit-pink;
    box-shadow: 0 0 6px var(--cockpit-pink-glow);
  }
  .activity-message {
    @apply text-cockpit-text;
  }
  .activity-time {
    @apply text-cockpit-muted text-xs mt-0.5;
  }
</style>
