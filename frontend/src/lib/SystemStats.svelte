<script>
  export let stats = null

  function formatBytes(gb) {
    return gb ? `${gb.toFixed(2)} GB` : '0 GB'
  }

  function getHealthColor(percent) {
    if (percent < 50) return '#4caf50'
    if (percent < 80) return '#ff9800'
    return '#f44336'
  }
</script>

<div class="stats-card">
  <h2>System Metrics</h2>

  {#if stats}
    <div class="metrics">
      <!-- CPU -->
      <div class="metric">
        <div class="metric-header">
          <span class="metric-icon">🖥️</span>
          <span class="metric-label">CPU Usage</span>
        </div>
        <div class="metric-bar">
          <div 
            class="metric-fill" 
            style="width: {stats.cpu_percent}%; background: {getHealthColor(stats.cpu_percent)}"
          ></div>
        </div>
        <div class="metric-value">{stats.cpu_percent}%</div>
      </div>

      <!-- Memory -->
      <div class="metric">
        <div class="metric-header">
          <span class="metric-icon">🧠</span>
          <span class="metric-label">Memory Usage</span>
        </div>
        <div class="metric-bar">
          <div 
            class="metric-fill" 
            style="width: {stats.memory_percent}%; background: {getHealthColor(stats.memory_percent)}"
          ></div>
        </div>
        <div class="metric-value">
          {stats.memory_percent}% ({formatBytes(stats.memory_used_gb)} / {formatBytes(stats.memory_total_gb)})
        </div>
      </div>

      <!-- Disk -->
      <div class="metric">
        <div class="metric-header">
          <span class="metric-icon">💾</span>
          <span class="metric-label">Disk Usage</span>
        </div>
        <div class="metric-bar">
          <div 
            class="metric-fill" 
            style="width: {stats.disk_percent}%; background: {getHealthColor(stats.disk_percent)}"
          ></div>
        </div>
        <div class="metric-value">
          {stats.disk_percent}% ({formatBytes(stats.disk_used_gb)} / {formatBytes(stats.disk_total_gb)})
        </div>
      </div>

      <!-- Docker -->
      <div class="metric docker">
        <div class="metric-header">
          <span class="metric-icon">🐳</span>
          <span class="metric-label">Docker Containers</span>
        </div>
        <div class="docker-stats">
          <div class="docker-stat">
            <span class="docker-count">{stats.docker_containers_total}</span>
            <span class="docker-label">Total</span>
          </div>
          <div class="docker-stat">
            <span class="docker-count running">{stats.docker_containers_running}</span>
            <span class="docker-label">Running</span>
          </div>
          <div class="docker-stat">
            <span class="docker-count stopped">{stats.docker_containers_stopped}</span>
            <span class="docker-label">Stopped</span>
          </div>
        </div>
      </div>

      <!-- Timestamp -->
      {#if stats.timestamp}
        <div class="timestamp">
          Last update: {new Date(stats.timestamp).toLocaleTimeString()}
        </div>
      {/if}
    </div>
  {:else}
    <div class="loading">
      <p>Loading system metrics...</p>
    </div>
  {/if}
</div>

<style>
  .stats-card {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: #333;
  }

  .metrics {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .metric {
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }

  .metric-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
  }

  .metric-icon {
    font-size: 1.5rem;
  }

  .metric-label {
    font-size: 1rem;
    font-weight: 600;
    color: #333;
  }

  .metric-bar {
    height: 20px;
    background: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 8px;
  }

  .metric-fill {
    height: 100%;
    transition: width 0.5s ease;
    border-radius: 10px;
  }

  .metric-value {
    font-size: 0.9rem;
    color: #666;
    text-align: right;
  }

  .metric.docker {
    background: #e3f2fd;
  }

  .docker-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 10px;
  }

  .docker-stat {
    text-align: center;
    padding: 10px;
    background: white;
    border-radius: 8px;
  }

  .docker-count {
    display: block;
    font-size: 1.8rem;
    font-weight: bold;
    color: #333;
  }

  .docker-count.running {
    color: #4caf50;
  }

  .docker-count.stopped {
    color: #f44336;
  }

  .docker-label {
    display: block;
    font-size: 0.85rem;
    color: #666;
    margin-top: 5px;
  }

  .timestamp {
    text-align: center;
    font-size: 0.85rem;
    color: #666;
    margin-top: 10px;
    font-style: italic;
  }

  .loading {
    text-align: center;
    padding: 40px;
    color: #666;
  }
</style>
