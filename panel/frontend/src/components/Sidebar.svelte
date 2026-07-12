<nav class="sidebar neon-border glass">
  <h1 class="logo neon-text chromatic">PENTEST<br>COCKPIT</h1>

  <a href="/">Dashboard</a>
  <a href="/nmap">Nmap</a>
  <a href="/recon">Recon</a>
  <a href="/hackagent">HackAgent</a>
  <a href="/autopentestx">AutoPentestX</a>
  <a href="/inspector">Inspector</a>
  <a href="/ai">AI Assistant</a>
  <a href="/reports">Raporty</a>
</nav>

<style>
  .sidebar {
    width: 260px;
    height: 100vh;
    padding: 25px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    box-sizing: border-box;
  }

  .logo {
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 20px;
    line-height: 1.1;
  }

  a {
    color: var(--text-main);
    font-size: 18px;
    padding: 10px 0;
    transition: 0.2s;
    font-family: 'Orbitron', sans-serif;
  }

  a:hover {
    color: var(--accent-cyan);
    text-shadow: 0 0 10px var(--accent-cyan);
    transform: translateX(5px);
  }
</style>
