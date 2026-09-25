<template>
  <div class="page">
    <section class="cabinet-hero">
      <div class="cabinet-hero-inner">
        <div class="user-avatar">{{ initials }}</div>
        <div class="user-info">
          <h1 class="user-name">{{ user?.name || user?.email || 'Загрузка...' }}</h1>
          <p class="user-email" v-if="user?.email">{{ user.email }}</p>
        </div>
        <button class="logout-btn" @click="logout">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Выйти
        </button>
      </div>

      <div class="cabinet-stats" v-if="user">
        <div class="stat">
          <span class="stat-num">{{ user?.analyses_count ?? 0 }}</span>
          <span class="stat-label">Анализов выполнено</span>
        </div>
        <div class="stat-div"></div>
        <div class="stat">
          <span class="stat-num">{{ memberSince }}</span>
          <span class="stat-label">На платформе с</span>
        </div>
      </div>
    </section>

    <section class="tool-section">
      <div class="tool-header">
        <h2 class="tool-title">Последние работы</h2>
        <p class="tool-subtitle">5 последних запусков доступны для скачивания в любой момент</p>
      </div>

      <div class="panel history-panel">
        <div class="panel-header">
          <span class="panel-label">ЗАПУСКИ</span>
        </div>

        <!-- Skeleton вместо текстовой заглушки — сохраняет форму контента,
             пока идёт запрос к /users/me/analyses/latest -->
        <div v-if="isLoading" class="history-list">
          <div v-for="i in 5" :key="i" class="history-row history-row--skeleton">
            <div class="skeleton skeleton-badge"></div>
            <div class="history-meta">
              <div class="skeleton skeleton-line skeleton-line--wide"></div>
              <div class="skeleton skeleton-line skeleton-line--narrow"></div>
            </div>
            <div class="skeleton skeleton-download"></div>
          </div>
        </div>

        <div v-else-if="!analyses.length" class="empty-state">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
          <p class="empty-text">Пока нет ни одного анализа</p>
          <router-link to="/" class="empty-cta">Запустить первый анализ →</router-link>
        </div>

        <div v-else class="history-list">
          <div v-for="item in analyses" :key="item.id" class="history-row">
            <div class="history-method">
              <span class="history-badge" :class="'history-badge--' + methodColor(item.algorithm)">{{ item.algorithm }}</span>
            </div>
            <div class="history-meta">
              <span class="history-area">{{ displayName(item) }}</span>
              <span class="history-date">{{ formatTimestamp(item.created_at) }}</span>
            </div>
            <a v-if="item.archive_url" :href="downloadUrl(item.archive_url)" class="history-download">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/http'
import { useAuth } from '@/router/useAuth'

const router = useRouter()
const { authState, resetAuth } = useAuth()

// данные о пользователе уже загружены гвардом роутера к моменту захода
// на эту страницу — здесь просто читаем их, без повторного запроса
const user = computed(() => authState.user)

const analyses = ref([])
const isLoading = ref(true)

const initials = computed(() => {
  const source = user.value?.name || user.value?.email || '?'
  return source.slice(0, 2).toUpperCase()
})

const memberSince = computed(() => {
  if (!user.value?.created_at) return '—'
  return new Date(user.value.created_at).toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })
})

const formatTimestamp = (ts) => ts ? new Date(ts).toLocaleString('ru-RU') : ''

const displayName = (item) => {
  if (item.upload_id) return `Участок ${item.upload_id.slice(-8)}`
  return 'Без названия'
}

const methodColor = (algorithm) => ({
  NDVI: 'green', ChlRI: 'blue', RPImod: 'amber',
}[algorithm] ?? 'blue')

const downloadUrl = (path) => api.defaults.baseURL + path

const logout = async () => {
  try { await api.post('/auth/logout') } catch {}
  resetAuth() // сбрасываем кэш — иначе гвард пропустит по старому isAuthenticated
  router.push({ name: 'Login' })
}

