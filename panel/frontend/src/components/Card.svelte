<script lang="ts">
  let { title, link, description = '' }: { title: string; link: string; description?: string } = $props();
</script>

<a href={link} class="card">
  <h2 class="card-title">{title}</h2>
  {#if description}
    <p class="card-desc">{description}</p>
  {/if}
</a>

<style>
  .card {
    @apply block p-6 bg-cockpit-panel rounded-xl border border-white/5 transition-all hover:border-cockpit-accent/50 hover:shadow-[0_0_15px_rgba(0,175,255,0.15)] hover:-translate-y-1;
  }
  .card-title {
    @apply text-xl font-bold text-cockpit-accent mb-2;
  }
  .card-desc {
    @apply text-sm text-cockpit-muted;
  }
</style>
