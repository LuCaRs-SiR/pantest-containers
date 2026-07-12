<script lang="ts">
  let {
    activities = []
  }: {
    activities?: { time: string; message: string; type?: 'info' | 'success' | 'warning' }[];
  } = $props();

  const dotColor = (type: string | undefined) => {
    switch (type) {
      case 'success': return 'bg-cockpit-terminal-green';
      case 'warning': return 'bg-cockpit-pink';
      default: return 'bg-cockpit-accent';
    }
  };
</script>

<div class="activity-list glow-card">
  <h3 class="section-title">Recent Activity</h3>
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
  .section-title {
    @apply text-lg font-bold text-cockpit-text;
  }
  .activity-item {
    @apply flex items-start gap-3 text-sm;
  }
  .activity-dot {
    @apply w-2 h-2 rounded-full mt-1.5;
  }
  .activity-message {
    @apply text-cockpit-text;
  }
  .activity-time {
    @apply text-cockpit-muted text-xs mt-0.5;
  }
</style>
