const IS_PRODUCTION = window.location.hostname !== 'localhost' && 
                      window.location.hostname !== '127.0.0.1';

const CONFIG = {
    API_BASE_URL: IS_PRODUCTION 
        ? 'https://speaku-2-o.onrender.com'
        : 'http://localhost:8000',
    
    WS_BASE_URL: IS_PRODUCTION
        ? 'wss://speaku-2-o.onrender.com'
        : 'ws://localhost:8000',
    
    ENDPOINTS: {
        // Authentication
        REGISTER: '/auth/register',
        LOGIN: '/auth/login',
        ME: '/auth/me',
        
        // Profile
        PROFILE_GET: '/profile/me',
        PROFILE_UPDATE: '/profile/update',
        PROFILE_PUBLIC: '/profile',
        LEADERBOARD: '/profile/leaderboard/top',
        SEARCH_LANGUAGE: '/profile/search/by-language',
        
        // Match
        MATCH_STATS: '/match/stats',
        
        // Call
        CALL_END: '/call/end',
        CALL_HISTORY: '/call/history',
        LINGOS_BALANCE: '/call/lingos/balance',
        
        // Rating
        RATING_SUBMIT: '/rating/submit',
        MY_RATINGS: '/rating/my-ratings',
    },
    
    WS_ENDPOINTS: {
        MATCH: '/match/find',
        SIGNALING: '/signaling/signal',
    },
    
    WEBRTC: {
        iceServers: [
            {
                urls: [
                    'stun:stun.l.google.com:19302',
                    'stun:stun1.l.google.com:19302',
                    'stun:stun2.l.google.com:19302',
                    'stun:stun3.l.google.com:19302',
                    'stun:stun4.l.google.com:19302'
                ]
            }
        ],
        
        mediaConstraints: {
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true
            },
            video: false
        }
    },
    
    APP: {
        NAME: 'SpeakU',
        VERSION: '2.0.0',
        
        STORAGE_KEYS: {
            ACCESS_TOKEN: 'speaku_access_token',
            USER_DATA: 'speaku_user_data',
        },
        
        TIMING: {
            TOAST_DURATION: 3000,
            MATCH_TIMEOUT: 60000,
            WS_RECONNECT_DELAY: 3000,
            WS_MAX_RECONNECTS: 5,
        },
        
        PAGINATION: {
            DEFAULT_LIMIT: 20,
            MAX_LIMIT: 100,
        }
    },
    
    VALIDATION: {
        USERNAME: {
            MIN_LENGTH: 3,
            MAX_LENGTH: 20,
            PATTERN: /^[a-zA-Z0-9_]+$/
        },
        PASSWORD: {
            MIN_LENGTH: 8,
            MAX_LENGTH: 50,
            PATTERN: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
        },
        EMAIL: {
            PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        }
    },
    
    LANGUAGES: [
        { code: 'English', name: 'English', flag: '🇬🇧' },
        { code: 'Hindi', name: 'Hindi', flag: '🇮🇳' },
        { code: 'Spanish', name: 'Spanish', flag: '🇪🇸' },
        { code: 'French', name: 'French', flag: '🇫🇷' },
        { code: 'German', name: 'German', flag: '🇩🇪' },
        { code: 'Japanese', name: 'Japanese', flag: '🇯🇵' },
        { code: 'Chinese', name: 'Chinese', flag: '🇨🇳' },
        { code: 'Korean', name: 'Korean', flag: '🇰🇷' },
        { code: 'Portuguese', name: 'Portuguese', flag: '🇵🇹' },
        { code: 'Italian', name: 'Italian', flag: '🇮🇹' },
        { code: 'Russian', name: 'Russian', flag: '🇷🇺' },
        { code: 'Arabic', name: 'Arabic', flag: '🇸🇦' },
        { code: 'Bengali', name: 'Bengali', flag: '🇧🇩' },
        { code: 'Tamil', name: 'Tamil', flag: '🇮🇳' },
        { code: 'Telugu', name: 'Telugu', flag: '🇮🇳' },
        { code: 'Marathi', name: 'Marathi', flag: '🇮🇳' },
        { code: 'Gujarati', name: 'Gujarati', flag: '🇮🇳' },
        { code: 'Punjabi', name: 'Punjabi', flag: '🇮🇳' },
    ],
    
    ROUTES: {
        HOME: '/',
        LOGIN: '/login.html',
        REGISTER: '/register.html',
        PROFILE: '/profile.html',
        MATCH: '/match.html',
        CALL: '/call.html',
    }
};

function getApiUrl(endpoint) {
    return `${CONFIG.API_BASE_URL}${endpoint}`;
}

function getWsUrl(endpoint, token = null) {
    let url = `${CONFIG.WS_BASE_URL}${endpoint}`;
    if (token) {
        url += `?token=${token}`;
    }
    return url;
}

Object.freeze(CONFIG);
Object.freeze(CONFIG.ENDPOINTS);
Object.freeze(CONFIG.WS_ENDPOINTS);
Object.freeze(CONFIG.WEBRTC);
Object.freeze(CONFIG.APP);
Object.freeze(CONFIG.VALIDATION);
Object.freeze(CONFIG.LANGUAGES);
Object.freeze(CONFIG.ROUTES);

if (!IS_PRODUCTION) {
    console.log('%c🔧 SpeakU Config Loaded', 'color: #8b5cf6; font-size: 14px; font-weight: bold;');
    console.log('📍 Environment:', IS_PRODUCTION ? 'Production' : 'Development');
    console.log('🌐 API Base URL:', CONFIG.API_BASE_URL);
    console.log('🔌 WS Base URL:', CONFIG.WS_BASE_URL);
}