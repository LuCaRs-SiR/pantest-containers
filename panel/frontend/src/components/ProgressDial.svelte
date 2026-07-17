<script lang="ts">
  let { value = 90, label = 'Progres Zadania' }: { value?: number; label?: string } = $props();

  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const offset = $derived(circumference - (value / 100) * circumference);
</script>

<div class="dial neon-card glass">
  <h3 class="dial-title">{label}</h3>
  <div class="dial-wrapper">
    <svg class="dial-svg" viewBox="0 0 110 110">
      <circle class="dial-bg" cx="55" cy="55" r={radius}></circle>
      <circle class="dial-progress" cx="55" cy="55" r={radius} stroke-dasharray={circumference} stroke-dashoffset={offset}></circle>
    </svg>
    <div class="dial-value">{value}%</div>
  </div>
</div>

<style>
  .dial {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    text-align: center;
  }

  .dial-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
    margin-bottom: 15px;
    color: var(--text-main);
  }

  .dial-wrapper {
    position: relative;
    width: 130px;
    height: 130px;
  }

  .dial-svg {
    width: 100%;
    height: 100%;
    transform: rotate(-90deg);
  }

  .dial-bg {
    fill: none;
    stroke: rgba(255, 255, 255, 0.1);
    stroke-width: 10;
  }

  .dial-progress {
    fill: none;
    stroke: var(--accent-cyan);
    stroke-width: 10;
    stroke-linecap: round;
    filter: drop-shadow(0 0 6px var(--accent-cyan));
    transition: stroke-dashoffset 0.6s ease;
  }

  .dial-value {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 24px;
    font-weight: bold;
    color: var(--accent-cyan);
    text-shadow: 0 0 10px var(--accent-cyan);
  }
</style>