onMounted(async () => {
  try {
    const { data } = await api.get('/users/me/analyses/latest')
    analyses.value = data
  } catch {
    analyses.value = []
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.page {
  background: #ffffff;
  font-family: 'Manrope', sans-serif;
  color: #1a1d23;
  min-height: 100vh;
}

.cabinet-hero {
  padding: 56px 48px 40px;
  border-bottom: 1px solid #e8eaee;
  background: linear-gradient(180deg, #f6f9f3 0%, #f2f7ee 100%);
}
.cabinet-hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}
.user-avatar {
  width: 56px; height: 56px; border-radius: 14px;
  background: #3d6ce8; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 18px; letter-spacing: 0.5px;
  font-family: 'JetBrains Mono', monospace; flex-shrink: 0;
}
.user-info { flex: 1; min-width: 0; }
.user-name {
  font-size: 22px; font-weight: 800; letter-spacing: -0.5px;
  color: #0d0f14; margin-bottom: 3px;
}
.user-email { font-size: 13px; color: #9ca3af; }

.logout-btn {
  display: flex; align-items: center; gap: 7px;
  padding: 9px 16px; background: #fff;
  border: 1px solid #e8eaee; border-radius: 8px;
  font-size: 12px; font-weight: 600; color: #6b7280;
  cursor: pointer; transition: all 0.2s;
  font-family: 'Manrope', sans-serif; flex-shrink: 0;
}
.logout-btn:hover { border-color: #d1d5db; color: #374151; }

.cabinet-stats {
  max-width: 1200px; margin: 32px auto 0;
  display: flex; align-items: center; gap: 28px;
  padding-top: 28px; border-top: 1px solid #e8eaee;
}
.stat { display: flex; flex-direction: column; gap: 3px; }
.stat-num {
  font-size: 22px; font-weight: 800; color: #0d0f14;
  letter-spacing: -0.5px; font-family: 'JetBrains Mono', monospace;
}
.stat-label {
  font-size: 10px; color: #9ca3af; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.8px;
}
.stat-div { width: 1px; height: 32px; background: #e8eaee; }

.tool-section { max-width: 1200px; margin: 0 auto; padding: 40px 48px 72px; }
.tool-header { margin-bottom: 20px; }
.tool-title {
  font-size: 20px; font-weight: 800; letter-spacing: -0.5px;
  color: #0d0f14; margin-bottom: 5px;
}
.tool-subtitle { font-size: 13px; color: #9ca3af; }

.panel {
  border: 1px solid #e8eaee; border-radius: 14px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05); overflow: hidden; background: #fff;
}
.panel-header {
  display: flex; align-items: center; padding: 15px 20px;
  border-bottom: 1px solid #e8eaee;
}
.panel-label {
  font-size: 10px; font-weight: 700; letter-spacing: 1.8px;
  color: #c5c9d4; text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
}

.state-msg { padding: 40px 20px; text-align: center; font-size: 13px; color: #9ca3af; }

.empty-state {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 10px; padding: 56px 20px;
  color: #d1d5db;
}
.empty-text { font-size: 13px; color: #9ca3af; font-weight: 500; }
.empty-cta {
  margin-top: 4px; font-size: 12px; font-weight: 700;
  color: #3d6ce8; text-decoration: none;
}
.empty-cta:hover { text-decoration: underline; }

.history-list { display: flex; flex-direction: column; }
.history-row {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 20px; border-bottom: 1px solid #f0f1f3;
  transition: background 0.15s;
}
.history-row:last-child { border-bottom: none; }
.history-row:hover { background: #fafbfc; }

.history-badge {
  padding: 4px 10px; border-radius: 6px; font-size: 11px;
  font-weight: 700; font-family: 'JetBrains Mono', monospace;
}
.history-badge--green { color: #2f6b2f; background: #dff2df; border: 1px solid #8fc98d; }
.history-badge--blue  { color: #2855c7; background: #e1e9ff; border: 1px solid #8da8ee; }
.history-badge--amber { color: #945914; background: #fff0d9; border: 1px solid #e5ad68; }

.history-meta { flex: 1; display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.history-area {
  font-size: 13px; font-weight: 600; color: #374151;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.history-date { font-size: 11px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; }

.history-download {
  display: flex; align-items: center; justify-content: center;
  width: 30px; height: 30px; border-radius: 7px;
  border: 1px solid #e8eaee; color: #6b7280;
  transition: all 0.2s; flex-shrink: 0;
}
.history-download:hover { border-color: #3d6ce8; color: #3d6ce8; background: rgba(61,108,232,0.05); }

/* --- Skeleton loading state --- */
.history-row--skeleton { cursor: default; }
.history-row--skeleton:hover { background: transparent; }

.skeleton {
  background: linear-gradient(90deg, #eef0f3 25%, #e3e6ea 37%, #eef0f3 63%);
  background-size: 400% 100%;
  animation: skeleton-shimmer 1.6s ease-in-out infinite;
  border-radius: 6px;
}

.skeleton-badge { width: 56px; height: 22px; flex-shrink: 0; }

.skeleton-line { height: 11px; border-radius: 4px; }
.skeleton-line--wide { width: 55%; margin-bottom: 6px; }
.skeleton-line--narrow { width: 30%; }

.skeleton-download { width: 30px; height: 30px; border-radius: 7px; flex-shrink: 0; }

@keyframes skeleton-shimmer {
  0% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@media (max-width: 720px) {
  .cabinet-hero, .tool-section { padding-left: 20px; padding-right: 20px; }
  .cabinet-hero-inner { flex-wrap: wrap; }
}
</style>