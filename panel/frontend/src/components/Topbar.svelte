<script lang="ts">
  let status = 'ONLINE';
  let ai = 'ACTIVE';
  let gpu = 'RTX 5070';
</script>

<header class="topbar">
  <div class="flex items-center gap-2">
    <span class="status-dot" aria-hidden="true"></span>
    <span class="label">System status:</span>
    <span class="value online glow-text">{status}</span>
  </div>
  <div class="flex items-center gap-2">
    <span class="label">AI:</span>
    <span class="value active glow-text">{ai}</span>
  </div>
  <div class="flex items-center gap-2">
    <span class="label">GPU:</span>
    <span class="value gpu glow-text-pink">{gpu}</span>
  </div>
</header>

<style>
  .topbar {
    @apply flex justify-between items-center px-6 py-4 bg-cockpit-panel border-b border-cockpit-accent/20 mb-6 text-sm;
  }
  .label {
    @apply text-cockpit-muted;
  }
  .value {
    @apply font-bold;
  }
  .online {
    @apply text-cockpit-terminal-green;
  }
  .active {
    @apply text-cockpit-accent;
  }
  .gpu {
    @apply text-cockpit-pink;
  }
  .status-dot {
    @apply w-2.5 h-2.5 rounded-full bg-cockpit-terminal-green shadow-glow-green;
  }
</style>
