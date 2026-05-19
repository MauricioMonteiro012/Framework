import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authAPI } from '../services/api'
import './Auth.css'

export function Activation() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '',
    codigo: ''
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
      await authAPI.activate(formData)
      alert('Conta ativada com sucesso! Faça login para continuar.')
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.mensagem || 'Erro ao ativar conta. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Ativar Conta</h2>
        <p>Digite o código que você recebeu no WhatsApp</p>
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
            type="text"
            name="codigo"
            placeholder="Código (4 dígitos)"
            value={formData.codigo}
            onChange={handleChange}
            maxLength="4"
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Ativando...' : 'Ativar'}
          </button>
        </form>
      </div>
    </div>
  )
}
