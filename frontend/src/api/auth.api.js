import api from './http'

export const authApi = {
  login(data) {
    return api.post('/auth/login', data)
  },

  registration(data) {
    return api.post('/auth/registration', data)
  },

  refresh() {
    return api.post('/auth/refresh')
  },

  validate() {
    return api.post('/auth/validate')
  },
}