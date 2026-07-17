<script lang="ts">
  import { page } from '$app/stores';
  import { clsx } from '$lib/utils';
  import {
    LayoutDashboard,
    Shield,
    Search,
    Bot,
    WandSparkles,
    Phone,
    AppWindow,
    Terminal,
    BrainCircuit,
    BarChart3
  } from '@lucide/svelte';

  const links = [
    { href: '/', label: 'Pulpit', icon: LayoutDashboard },
    { href: '/nmap', label: 'Nmap', icon: Shield },
    { href: '/recon', label: 'Recon', icon: Search },
    { href: '/hackagent', label: 'HackAgent', icon: Bot },
    { href: '/autopentestx', label: 'AutoPentestX', icon: WandSparkles },
    { href: '/inspector', label: 'Inspector', icon: Phone },
    { href: '/burp', label: 'Burp', icon: AppWindow },
    { href: '/kali', label: 'Kali Tools', icon: Terminal },
    { href: '/ai', label: 'AI Gateway', icon: BrainCircuit },
    { href: '/reports', label: 'Status i Raporty', icon: BarChart3 }
  ];
</script>

<nav class="sidebar neon-border glass">
  <h1 class="logo neon-text chromatic">PULPIT<br>ZARZĄDZANIA<br>PROJEKTEM</h1>

  {#each links as { href, label, icon }}
    <a
      {href}
      class={clsx('nav-link', $page.url.pathname === href && 'nav-link-active')}
    >
      <span class="nav-icon">
        <svelte:component this={icon} size={18} />
      </span>
      {label}
    </a>
  {/each}
</nav>

<style>
  .sidebar {
    width: 280px;
    height: 100vh;
    padding: 25px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    box-sizing: border-box;
  }

  .logo {
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 25px;
    line-height: 1.1;
    font-family: 'Orbitron', sans-serif;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-main);
    font-size: 15px;
    padding: 12px;
    border-radius: 8px;
    transition: 0.2s;
    font-family: 'Orbitron', sans-serif;
  }

  .nav-link:hover {
    color: var(--accent-cyan);
    text-shadow: 0 0 10px var(--accent-cyan);
    transform: translateX(5px);
    background: rgba(0, 229, 255, 0.05);
  }

  .nav-link-active {
    color: var(--accent-cyan);
    background: rgba(0, 229, 255, 0.1);
    border-left: 3px solid var(--accent-cyan);
  }

  .nav-icon {
    display: flex;
    align-items: center;
    color: var(--accent-cyan);
    filter: drop-shadow(0 0 4px var(--accent-cyan));
  }
</style>
