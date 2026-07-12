<script lang="ts">
  let status = 'OK';
  let ai = 'Online';
  let gpu = 'RTX 5070';
</script>

<header class="topbar">
  <div class="flex items-center gap-2">
    <span class="status-dot" aria-hidden="true"></span>
    <span>System status: <span class="text-cockpit-text">{status}</span></span>
  </div>
  <span>AI: <span class="text-cockpit-terminal-green">{ai}</span></span>
  <span>GPU: <span class="text-cockpit-accent">{gpu}</span></span>
</header>

<style>
  .topbar {
    @apply flex justify-between items-center px-5 py-3 bg-cockpit-panel border-b border-white/10 mb-6 text-sm text-cockpit-muted;
  }
  .status-dot {
    @apply w-2 h-2 rounded-full bg-cockpit-terminal-green shadow-[0_0_8px_#00FF7F];
  }
</style>
