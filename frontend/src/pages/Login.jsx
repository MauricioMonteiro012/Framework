import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authAPI } from '../services/api'
import { useAuth } from '../context/AuthContext'
import './Auth.css'

export function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    senha: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await authAPI.login(formData)
      const { token, user } = response.data
      login(user, token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.mensagem || 'Erro ao fazer login. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Login</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            name="email"
            placeholder="E-mail"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="senha"
            placeholder="Senha"
            value={formData.senha}
            onChange={handleChange}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Entrando...' : 'Login'}
          </button>
        </form>
        <p>
          Não tem conta? <a href="/register">Cadastre-se aqui</a>
        </p>
      </div>
    </div>
  )
}
