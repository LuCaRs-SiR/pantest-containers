<script lang="ts">
  const tools = [
    {
      href: '/nmap',
      title: 'Nmap',
      subtitle: 'Skanowanie hostow i portow',
      sample: 'nmap -sV 192.168.1.10'
    },
    {
      href: '/recon',
      title: 'Recon',
      subtitle: 'Enumeracja domen i subdomen',
      sample: 'subfinder -d example.com'
    },
    {
      href: '/hackagent',
      title: 'HackAgent',
      subtitle: 'Asystent scenariuszy testowych',
      sample: 'hackagent --help'
    },
    {
      href: '/autopentestx',
      title: 'AutoPentestX',
      subtitle: 'Automatyzacja workflow pentest',
      sample: 'python3 /app/main.py --version'
    },
    {
      href: '/inspector',
      title: 'Inspector',
      subtitle: 'Moduly inspekcji i raportowania',
      sample: 'python3 /app/core/inspector.py -h'
    },
    {
      href: '/burp',
      title: 'Burp',
      subtitle: 'Proxy i analiza ruchu HTTP',
      sample: 'echo burp-ok'
    },
    {
      href: '/kali',
      title: 'Kali Tools',
      subtitle: 'Shell narzedzi Kali Linux',
      sample: 'nmap --help'
    },
    {
      href: '/ai',
      title: 'AI Gateway',
      subtitle: 'Interakcja z modelem lokalnym',
      sample: 'prompt -> qwen2.5'
    }
  ];
</script>

<h1 class="neon-text chromatic fade-in">PANEL NARZEDZI PENTEST</h1>

<p class="intro fade-in">
  Wszystkie narzedzia sa dostepne ponizej jako szybkie kafelki. Kliknij wybrane
  narzedzie, aby przejsc do uruchamiania komend i testow.
</p>

<div class="tools-grid fade-in">
  {#each tools as tool}
    <a class="tool-card glass neon-border" href={tool.href}>
      <h2>{tool.title}</h2>
      <p class="subtitle">{tool.subtitle}</p>
      <p class="sample">{tool.sample}</p>
    </a>
  {/each}
</div>

<style>
  h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 26px;
    margin-bottom: 10px;
  }

  .intro {
    color: var(--text-secondary);
    margin-bottom: 20px;
    max-width: 900px;
    line-height: 1.4;
  }

  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 14px;
  }

  .tool-card {
    padding: 18px;
    border-radius: 12px;
    text-decoration: none;
    color: var(--text-main);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .tool-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
  }

  .tool-card h2 {
    margin: 0 0 8px;
    font-size: 18px;
    font-family: 'Orbitron', sans-serif;
    color: var(--accent-cyan);
  }

  .subtitle {
    margin: 0 0 10px;
    color: var(--text-main);
    font-size: 14px;
  }

  .sample {
    margin: 0;
    font-family: monospace;
    font-size: 12px;
    color: var(--text-secondary);
    opacity: 0.85;
    word-break: break-word;
  }

  @media (max-width: 1200px) {
    .tools-grid {
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    }
  }
</style>
