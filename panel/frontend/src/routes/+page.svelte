<script lang="ts">
  import Card from '../components/Card.svelte';

  const tools = [
    { title: 'Nmap', link: '/nmap', desc: 'Skanowanie sieci i portów' },
    { title: 'Recon', link: '/recon', desc: 'Rekonfiguracja powierzchni ataku' },
    { title: 'HackAgent', link: '/hackagent', desc: 'Agent AI do pentestu' },
    { title: 'AutoPentestX', link: '/autopentestx', desc: 'Automatyczny pentest' },
    { title: 'Inspector', link: '/inspector', desc: 'Inspekcja i szczegóły' },
    { title: 'AI Assistant', link: '/ai', desc: 'Chat z lokalnym modelem' },
    { title: 'Raporty', link: '/reports', desc: 'Generowanie raportów' }
  ];
</script>

<h1 class="text-3xl font-black text-cockpit-accent mb-6">Dashboard</h1>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
  {#each tools as tool}
    <Card title={tool.title} link={tool.link} description={tool.desc} />
  {/each}
</div>
