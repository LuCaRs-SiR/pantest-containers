<div class="topbar neon-border glass">
  <div class="status-item">
    <span class="status-label">Postęp Projektu:</span>
    <span class="status-value">75%</span>
    <span class="status-badge cyan">Bieżący</span>
  </div>
  <div class="status-item">
    <span class="status-label">Terminy:</span>
    <span class="status-value green">Zgodne</span>
  </div>
  <div class="status-item">
    <span class="status-label">Status Budżetu:</span>
    <span class="status-value green">Zdrowy</span>
  </div>
</div>

<style>
  .topbar {
    display: flex;
    justify-content: space-between;
    padding: 15px 25px;
    margin-bottom: 20px;
    font-family: 'Orbitron', sans-serif;
    font-size: 14px;
  }

  .status-item {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .status-label {
    color: var(--text-secondary);
  }

  .status-value {
    color: var(--text-main);
    font-weight: bold;
    text-shadow: 0 0 8px var(--accent-cyan);
  }

  .status-value.green {
    color: var(--terminal-green);
    text-shadow: 0 0 8px var(--terminal-green);
  }

  .status-badge {
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: bold;
  }

  .status-badge.cyan {
    color: black;
    background: var(--accent-cyan);
    box-shadow: 0 0 10px var(--accent-cyan);
  }
</style>
