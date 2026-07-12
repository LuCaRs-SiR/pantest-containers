<script lang="ts">
  let status = 'ONLINE';
  let ai = 'ACTIVE';
  let gpu = 'RTX 5070';
</script>

<header class="topbar">
  <div class="status-group">
    <span class="status-dot" aria-hidden="true"></span>
    <span class="label">System status:</span>
    <span class="value online glow-text">{status}</span>
  </div>
  <div class="status-group">
    <span class="pulse-ring" aria-hidden="true"></span>
    <span class="label">AI:</span>
    <span class="value active glow-text">{ai}</span>
  </div>
  <div class="status-group">
    <span class="label">GPU:</span>
    <span class="value gpu glow-text-pink">{gpu}</span>
  </div>
</header>

<style>
  .topbar {
    @apply relative flex justify-between items-center px-6 py-4 text-sm overflow-hidden;
    background: rgba(17, 17, 24, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0, 175, 255, 0.22);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
  }
  .topbar::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cockpit-accent), var(--cockpit-pink), transparent);
  }
  .status-group {
    @apply flex items-center gap-2;
  }
  .label {
    @apply text-cockpit-muted font-medium tracking-wide;
  }
  .value {
    @apply font-bold font-display tracking-wide;
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
    @apply w-2.5 h-2.5 rounded-full bg-cockpit-terminal-green;
    box-shadow: 0 0 10px var(--cockpit-terminal-green);
  }
  .pulse-ring {
    @apply w-2.5 h-2.5 rounded-full border border-cockpit-accent;
    animation: pulse-ring 2s ease-out infinite;
  }

  @keyframes pulse-ring {
    0% { transform: scale(0.8); opacity: 1; box-shadow: 0 0 0 0 rgba(0, 175, 255, 0.5); }
    70% { transform: scale(1.3); opacity: 0; box-shadow: 0 0 0 8px rgba(0, 175, 255, 0); }
    100% { transform: scale(0.8); opacity: 0; }
  }
</style>
