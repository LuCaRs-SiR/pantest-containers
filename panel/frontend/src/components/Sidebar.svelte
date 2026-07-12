<script lang="ts">
  import { page } from '$app/stores';
  import { clsx } from '$lib/utils';

  const links = [
    { href: '/', label: 'Dashboard' },
    { href: '/nmap', label: 'Nmap' },
    { href: '/recon', label: 'Recon' },
    { href: '/hackagent', label: 'HackAgent' },
    { href: '/autopentestx', label: 'AutoPentestX' },
    { href: '/inspector', label: 'Inspector' },
    { href: '/ai', label: 'AI Assistant' },
    { href: '/reports', label: 'Raporty' }
  ];
</script>

<nav class="sidebar" aria-label="Główna nawigacja">
  <div class="logo">
    <span class="text-cockpit-accent">PENTEST</span>
    <span>COCKPIT</span>
  </div>

  <ul class="flex flex-col gap-2">
    {#each links as { href, label }}
      <li>
        <a
          {href}
          class={clsx(
            'nav-link',
            $page.url.pathname === href && 'nav-link-active'
          )}
        >
          {label}
        </a>
      </li>
    {/each}
  </ul>
</nav>

<style>
  .sidebar {
    @apply w-60 bg-cockpit-panel p-5 flex flex-col gap-6 h-screen shrink-0 border-r border-cockpit-accent/20;
  }
  .logo {
    @apply text-2xl font-black leading-none tracking-tight text-cockpit-text;
  }
  .logo span:first-child {
    @apply text-cockpit-accent;
  }
  .nav-link {
    @apply block text-cockpit-text text-base py-2 px-3 rounded-lg transition-colors hover:text-cockpit-accent hover:bg-cockpit-accent/10;
  }
  .nav-link-active {
    @apply text-cockpit-accent bg-cockpit-accent/10 border-l-4 border-cockpit-accent;
  }
</style>
