class WebSocketManager {
    constructor(endpoint) {
        this.endpoint = endpoint;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnects = CONFIG.APP.TIMING.WS_MAX_RECONNECTS;
        this.reconnectDelay = CONFIG.APP.TIMING.WS_RECONNECT_DELAY;
        this.handlers = {};
        this.isConnecting = false;
    }

    connect(token = null) {
        if (this.isConnecting || (this.ws && this.ws.readyState === WebSocket.OPEN)) return;
        this.isConnecting = true;

        const url = getWsUrl(this.endpoint, token || Auth.getToken());
        this.ws = new WebSocket(url);

        this.ws.onopen = () => {
            this.isConnecting = false;
            this.reconnectAttempts = 0;
            this.emit('connected');
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.emit('message', data);
                if (data.type) this.emit(data.type, data);
            } catch {
                this.emit('message', event.data);
            }
        };

        this.ws.onclose = (event) => {
            this.isConnecting = false;
            this.emit('disconnected', event);
            if (!event.wasClean && this.reconnectAttempts < this.maxReconnects) {
                this.reconnectAttempts++;
                setTimeout(() => this.connect(token), this.reconnectDelay);
            }
        };

        this.ws.onerror = (error) => {
            this.isConnecting = false;
            this.emit('error', error);
        };
    }

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(typeof data === 'string' ? data : JSON.stringify(data));
            return true;
        }
        return false;
    }

    on(event, callback) {
        if (!this.handlers[event]) this.handlers[event] = [];
        this.handlers[event].push(callback);
    }

    off(event, callback) {
        if (!this.handlers[event]) return;
        this.handlers[event] = this.handlers[event].filter(cb => cb !== callback);
    }

    emit(event, data = null) {
        if (this.handlers[event]) {
            this.handlers[event].forEach(cb => cb(data));
        }
    }

    disconnect() {
        this.maxReconnects = 0;
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }

    get isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }
}