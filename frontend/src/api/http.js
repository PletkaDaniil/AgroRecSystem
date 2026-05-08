import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
})

const AUTH_ROUTES = [
  '/auth/login',
  '/auth/registration',
  '/auth/refresh',
]

// флаг активного refresh запроса
let isRefreshing = false

// очередь запросов, которые ждут завершения refresh
let refreshSubscribers = []

function subscribeTokenRefresh(callback) {
  refreshSubscribers.push(callback)
}

function onRefreshed(success) {
  refreshSubscribers.forEach(cb => cb(success))
  refreshSubscribers = []
}

api.interceptors.response.use(
  response => response,

  async error => {
    const status = error.response?.status
    const originalRequest = error.config

    const isAuthRoute = AUTH_ROUTES.some(route =>
      originalRequest.url?.includes(route)
    )

    // если 401 и это не auth запрос и ещё не было retry
    if (status === 401 && !originalRequest._retry && !isAuthRoute) {

      // если refresh уже выполняется — просто подписываемся на результат
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          subscribeTokenRefresh((success) => {
            if (success) resolve(api(originalRequest))
            else reject(error)
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        // refresh должен отработать быстро, поэтому ставим таймаут
        const controller = new AbortController()
        const refreshTimeout = setTimeout(() => controller.abort(), 15_000)

        await api.post('/auth/refresh', null, { signal: controller.signal })
        clearTimeout(refreshTimeout)

        isRefreshing = false
        onRefreshed(true)

        // повторяем исходный запрос после успешного refresh
        return api(originalRequest)

      } catch (refreshError) {
        isRefreshing = false
        onRefreshed(false)

        // глобальное событие: разлогин / ошибка авторизации
        window.dispatchEvent(
          new CustomEvent('auth-error', {
            detail: refreshError.response?.data?.detail
          })
        )

        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api