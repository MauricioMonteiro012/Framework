import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para adicionar token em todas requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// API de Autenticação
export const authAPI = {
  register: (data) => api.post('/sellers', data),
  activate: (data) => api.post('/sellers/activate', data),
  login: (data) => api.post('/auth/login', data),
  updateProfile: (data) => api.put('/user/update', data)
}

// API de Produtos
export const productAPI = {
  list: () => api.get('/products'),
  create: (data) => api.post('/products', data),
  getById: (id) => api.get(`/products/${id}`),
  update: (id, data) => api.put(`/products/${id}`, data),
  delete: (id) => api.delete(`/products/${id}`)
}

// API de Vendas
export const saleAPI = {
  create: (data) => api.post('/sales', data),
  list: () => api.get('/sales')
}

export default api
