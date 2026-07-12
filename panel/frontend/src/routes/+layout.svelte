<script>
  import Sidebar from '../components/Sidebar.svelte';
  import Topbar from '../components/Topbar.svelte';
  import '../app.css';
</script>

<div class="layout">
  <Sidebar />
  <div class="content">
    <Topbar />
    <slot />
  </div>
</div>

<style>
  .layout {
    display: flex;
    height: 100vh;
    background: var(--bg-dark);
  }
  .content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: radial-gradient(circle at top left, #0A0A0F 0%, #111118 100%);
  }
</style>
