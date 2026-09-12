import { reactive } from 'vue'
import api from '@/api/http'

const authState = reactive({
  user: null,
  isAuthenticated: false,
})

async function fetchUser() {
  try {
    const { data } = await api.get('/users/me')
    authState.user = data
    authState.isAuthenticated = true
    return true
  } catch {
    authState.user = null
    authState.isAuthenticated = false
    return false
  }
}

function resetAuth() {
  authState.user = null
  authState.isAuthenticated = false
}

export function useAuth() {
  return { authState, fetchUser, resetAuth }
}