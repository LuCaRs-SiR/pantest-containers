<script lang="ts">
  import { page } from '$app/stores';
  import { clsx } from '$lib/utils';
  import {
    LayoutDashboard,
    CheckSquare,
    Database,
    Users,
    CalendarDays,
    BrainCircuit,
    Bug,
    BarChart3
  } from '@lucide/svelte';

  const links = [
    { href: '/', label: 'Główny Pulpit', icon: LayoutDashboard },
    { href: '/tasks', label: 'Zadania', icon: CheckSquare },
    { href: '/resources', label: 'Zasoby', icon: Database },
    { href: '/team', label: 'Zespół Projektowy', icon: Users },
    { href: '/timeline', label: 'Oś Czasu (Gantt)', icon: CalendarDays },
    { href: '/ai', label: 'Narzędzia AI', icon: BrainCircuit },
    { href: '/issues', label: 'Zgłoszenia (Błędy)', icon: Bug },
    { href: '/reports', label: 'Analiza i Raporty', icon: BarChart3 }
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
