import { writable } from 'svelte/store'

function createWebSocketStore() {
  const { subscribe, set, update } = writable({
    connected: false,
    stats: null,
    tamagotchi: null
  })

  let ws = null
  let reconnectTimeout = null
  const RECONNECT_DELAY = 3000 // 3 seconds

  function connect() {
    // Determine WebSocket URL
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const wsUrl = `${protocol}//${host}/ws`

    console.log('Connecting to WebSocket:', wsUrl)

    try {
      ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log('✓ WebSocket connected')
        update(store => ({ ...store, connected: true }))
        
        // Clear any pending reconnection
        if (reconnectTimeout) {
          clearTimeout(reconnectTimeout)
          reconnectTimeout = null
        }
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          
          if (data.type === 'stats_update') {
            update(store => ({
              ...store,
              stats: data.stats,
              tamagotchi: data.tamagotchi
            }))
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      ws.onclose = () => {
        console.log('✗ WebSocket disconnected')
        update(store => ({ ...store, connected: false }))
        
        // Attempt to reconnect
        reconnectTimeout = setTimeout(() => {
          console.log('Attempting to reconnect...')
          connect()
        }, RECONNECT_DELAY)
      }
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
      
      // Attempt to reconnect
      reconnectTimeout = setTimeout(() => {
        console.log('Attempting to reconnect...')
        connect()
      }, RECONNECT_DELAY)
    }
  }

  function disconnect() {
    if (ws) {
      ws.close()
      ws = null
    }
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
      reconnectTimeout = null
    }
  }

  function send(message) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket not connected')
    }
  }

  // Auto-connect on store creation
  connect()

  return {
    subscribe,
    send,
    disconnect,
    reconnect: connect
  }
}

export const websocketStore = createWebSocketStore()
