import uvicorn
from app import create_app
from app.config import settings

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,          
        log_level="info"
    )


# http://localhost:8000/ console.log('Token:', localStorage.getItem('speaku_access_token'));
#console.log('User:', localStorage.getItem('speaku_user_data'));

# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
#     <title>Login - SpeakU</title>
#     <link rel="stylesheet" href="/css/style.css">
#     <style>
#         body {
#             background: #1a1a1a !important;
#             min-height: 100vh;
#             margin: 0;
#             padding: 0;
#         }
#         .auth-wrapper {
#             position: relative;
#             z-index: 1;
#             min-height: 100vh;
#             padding: 40px 32px;
#             max-width: 600px;
#             margin: 0 auto;
#         }
#         .auth-form input,
#         .auth-form button,
#         .auth-form a,
#         .back-btn {
#             position: relative;
#             z-index: 10;
#             pointer-events: auto;
#         }
#         .auth-form input {
#             cursor: text;
#             user-select: text;
#         }
#     </style>
# </head>
# <body>
#     <div class="auth-wrapper">
#         <div class="auth-header">
#             <a href="/" class="back-btn">← Back</a>
#             <h1 class="auth-title">Welcome Back!</h1>
#             <p class="auth-subtitle">Log in to continue your language journey</p>
#         </div>

#         <form class="auth-form" id="login-form">
#             <div class="form-group">
#                 <label for="email">Email</label>
#                 <input type="email" id="email" placeholder="you@example.com" autocomplete="email" required>
#                 <div class="form-error" id="email-error"></div>
#             </div>

#             <div class="form-group">
#                 <label for="password">Password</label>
#                 <input type="password" id="password" placeholder="Enter your password" autocomplete="current-password" required>
#                 <div class="form-error" id="password-error"></div>
#             </div>

#             <button type="submit" class="btn btn-primary" id="submit-btn">Log In</button>

#             <p class="link-text">
#                 Don't have an account? <a href="/register.html">Sign up</a>
#             </p>
#         </form>
#     </div>

#     <script src="/js/config.js"></script>
#     <script src="/js/ui.js"></script>
#     <script src="/js/auth.js"></script>
#     <script src="/js/api.js"></script>
#     <script>
#         console.log('LOGIN PAGE LOADED');
        
#         // Clear old session
#         Auth.clearAll();

#         const form = document.getElementById('login-form');
#         const submitBtn = document.getElementById('submit-btn');

#         function showError(fieldId, message) {
#             const errorEl = document.getElementById(`${fieldId}-error`);
#             if (message) {
#                 errorEl.textContent = message;
#                 errorEl.style.display = 'block';
#             } else {
#                 errorEl.style.display = 'none';
#             }
#         }

#         function clearErrors() {
#             ['email', 'password'].forEach(id => showError(id, ''));
#         }

#         form.addEventListener('submit', async (e) => {
#             e.preventDefault();
#             clearErrors();

#             const email = document.getElementById('email').value.trim();
#             const password = document.getElementById('password').value;

#             let hasError = false;

#             if (!CONFIG.VALIDATION.EMAIL.PATTERN.test(email)) {
#                 showError('email', 'Please enter a valid email');
#                 hasError = true;
#             }

#             if (!password) {
#                 showError('password', 'Password is required');
#                 hasError = true;
#             }

#             if (hasError) return;

#             submitBtn.disabled = true;
#             submitBtn.textContent = 'Logging in...';
#             Loader.show('Logging you in...');

#             try {
#                 const data = await API.login(email, password);
#                 Loader.hide();
                
#                 if (data && data.access_token) {
#                     Toast.success('Welcome back!');
#                     try {
#                         const profile = await API.getProfile();
#                         if (profile && profile.native_lang && profile.learning_lang) {
#                             setTimeout(() => redirectTo('/home.html'), 800);
#                         } else {
#                             setTimeout(() => redirectTo('/profile.html'), 800);
#                         }
#                     } catch {
#                         setTimeout(() => redirectTo('/profile.html'), 800);
#                     }
#                 }
#             } catch (error) {
#                 Loader.hide();
#                 submitBtn.disabled = false;
#                 submitBtn.textContent = 'Log In';
                
#                 if (error && error.status === 401) {
#                     Toast.error('Invalid email or password');
#                 } else if (error && error.data && error.data.detail) {
#                     Toast.error(error.data.detail);
#                 } else {
#                     Toast.error('Login failed. Please try again.');
#                 }
#             }
#         });
#     </script>
# </body>
# </html>