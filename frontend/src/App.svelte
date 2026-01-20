<script>
  import Tamagotchi from './lib/Tamagotchi.svelte'
  import SystemStats from './lib/SystemStats.svelte'
  import { websocketStore } from './stores/websocket.js'

  const { connected, stats, tamagotchi } = websocketStore
</script>

<main>
  <div class="container">
    <header>
      <h1>🖥️ SysMon</h1>
      <p class="subtitle">Server Tamagotchi</p>
      {#if $connected}
        <span class="status connected">● Connected</span>
      {:else}
        <span class="status disconnected">● Disconnected</span>
      {/if}
    </header>

    <div class="content">
      <Tamagotchi tamagotchi={$tamagotchi} />
      <SystemStats stats={$stats} />
    </div>
  </div>
</main>

<style>
  main {
    width: 100%;
    max-width: 1200px;
  }

  .container {
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }

  header {
    text-align: center;
    margin-bottom: 40px;
    position: relative;
  }

  h1 {
    font-size: 3rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
  }

  .subtitle {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 10px;
  }

  .status {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
  }

  .status.connected {
    background: #d4edda;
    color: #155724;
  }

  .status.disconnected {
    background: #f8d7da;
    color: #721c24;
  }

  .content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
  }

  @media (max-width: 768px) {
    .content {
      grid-template-columns: 1fr;
    }

    h1 {
      font-size: 2rem;
    }
  }
</style>
