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
    @apply flex-1 flex flex-col overflow-hidden;
  }
  main {
    @apply flex-1 overflow-y-auto;
  }
</style>
