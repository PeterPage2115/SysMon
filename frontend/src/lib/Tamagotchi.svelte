<script>
  export let tamagotchi = null

  // Determine creature state based on health
  $: state = getCreatureState(tamagotchi?.health || 100)
  $: emoji = getEmoji(state)
  $: statusColor = getStatusColor(state)

  function getCreatureState(health) {
    if (health >= 80) return 'happy'
    if (health >= 50) return 'neutral'
    if (health >= 20) return 'stressed'
    return 'critical'
  }

  function getEmoji(state) {
    const emojis = {
      happy: '😊',
      neutral: '😐',
      stressed: '😰',
      critical: '🤒'
    }
    return emojis[state] || '😊'
  }

  function getStatusColor(state) {
    const colors = {
      happy: '#4caf50',
      neutral: '#ff9800',
      stressed: '#ff5722',
      critical: '#f44336'
    }
    return colors[state] || '#4caf50'
  }

  async function feedTamagotchi() {
    try {
      const response = await fetch('/api/tamagotchi/feed', { method: 'POST' })
      const data = await response.json()
      console.log('Fed tamagotchi:', data)
    } catch (error) {
      console.error('Error feeding tamagotchi:', error)
    }
  }

  async function renameTamagotchi() {
    const name = prompt('Enter new name:', tamagotchi?.name || 'Server-chan')
    if (name && name.trim()) {
      try {
        const response = await fetch(`/api/tamagotchi/rename?name=${encodeURIComponent(name)}`, {
          method: 'POST'
        })
        const data = await response.json()
        console.log('Renamed tamagotchi:', data)
      } catch (error) {
        console.error('Error renaming tamagotchi:', error)
      }
    }
  }
</script>

<div class="tamagotchi-card">
  <h2>Your Server Pet</h2>
  
  {#if tamagotchi}
    <div class="creature" style="--status-color: {statusColor}">
      <div class="creature-display">
        <span class="creature-emoji">{emoji}</span>
      </div>
      
      <div class="creature-info">
        <h3 class="creature-name" on:click={renameTamagotchi}>
          {tamagotchi.name}
        </h3>
        <p class="creature-level">Level {tamagotchi.level}</p>
      </div>

      <div class="stats">
        <div class="stat-bar">
          <label>Health</label>
          <div class="bar">
            <div class="fill" style="width: {tamagotchi.health}%; background: {statusColor}"></div>
          </div>
          <span class="value">{Math.round(tamagotchi.health)}%</span>
        </div>

        <div class="stat-bar">
          <label>Happiness</label>
          <div class="bar">
            <div class="fill" style="width: {tamagotchi.happiness}%; background: #ffd700"></div>
          </div>
          <span class="value">{Math.round(tamagotchi.happiness)}%</span>
        </div>

        <div class="stat-bar">
          <label>XP</label>
          <div class="bar">
            <div class="fill" style="width: {(tamagotchi.xp / (tamagotchi.level * 100)) * 100}%; background: #2196f3"></div>
          </div>
          <span class="value">{tamagotchi.xp} / {tamagotchi.level * 100}</span>
        </div>
      </div>

      <button class="feed-button" on:click={feedTamagotchi}>
        🍕 Feed (+10 XP)
      </button>
    </div>
  {:else}
    <div class="loading">
      <p>Connecting to your server pet...</p>
    </div>
  {/if}
</div>

<style>
  .tamagotchi-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: #333;
  }

  .creature {
    text-align: center;
  }

  .creature-display {
    width: 200px;
    height: 200px;
    margin: 0 auto 20px;
    background: white;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    border: 5px solid var(--status-color);
    transition: all 0.3s ease;
  }

  .creature-emoji {
    font-size: 6rem;
    animation: bounce 2s ease-in-out infinite;
  }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }

  .creature-info {
    margin-bottom: 20px;
  }

  .creature-name {
    font-size: 1.8rem;
    color: #333;
    margin-bottom: 5px;
    cursor: pointer;
    transition: color 0.2s;
  }

  .creature-name:hover {
    color: #667eea;
  }

  .creature-level {
    font-size: 1rem;
    color: #666;
    font-weight: 600;
  }

  .stats {
    margin: 20px 0;
  }

  .stat-bar {
    margin-bottom: 15px;
  }

  .stat-bar label {
    display: block;
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 5px;
    font-weight: 600;
  }

  .bar {
    height: 20px;
    background: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
  }

  .fill {
    height: 100%;
    transition: width 0.5s ease;
    border-radius: 10px;
  }

  .value {
    display: block;
    text-align: right;
    font-size: 0.85rem;
    color: #666;
    margin-top: 3px;
  }

  .feed-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 25px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-top: 10px;
  }

  .feed-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
  }

  .feed-button:active {
    transform: translateY(0);
  }

  .loading {
    text-align: center;
    padding: 40px;
    color: #666;
  }
</style>
