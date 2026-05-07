<template>
  <header class="header">
    <div class="logo">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
        <rect x="3" y="3" width="8" height="8" rx="1"/>
        <rect x="13" y="3" width="8" height="8" rx="1"/>
        <rect x="3" y="13" width="8" height="8" rx="1"/>
        <rect x="13" y="13" width="8" height="8" rx="1"/>
      </svg>
      <span class="logo-text">НИТРОПРО</span>
    </div>

    <div class="container">
      <nav class="nav">
        <router-link to="/" class="nav-link">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/>
            <polyline points="9 21 9 12 15 12 15 21"/>
          </svg>
          <span class="nav-label">Главная</span>
        </router-link>

        <router-link to="/about" class="nav-link">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
          <span class="nav-label">О проекте</span>
        </router-link>
      </nav>
    </div>

    <div class="auth">
      <router-link to="/login" class="login-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
        <span class="auth-label">Личный кабинет</span>
      </router-link>
    </div>
  </header>
</template>

<script setup>
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

.header {
  background: #ffffff;
  border-bottom: 1px solid #e8eaee;
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 32px;
  font-family: 'Manrope', sans-serif;
  position: relative;
}

.logo {
  display: flex;
  align-items: center;
  gap: 9px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 500;
  color: #1a1d23;
  white-space: nowrap;
  flex-shrink: 0;
  text-decoration: none;
}

.logo svg {
  color: #3d6ce8;
  flex-shrink: 0;
}

.container {
  flex: 1;
  display: flex;
  justify-content: center;
  min-width: 0;
}

.nav {
  display: flex;
  gap: 4px;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: #6b7280;
  font-size: 13px;
  font-weight: 600;
  padding: 7px 12px;
  border-radius: 7px;
  border: 1px solid transparent;
  transition: color 0.15s, background 0.15s, border-color 0.15s;
  white-space: nowrap;
}

.nav-link svg {
  flex-shrink: 0;
  opacity: 0.7;
  transition: opacity 0.15s;
}

.nav-link:hover {
  color: #1a1d23;
  background: #f3f4f6;
}

.nav-link:hover svg {
  opacity: 1;
}

.nav-link.router-link-active {
  color: #3d6ce8;
  background: rgba(61, 108, 232, 0.07);
  border-color: rgba(61, 108, 232, 0.15);
}

.nav-link.router-link-active svg {
  opacity: 1;
}

.auth {
  flex-shrink: 0;
}

.login-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  text-decoration: none;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Manrope', sans-serif;
  border-radius: 7px;
  border: 1px solid #e8eaee;
  color: #1a1d23;
  background: #ffffff;
  white-space: nowrap;
  transition: background 0.15s, border-color 0.15s, box-shadow 0.15s;
}

.login-btn svg {
  color: #6b7280;
  flex-shrink: 0;
  transition: color 0.15s;
}

.login-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.login-btn:hover svg {
  color: #3d6ce8;
}

@media (max-width: 800px) {
  .logo-text { display: none; }
}

@media (max-width: 640px) {
  .header { padding: 0 16px; }
  .nav-label { display: none; }
  .nav-link { padding: 8px; }
  .auth-label { display: none; }
  .login-btn { padding: 8px; }
}
</style>