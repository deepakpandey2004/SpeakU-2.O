const Toast = {
    container: null,

    init() {
        if (this.container) return;
        this.container = document.createElement('div');
        this.container.id = 'toast-container';
        this.container.className = 'toast-container';
        document.body.appendChild(this.container);
    },

    show(message, type = 'info') {
        this.init();
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
        toast.innerHTML = `<span>${icons[type] || 'ℹ️'} ${message}</span>`;

        this.container.appendChild(toast);
        setTimeout(() => toast.classList.add('toast-show'), 10);

        setTimeout(() => {
            toast.classList.remove('toast-show');
            setTimeout(() => toast.remove(), 300);
        }, CONFIG.APP.TIMING.TOAST_DURATION);
    },

    success(msg) { this.show(msg, 'success'); },
    error(msg) { this.show(msg, 'error'); },
    info(msg) { this.show(msg, 'info'); },
    warning(msg) { this.show(msg, 'warning'); }
};

const Loader = {
    overlay: null,

    show(message = 'Loading...') {
        if (this.overlay) return;
        this.overlay = document.createElement('div');
        this.overlay.className = 'loader-overlay';
        this.overlay.innerHTML = `
            <div class="loader-content">
                <div class="loader-spinner"></div>
                <p>${message}</p>
            </div>
        `;
        document.body.appendChild(this.overlay);
    },

    hide() {
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
    }
};

function redirectTo(route) {
    window.location.href = route;
}

function isLoggedIn() {
    return !!localStorage.getItem(CONFIG.APP.STORAGE_KEYS.ACCESS_TOKEN);
}

function requireAuth() {
    if (!isLoggedIn()) {
        Toast.warning('Please login first');
        redirectTo(CONFIG.ROUTES.LOGIN);
        return false;
    }
    return true;
}

// function requireGuest() {
//     if (isLoggedIn()) {
//         redirectTo('/home.html');
//         return false;
//     }
//     return true;
// }

function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function validateField(value, rules) {
    if (!value || value.trim() === '') return 'This field is required';
    if (rules.MIN_LENGTH && value.length < rules.MIN_LENGTH) return `Minimum ${rules.MIN_LENGTH} characters required`;
    if (rules.MAX_LENGTH && value.length > rules.MAX_LENGTH) return `Maximum ${rules.MAX_LENGTH} characters allowed`;
    if (rules.PATTERN && !rules.PATTERN.test(value)) return 'Invalid format';
    return null;
}