const API = {
    async request(endpoint, options = {}) {
        const url = getApiUrl(endpoint);
        const defaultOptions = {
            headers: Auth.getAuthHeaders(),
        };

        const finalOptions = { ...defaultOptions, ...options };
        if (finalOptions.body && typeof finalOptions.body === 'object') {
            finalOptions.body = JSON.stringify(finalOptions.body);
        }

        try {
            const response = await fetch(url, finalOptions);

            const isAuthPage = window.location.pathname.includes('login.html') || 
                               window.location.pathname.includes('register.html') ||
                               window.location.pathname === '/';

            if (response.status === 401 && !isAuthPage) {
                Auth.clearAll();
                Toast.error('Session expired. Please login again.');
                setTimeout(() => redirectTo(CONFIG.ROUTES.LOGIN), 1000);
                return null;
            }

            let data;
            try {
                data = await response.json();
            } catch {
                data = {};
            }

            if (!response.ok) {
                throw { status: response.status, data };
            }

            return data;
        } catch (error) {
            if (error.status) throw error;
            Toast.error('Network error. Please check your connection.');
            throw error;
        }
    },

    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    post(endpoint, body) {
        return this.request(endpoint, { method: 'POST', body });
    },

    put(endpoint, body) {
        return this.request(endpoint, { method: 'PUT', body });
    },

    patch(endpoint, body) {
        return this.request(endpoint, { method: 'PATCH', body });
    },

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },

    async register(username, email, password) {
        const data = await this.post(CONFIG.ENDPOINTS.REGISTER, { username, email, password });
        if (data && data.access_token) {
            Auth.saveToken(data.access_token);
            if (data.user) Auth.saveUserData(data.user);
        }
        return data;
    },

    async login(email, password) {
        const data = await this.post(CONFIG.ENDPOINTS.LOGIN, { email, password });
        if (data && data.access_token) {
            Auth.saveToken(data.access_token);
            if (data.user) Auth.saveUserData(data.user);
        }
        return data;
    },

    async getMe() {
        return this.get(CONFIG.ENDPOINTS.ME);
    },

    async getProfile() {
        return this.get(CONFIG.ENDPOINTS.PROFILE_GET);
    },

    async updateProfile(profileData) {
        return this.put(CONFIG.ENDPOINTS.PROFILE_UPDATE, profileData);
    },

    async endCall(roomId) {
        return this.post(`${CONFIG.ENDPOINTS.CALL_END}/${roomId}`, {});
    },

    async getCallHistory(limit = 20) {
        return this.get(`${CONFIG.ENDPOINTS.CALL_HISTORY}?limit=${limit}`);
    },

    async getLingosBalance() {
        return this.get(CONFIG.ENDPOINTS.LINGOS_BALANCE);
    },

    async submitRating(sessionId, ratedUserId, rating, feedback) {
        return this.post(CONFIG.ENDPOINTS.RATING_SUBMIT, {
            session_id: sessionId,
            rated_user_id: ratedUserId,
            rating,
            feedback: feedback || null
        });
    },

    async getMyRatings(limit = 20) {
        return this.get(`${CONFIG.ENDPOINTS.MY_RATINGS}?limit=${limit}`);
    }
};