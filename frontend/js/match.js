(async function() {
    if (!requireAuth()) return;

    const findingTitle = document.getElementById('finding-title');
    const findingSubtitle = document.getElementById('finding-subtitle');
    const timerEl = document.getElementById('finding-timer');
    const cancelBtn = document.getElementById('cancel-btn');
    const userAvatar = document.getElementById('user-avatar');
    const langInfo = document.getElementById('lang-info');

    let wsManager = null;
    let timerInterval = null;
    let searchStartTime = null;
    let timeoutTimer = null;
    let hasTimedOut = false;
    const MATCH_TIMEOUT_SECONDS = 60;

    window.MATCH_DEBUG = { started: false, timeoutSet: false };

    async function loadUserInfo() {
        try {
            const profile = await API.getProfile();
            if (!profile) return;

            if (!profile.native_lang || !profile.learning_lang) {
                Toast.warning('Please complete your profile first');
                setTimeout(() => redirectTo(CONFIG.ROUTES.PROFILE), 1000);
                return;
            }

            userAvatar.textContent = profile.username.charAt(0).toUpperCase();

            const nativeLang = CONFIG.LANGUAGES.find(l => l.code === profile.native_lang);
            const learningLang = CONFIG.LANGUAGES.find(l => l.code === profile.learning_lang);
            
            langInfo.innerHTML = `
                <span class="lang-chip">${nativeLang?.flag || '🌐'} ${profile.native_lang}</span>
                <span class="lang-arrow">↔</span>
                <span class="lang-chip">${learningLang?.flag || '🌐'} ${profile.learning_lang}</span>
            `;

            Auth.saveUserData(profile);
            startMatching();
        } catch {
            Toast.error('Failed to load profile');
        }
    }

    function startTimer() {
        searchStartTime = Date.now();
        timerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - searchStartTime) / 1000);
            timerEl.textContent = formatDuration(elapsed);
            
            if (elapsed >= MATCH_TIMEOUT_SECONDS && !hasTimedOut) {
                hasTimedOut = true;
                console.log('⏰ TIMEOUT TRIGGERED at', elapsed, 'seconds');
                handleNoMatchFound();
            }
        }, 1000);
    }

    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        if (timeoutTimer) {
            clearTimeout(timeoutTimer);
            timeoutTimer = null;
        }
    }

    function handleNoMatchFound() {
        console.log('🚫 handleNoMatchFound called');
        stopTimer();

        if (wsManager) {
            try {
                if (wsManager.isConnected) {
                    wsManager.send({ type: 'cancel' });
                }
                setTimeout(() => wsManager.disconnect(), 300);
            } catch (e) {
                console.log('WS disconnect error:', e);
            }
        }

        findingTitle.textContent = 'No match found';
        findingSubtitle.textContent = 'No partners available right now. Please try again!';
        timerEl.textContent = '00:00';

        Toast.warning('No match found. Try again later!');

        showRetryOptions();
    }

    function showRetryOptions() {
        cancelBtn.innerHTML = `
            <span class="cancel-icon" style="transform: none;">🔄</span>
            <span>Try Again</span>
        `;
        cancelBtn.style.background = '#a855f7';
        
        const newBtn = cancelBtn.cloneNode(true);
        cancelBtn.parentNode.replaceChild(newBtn, cancelBtn);
        newBtn.addEventListener('click', retryMatch);

        if (!document.getElementById('home-btn')) {
            const goHomeBtn = document.createElement('button');
            goHomeBtn.className = 'cancel-call-btn';
            goHomeBtn.id = 'home-btn';
            goHomeBtn.style.background = '#6b6b6b';
            goHomeBtn.style.marginTop = '12px';
            goHomeBtn.innerHTML = `
                <span class="cancel-icon" style="transform: none;">🏠</span>
                <span>Back to Home</span>
            `;
            goHomeBtn.addEventListener('click', () => {
                redirectTo('/home.html');
            });
            newBtn.parentElement.appendChild(goHomeBtn);
        }
    }

    function retryMatch() {
        console.log('🔄 Retry match clicked');
        const homeBtn = document.getElementById('home-btn');
        if (homeBtn) homeBtn.remove();

        hasTimedOut = false;

        const currentBtn = document.getElementById('cancel-btn');
        currentBtn.innerHTML = `
            <span class="cancel-icon">📞</span>
            <span>Cancel</span>
        `;
        currentBtn.style.background = '';

        const newBtn = currentBtn.cloneNode(true);
        currentBtn.parentNode.replaceChild(newBtn, currentBtn);
        newBtn.addEventListener('click', cancelMatch);

        findingTitle.textContent = 'Looking for a new partner';
        findingSubtitle.textContent = 'Please wait a moment...';
        timerEl.textContent = '00:00';

        startMatching();
    }

    function startMatching() {
        console.log('🚀 Starting matching...');
        hasTimedOut = false;
        startTimer();

        wsManager = new WebSocketManager(CONFIG.WS_ENDPOINTS.MATCH);

        wsManager.on('connected', () => {
            findingSubtitle.textContent = 'Connecting to server...';
        });

        wsManager.on('waiting', () => {
            findingSubtitle.textContent = 'Please wait a moment...';
        });

        wsManager.on('match_found', (data) => {
            stopTimer();
            findingTitle.textContent = 'Match Found!';
            findingSubtitle.textContent = `Connecting with ${data.partner.username}...`;

            const callData = {
                room_id: data.room_id,
                session_id: data.session_id,
                partner: data.partner,
                is_caller: false
            };
            
            sessionStorage.setItem('call_data', JSON.stringify(callData));
            Toast.success(`Matched with ${data.partner.username}!`);

            setTimeout(() => {
                if (wsManager) wsManager.disconnect();
                redirectTo(CONFIG.ROUTES.CALL);
            }, 1500);
        });

        wsManager.on('cancelled', () => {
            if (!hasTimedOut) {
                stopTimer();
            }
        });

        wsManager.on('disconnected', (event) => {
            if (hasTimedOut) return;
            
            stopTimer();
            if (event && event.reason) {
                Toast.error(event.reason);
                if (event.reason.includes('profile')) {
                    setTimeout(() => redirectTo(CONFIG.ROUTES.PROFILE), 1500);
                    return;
                }
            }
        });

        wsManager.on('error', () => {
            if (hasTimedOut) return;
            stopTimer();
            Toast.error('Connection error. Please try again.');
            setTimeout(() => redirectTo('/home.html'), 1500);
        });

        wsManager.connect();
    }

    function cancelMatch() {
        console.log('❌ Cancel clicked');
        if (wsManager && wsManager.isConnected) {
            wsManager.send({ type: 'cancel' });
            setTimeout(() => {
                stopTimer();
                redirectTo('/home.html');
            }, 500);
        } else {
            stopTimer();
            redirectTo('/home.html');
        }
    }

    cancelBtn.addEventListener('click', cancelMatch);

    window.addEventListener('beforeunload', () => {
        stopTimer();
        if (wsManager) wsManager.disconnect();
    });

    await loadUserInfo();
})();