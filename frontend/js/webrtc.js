(async function() {
    if (!requireAuth()) return;

    const callDataRaw = sessionStorage.getItem('call_data');
    if (!callDataRaw) {
        Toast.error('No active call data found');
        setTimeout(() => redirectTo(CONFIG.ROUTES.MATCH), 1500);
        return;
    }

    const callData = JSON.parse(callDataRaw);
    const { room_id, session_id, partner } = callData;
    const currentUser = Auth.getUserData();

    // UI Elements
    const connectingState = document.getElementById('connecting-state');
    const callState = document.getElementById('call-state');
    const connectionStatus = document.getElementById('connection-status');
    const callTimer = document.getElementById('call-timer');
    const muteBtn = document.getElementById('mute-btn');
    const speakerBtn = document.getElementById('speaker-btn');
    const endBtn = document.getElementById('end-btn');
    const remoteAudio = document.getElementById('remote-audio');
    const connectionQuality = document.getElementById('connection-quality');
    const ratingModal = document.getElementById('rating-modal');

    // WebRTC state
    let peerConnection = null;
    let localStream = null;
    let signalingWs = null;
    let isMuted = false;
    let isSpeakerOn = true;
    let isCallActive = false;
    let callStartTime = null;
    let callTimerInterval = null;
    let callStartTime = null;
    let callTimerInterval = null;
    let sessionCountdownInterval = null;
    const SESSION_LIMIT_SECONDS = 10 * 60; // 10 minutes
    let isInitiator = false;
    let peerJoined = false;
    let selectedRating = 0;
    let callEnded = false;

    // Populate partner info
    function displayPartnerInfo() {
        const avatar = partner.username.charAt(0).toUpperCase();
        const nativeLang = CONFIG.LANGUAGES.find(l => l.code === partner.native_lang);
        const learningLang = CONFIG.LANGUAGES.find(l => l.code === partner.learning_lang);
        const langText = `${nativeLang?.flag || '🌐'} ${partner.native_lang} → ${learningLang?.flag || '🌐'} ${partner.learning_lang}`;

        document.getElementById('partner-avatar').textContent = avatar;
        document.getElementById('partner-avatar-2').textContent = avatar;
        document.getElementById('partner-name').textContent = partner.username;
        document.getElementById('partner-name-2').textContent = partner.username;
        document.getElementById('partner-langs').textContent = langText;
        document.getElementById('partner-langs-2').textContent = langText;
        document.getElementById('rate-partner-name').textContent = `How was your call with ${partner.username}?`;
    }

    // Get microphone access
    async function getMicrophoneAccess() {
        try {
            connectionStatus.textContent = '🎤 Requesting microphone...';
            localStream = await navigator.mediaDevices.getUserMedia(CONFIG.WEBRTC.mediaConstraints);
            return true;
        } catch (error) {
            Toast.error('Microphone access denied. Please allow microphone.');
            connectionStatus.textContent = '❌ Microphone access denied';
            setTimeout(() => redirectTo(CONFIG.ROUTES.MATCH), 2000);
            return false;
        }
    }

    // Create WebRTC peer connection
    function createPeerConnection() {
        peerConnection = new RTCPeerConnection({
            iceServers: CONFIG.WEBRTC.iceServers
        });

        // Add local audio tracks
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });

        // Send ICE candidates to peer
        peerConnection.onicecandidate = (event) => {
            if (event.candidate && signalingWs && signalingWs.isConnected) {
                signalingWs.send({
                    type: 'ice-candidate',
                    candidate: event.candidate
                });
            }
        };

        // Handle remote audio stream
        peerConnection.ontrack = (event) => {
            if (event.streams && event.streams[0]) {
                remoteAudio.srcObject = event.streams[0];
                onCallConnected();
            }
        };

        // Connection state changes
        peerConnection.onconnectionstatechange = () => {
            const state = peerConnection.connectionState;
            console.log('Connection state:', state);
            
            if (state === 'connected') {
                connectionQuality.textContent = '🟢 Connected';
            } else if (state === 'disconnected') {
                connectionQuality.textContent = '🟡 Reconnecting...';
            } else if (state === 'failed') {
                connectionQuality.textContent = '🔴 Connection failed';
                Toast.error('Connection failed');
                handleCallEnd(false);
            }
        };
    }

    // Connect to signaling WebSocket
    function connectSignaling() {
        const token = Auth.getToken();
        const wsUrl = `${CONFIG.WS_BASE_URL}${CONFIG.WS_ENDPOINTS.SIGNALING}/${room_id}?token=${token}`;
        
        signalingWs = {
            ws: new WebSocket(wsUrl),
            isConnected: false,
            send(data) {
                if (this.ws.readyState === WebSocket.OPEN) {
                    this.ws.send(JSON.stringify(data));
                    return true;
                }
                return false;
            },
            close() {
                if (this.ws) this.ws.close();
            }
        };

        signalingWs.ws.onopen = () => {
            signalingWs.isConnected = true;
            connectionStatus.textContent = '🔗 Signaling connected...';
            console.log('Signaling WebSocket connected');
        };

        signalingWs.ws.onmessage = async (event) => {
            try {
                const message = JSON.parse(event.data);
                await handleSignalingMessage(message);
            } catch (error) {
                console.error('Signaling message error:', error);
            }
        };

        signalingWs.ws.onerror = (error) => {
            console.error('Signaling error:', error);
            Toast.error('Signaling connection error');
        };

        signalingWs.ws.onclose = () => {
            signalingWs.isConnected = false;
            console.log('Signaling WebSocket closed');
        };
    }

    // Handle signaling messages
    async function handleSignalingMessage(message) {
        console.log('📩 Signaling message:', message.type);

        switch (message.type) {
            case 'room-joined':
    connectionStatus.textContent = '⏳ Waiting for partner...';
    if (message.peers_in_room === 2) {
        peerJoined = true;
        
    }
    break;

            case 'peer-joined':
                peerJoined = true;
                connectionStatus.textContent = '📡 Partner joined, connecting...';
                // First person creates offer when second person joins
                if (!isInitiator) {
                    isInitiator = true;
                    await createOffer();
                }
                break;

            case 'offer':
                await handleOffer(message);
                break;

            case 'answer':
                await handleAnswer(message);
                break;

            case 'ice-candidate':
                await handleIceCandidate(message);
                break;

            case 'peer-left':
                Toast.warning('Partner disconnected');
                handleCallEnd(true);
                break;

            case 'call-ended':
                Toast.info('Call ended by partner');
                handleCallEnd(true);
                break;

            case 'error':
                Toast.error(message.message || 'Signaling error');
                break;
        }
    }

    // Create and send offer
    async function createOffer() {
        try {
            const offer = await peerConnection.createOffer();
            await peerConnection.setLocalDescription(offer);
            signalingWs.send({
                type: 'offer',
                offer: offer
            });
            console.log('📤 Offer sent');
        } catch (error) {
            console.error('Create offer error:', error);
            Toast.error('Failed to create offer');
        }
    }

    // Handle incoming offer
    async function handleOffer(message) {
        try {
            await peerConnection.setRemoteDescription(new RTCSessionDescription(message.offer));
            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);
            signalingWs.send({
                type: 'answer',
                answer: answer
            });
            console.log('📤 Answer sent');
        } catch (error) {
            console.error('Handle offer error:', error);
            Toast.error('Failed to handle offer');
        }
    }

    // Handle incoming answer
    async function handleAnswer(message) {
        try {
            await peerConnection.setRemoteDescription(new RTCSessionDescription(message.answer));
            console.log('✅ Answer received');
        } catch (error) {
            console.error('Handle answer error:', error);
        }
    }

    // Handle ICE candidate
    async function handleIceCandidate(message) {
        try {
            if (message.candidate) {
                await peerConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
            }
        } catch (error) {
            console.error('ICE candidate error:', error);
        }
    }

    // Call connected successfully
    function onCallConnected() {
        if (isCallActive) return;
        isCallActive = true;
        connectingState.style.display = 'none';
        callState.style.display = 'block';
        callStartTime = Date.now();
        startCallTimer();
        startSessionCountdown();
        Toast.success('Call connected!');
    }

    // Start call timer
    function startCallTimer() {
        callTimerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - callStartTime) / 1000);
            callTimer.textContent = formatDuration(elapsed);
        }, 1000);
        
    }

    function startSessionCountdown() {
    const countdownEl = document.getElementById('session-countdown');
    sessionCountdownInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - callStartTime) / 1000);
        const remaining = SESSION_LIMIT_SECONDS - elapsed;

        if (remaining <= 0) {
            countdownEl.textContent = '⏳ 00:00 left';
            clearInterval(sessionCountdownInterval);
            sessionCountdownInterval = null;
            showContinueModal();
        } else {
            countdownEl.textContent = `⏳ ${formatDuration(remaining)} left`;
        }
        }, 1000);
    }

    function stopSessionCountdown() {
        if (sessionCountdownInterval) {
            clearInterval(sessionCountdownInterval);
            sessionCountdownInterval = null;
        }
    }

    function showContinueModal() {
        document.getElementById('continue-modal').style.display = 'flex';
        }

    function hideContinueModal() {
        document.getElementById('continue-modal').style.display = 'none';
    }
    

    // Stop call timer
    function stopCallTimer() {
        if (callTimerInterval) {
            clearInterval(callTimerInterval);
            callTimerInterval = null;
        }
    }

    // Mute/Unmute
    function toggleMute() {
        if (!localStream) return;
        isMuted = !isMuted;
        localStream.getAudioTracks().forEach(track => {
            track.enabled = !isMuted;
        });
        muteBtn.textContent = isMuted ? '🔇' : '🎤';
        muteBtn.classList.toggle('active', isMuted);
        Toast.info(isMuted ? 'Microphone muted' : 'Microphone unmuted');
    }

    // Speaker toggle
    function toggleSpeaker() {
        isSpeakerOn = !isSpeakerOn;
        remoteAudio.muted = !isSpeakerOn;
        speakerBtn.textContent = isSpeakerOn ? '🔊' : '🔇';
        speakerBtn.classList.toggle('active', !isSpeakerOn);
        Toast.info(isSpeakerOn ? 'Speaker on' : 'Speaker muted');
    }

    // End call
    async function handleCallEnd(fromPeer = false) {
    if (callEnded) return;
    callEnded = true;

    stopCallTimer();
    stopSessionCountdown();

    // Notify peer via signaling

        // Notify peer via signaling
        if (!fromPeer && signalingWs && signalingWs.isConnected) {
            signalingWs.send({ type: 'end-call' });
        }

        // End call in backend
        try {
            await API.endCall(room_id);
        } catch (error) {
            console.error('End call API error:', error);
        }

        // Cleanup
        if (peerConnection) {
            peerConnection.close();
            peerConnection = null;
        }
        if (localStream) {
            localStream.getTracks().forEach(track => track.stop());
            localStream = null;
        }
        if (signalingWs) {
            signalingWs.close();
            signalingWs = null;
        }

        // Show rating modal if call was active
        if (isCallActive) {
            showRatingModal();
        } else {
            redirectTo(CONFIG.ROUTES.MATCH);
        }
    }

    // Rating modal
    function showRatingModal() {
        ratingModal.style.display = 'flex';
        setupRatingStars();
    }

    function setupRatingStars() {
        const stars = document.querySelectorAll('.star');
        const submitBtn = document.getElementById('submit-rating');

        stars.forEach(star => {
            star.addEventListener('click', () => {
                selectedRating = parseInt(star.dataset.rating);
                stars.forEach(s => {
                    const rating = parseInt(s.dataset.rating);
                    s.classList.toggle('active', rating <= selectedRating);
                });
                submitBtn.disabled = false;
            });
        });

        document.getElementById('skip-rating').addEventListener('click', () => {
            redirectTo(CONFIG.ROUTES.MATCH);
        });

        submitBtn.addEventListener('click', async () => {
            if (selectedRating === 0) return;

            const feedback = document.getElementById('feedback').value.trim();
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            try {
                await API.submitRating(session_id, partner.id, selectedRating, feedback);
                Toast.success('Thanks for your feedback!');
                setTimeout(() => redirectTo(CONFIG.ROUTES.MATCH), 1000);
            } catch (error) {
                Toast.error('Failed to submit rating');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit';
            }
        });
    }

    // Event listeners
    muteBtn.addEventListener('click', toggleMute);
    speakerBtn.addEventListener('click', toggleSpeaker);
    endBtn.addEventListener('click', () => handleCallEnd(false));

    document.getElementById('continue-session-btn').addEventListener('click', () => {
    hideContinueModal();
    callStartTime = Date.now();
    startSessionCountdown();
});

document.getElementById('end-session-btn').addEventListener('click', () => {
    hideContinueModal();
    handleCallEnd(false);
});

    window.addEventListener('beforeunload', (e) => {
        if (isCallActive && !callEnded) {
            handleCallEnd(false);
        }
    });

    // Initialize call
    async function initCall() {
        displayPartnerInfo();

        const micGranted = await getMicrophoneAccess();
        if (!micGranted) return;

        createPeerConnection();
        connectSignaling();

        // Cleanup call data from sessionStorage
        sessionStorage.removeItem('call_data');
    }

    initCall();
})();