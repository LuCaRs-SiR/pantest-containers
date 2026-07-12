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
    <span class="text-cockpit-accent glow-text">PENTEST</span>
    <span>COCKPIT</span>
  </div>

  <ul class="flex flex-col gap-1">
    {#each links as { href, label, icon }}
      <li>
        <a
          {href}
          class={clsx(
            'nav-link',
            $page.url.pathname === href && 'nav-link-active'
          )}
        >
          <svelte:component this={icon} size={18} />
          {label}
        </a>
      </li>
    {/each}
  </ul>
</nav>

<style>
  .sidebar {
    @apply w-64 bg-cockpit-panel p-5 flex flex-col gap-6 h-screen shrink-0 border-r border-cockpit-accent/20;
  }
  .logo {
    @apply text-2xl font-black leading-none tracking-tight text-cockpit-text;
  }
  .logo span:first-child {
    @apply text-cockpit-accent;
  }
  .nav-link {
    @apply flex items-center gap-3 text-cockpit-muted text-sm font-medium py-3 px-4 rounded-xl transition-all hover:text-cockpit-accent hover:bg-cockpit-accent/10;
  }
  .nav-link-active {
    @apply text-cockpit-accent bg-cockpit-accent/10 border-l-4 border-cockpit-accent shadow-glow-accent;
  }
</style>
