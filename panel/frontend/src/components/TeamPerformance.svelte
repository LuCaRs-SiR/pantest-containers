<script lang="ts">
  let {
    members = []
  }: {
    members?: { name: string; value: number }[];
  } = $props();
</script>

<div class="performance neon-card glass">
  <h3 class="performance-title">Wydajność Zespołu</h3>
  <div class="performance-list">
    {#each members as member}
      <div class="performance-row">
        <span class="performance-name">{member.name}</span>
        <div class="performance-bar">
          <div class="performance-fill" style="width: {member.value}%"></div>
        </div>
        <span class="performance-value">{member.value}%</span>
      </div>
    {/each}
  </div>
</div>

<style>
  .performance {
    padding: 20px;
  }

  .performance-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
    margin-bottom: 15px;
    color: var(--text-main);
  }

  .performance-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .performance-row {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .performance-name {
    width: 100px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 14px;
    color: var(--text-main);
  }

  .performance-bar {
    flex: 1;
    height: 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 5px;
    overflow: hidden;
  }

  .performance-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-magenta));
    border-radius: 5px;
    box-shadow: 0 0 8px var(--accent-cyan);
    transition: width 0.6s ease;
  }

  .performance-value {
    width: 40px;
    text-align: right;
    font-family: 'Orbitron', sans-serif;
    font-size: 12px;
    color: var(--accent-cyan);
  }
</style>
