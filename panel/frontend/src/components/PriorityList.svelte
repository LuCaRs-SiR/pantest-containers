<script lang="ts">
  let {
    title = 'Lista Priorytetów',
    tasks = []
  }: {
    title?: string;
    tasks?: { name: string; priority: 'critical' | 'high' | 'medium' | 'low' }[];
  } = $props();

  const priorityLabel = {
    critical: 'Krytyczne',
    high: 'Wysokie',
    medium: 'Średnie',
    low: 'Niskie'
  };

  const priorityColor = {
    critical: 'critical',
    high: 'high',
    medium: 'medium',
    low: 'low'
  };
</script>

<div class="priority neon-card glass">
  <h3 class="priority-title">{title}</h3>
  <ul class="priority-list">
    {#each tasks as task}
      <li class="priority-item">
        <span class="priority-name">{task.name}</span>
        <span class="priority-badge {priorityColor[task.priority]}">{priorityLabel[task.priority]}</span>
      </li>
    {/each}
  </ul>
  <button class="start-btn">Start / Wznów</button>
</div>

<style>
  .priority {
    display: flex;
    flex-direction: column;
    padding: 20px;
  }

  .priority-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
    margin-bottom: 15px;
    color: var(--text-main);
  }

  .priority-list {
    list-style: none;
    padding: 0;
    margin: 0 0 15px 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .priority-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 14px;
  }

  .priority-name {
    color: var(--text-main);
  }

  .priority-badge {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: bold;
  }

  .critical {
    background: var(--accent-magenta);
    color: black;
  }

  .high {
    background: #ff9900;
    color: black;
  }

  .medium {
    background: var(--accent-cyan);
    color: black;
  }

  .low {
    background: var(--accent-purple);
    color: white;
  }

  .start-btn {
    margin-top: auto;
  }
</style>
