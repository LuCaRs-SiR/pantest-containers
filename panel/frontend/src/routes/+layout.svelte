<script lang="ts">
  import Sidebar from '../components/Sidebar.svelte';
  import Topbar from '../components/Topbar.svelte';
  import '../app.css';
</script>

<div class="layout">
  <Sidebar />
  <div class="content">
    <Topbar />
    <main class="p-6 cockpit-scrollbar">
      <slot />
    </main>
  </div>
</div>

<style>
  .layout {
    @apply flex h-screen bg-cockpit-bg text-cockpit-text overflow-hidden;
  }
  .content {
    @apply flex-1 flex flex-col overflow-hidden relative;
  }
  .content::before {
    content: '';
    @apply absolute inset-0 pointer-events-none;
    background:
      radial-gradient(circle at 20% 30%, rgba(0, 175, 255, 0.06) 0%, transparent 40%),
      radial-gradient(circle at 80% 70%, rgba(255, 0, 160, 0.06) 0%, transparent 40%);
  }
  main {
    @apply flex-1 overflow-y-auto relative z-10;
  }
</style>
