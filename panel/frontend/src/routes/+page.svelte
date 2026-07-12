<h1 class="neon-text chromatic fade-in">Dashboard</h1>

<div class="grid fade-in">
  <div class="neon-card glass neon-glow">Nmap Scan</div>
  <div class="neon-card glass">Recon Tools</div>
  <div class="neon-card glass">Web Testing</div>
  <div class="neon-card glass">AI Assistant</div>
  <div class="neon-card glass">Raporty</div>
</div>

<style>
  h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 28px;
    margin-bottom: 25px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
  }

  .neon-card {
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    min-height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }

  @media (max-width: 1024px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 640px) {
    .grid {
      grid-template-columns: 1fr;
    }
  }
</style>
