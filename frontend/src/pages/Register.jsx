import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authAPI } from '../services/api'
import './Auth.css'

export function Register() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    nome: '',
    cnpj: '',
    email: '',
    celular: '',
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
      const response = await authAPI.register(formData)
      alert('Cadastro realizado! Verifique seu WhatsApp para o código de ativação.')
      navigate('/ativacao')
    } catch (err) {
      setError(err.response?.data?.mensagem || 'Erro ao registrar. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Cadastro de Vendedor</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="nome"
            placeholder="Nome"
            value={formData.nome}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="cnpj"
            placeholder="CNPJ"
            value={formData.cnpj}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="E-mail"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="tel"
            name="celular"
            placeholder="Celular"
            value={formData.celular}
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
            {loading ? 'Cadastrando...' : 'Cadastrar'}
          </button>
        </form>
        <p>
          Já tem conta? <a href="/login">Fazer login</a>
        </p>
      </div>
    </div>
  )
}
