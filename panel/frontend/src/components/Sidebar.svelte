<script lang="ts">
  import { page } from '$app/stores';
  import { clsx } from '$lib/utils';
  import {
    LayoutDashboard,
    Network,
    Search,
    Bot,
    Zap,
    Eye,
    BrainCircuit,
    FileText
  } from '@lucide/svelte';

  const links = [
    { href: '/', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/nmap', label: 'Nmap', icon: Network },
    { href: '/recon', label: 'Recon', icon: Search },
    { href: '/hackagent', label: 'HackAgent', icon: Bot },
    { href: '/autopentestx', label: 'AutoPentestX', icon: Zap },
    { href: '/inspector', label: 'Inspector', icon: Eye },
    { href: '/ai', label: 'AI Assistant', icon: BrainCircuit },
    { href: '/reports', label: 'Raporty', icon: FileText }
  ];
</script>

<nav class="sidebar" aria-label="Główna nawigacja">
  <div class="logo">
    <span class="logo-accent glow-text">PENTEST</span>
    <span class="logo-text">COCKPIT</span>
  </div>

  <div class="nav-section">
    <span class="nav-label">MENU</span>
    <ul class="nav-list">
      {#each links as { href, label, icon }}
        <li class="nav-item">
          <a
            {href}
            class={clsx(
              'nav-link',
              $page.url.pathname === href && 'nav-link-active'
            )}
          >
            <span class="nav-icon">
              <svelte:component this={icon} size={18} />
            </span>
            {label}
          </a>
        </li>
      {/each}
    </ul>
  </div>

  <div class="sidebar-glow"></div>
</nav>

<style>
  .sidebar {
    @apply relative w-64 h-screen shrink-0 p-6 flex flex-col gap-8 overflow-hidden;
    background: linear-gradient(180deg, rgba(10, 10, 15, 0.95) 0%, rgba(17, 17, 24, 0.92) 100%);
    border-right: 1px solid rgba(0, 175, 255, 0.22);
    box-shadow: 4px 0 24px rgba(0, 175, 255, 0.08);
  }
  .logo {
    @apply relative font-display text-2xl font-black leading-none tracking-wider;
  }
  .logo-accent {
    @apply text-cockpit-accent block;
  }
  .logo-text {
    @apply text-cockpit-text tracking-widest;
  }
  .nav-section {
    @apply flex flex-col gap-3;
  }
  .nav-label {
    @apply text-xs font-bold text-cockpit-muted/60 tracking-[0.2em] px-4;
  }
  .nav-list {
    @apply flex flex-col gap-1;
  }
  .nav-link {
    @apply flex items-center gap-3 px-4 py-3 rounded-lg text-cockpit-muted text-sm font-semibold transition-all duration-300;
  }
  .nav-link:hover {
    @apply text-cockpit-accent bg-cockpit-accent/10;
    box-shadow: 0 0 14px rgba(0, 175, 255, 0.12);
  }
  .nav-icon {
    @apply text-cockpit-muted transition-colors;
  }
  .nav-link:hover .nav-icon {
    @apply text-cockpit-accent;
  }
  .nav-link-active {
    @apply text-cockpit-accent bg-cockpit-accent/10;
    border-left: 3px solid var(--cockpit-accent);
    box-shadow:
      0 0 14px rgba(0, 175, 255, 0.18),
      inset 0 1px 0 rgba(255, 255, 255, 0.05);
  }
  .nav-link-active .nav-icon {
    @apply text-cockpit-accent;
    filter: drop-shadow(0 0 6px var(--cockpit-accent-glow));
  }
  .sidebar-glow {
    @apply absolute -right-24 top-1/4 w-48 h-48 rounded-full pointer-events-none;
    background: radial-gradient(circle, rgba(0, 175, 255, 0.12) 0%, transparent 70%);
    filter: blur(40px);
  }
</style>
