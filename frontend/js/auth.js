const Auth = {
    getToken() {
        return localStorage.getItem(CONFIG.APP.STORAGE_KEYS.ACCESS_TOKEN);
    },

    getUserData() {
        const data = localStorage.getItem(CONFIG.APP.STORAGE_KEYS.USER_DATA);
        return data ? JSON.parse(data) : null;
    },

    saveToken(accessToken) {
        localStorage.setItem(CONFIG.APP.STORAGE_KEYS.ACCESS_TOKEN, accessToken);
    },

    saveUserData(userData) {
        localStorage.setItem(CONFIG.APP.STORAGE_KEYS.USER_DATA, JSON.stringify(userData));
    },

    clearAll() {
        localStorage.removeItem(CONFIG.APP.STORAGE_KEYS.ACCESS_TOKEN);
        localStorage.removeItem(CONFIG.APP.STORAGE_KEYS.USER_DATA);
    },

    logout() {
        this.clearAll();
        Toast.success('Logged out successfully');
        redirectTo(CONFIG.ROUTES.LOGIN);
    },

    getAuthHeaders() {
        const token = this.getToken();
        return token 
            ? { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } 
            : { 'Content-Type': 'application/json' };
    }
};