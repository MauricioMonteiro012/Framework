import React, { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { productAPI } from '../services/api'
import './Products.css'

export function ProductForm() {
  const navigate = useNavigate()
  const { id } = useParams()
  const [formData, setFormData] = useState({
    nome: '',
    preco: '',
    quantidade: '',
    status: 'ativo',
    imagem: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (id) {
      loadProduct(id)
    }
  }, [id])

  const loadProduct = async (productId) => {
    try {
      const response = await productAPI.getById(productId)
      setFormData(response.data)
    } catch (err) {
      setError('Erro ao carregar produto')
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (id) {
        await productAPI.update(id, formData)
        alert('Produto atualizado com sucesso!')
      } else {
        await productAPI.create(formData)
        alert('Produto criado com sucesso!')
      }
      navigate('/products')
    } catch (err) {
      setError(err.response?.data?.mensagem || 'Erro ao salvar produto')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="form-container">
      <div className="form-card">
        <h2>{id ? 'Editar Produto' : 'Novo Produto'}</h2>
        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nome</label>
            <input
              type="text"
              name="nome"
              value={formData.nome}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Preço</label>
            <input
              type="number"
              name="preco"
              step="0.01"
              value={formData.preco}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Quantidade em Estoque</label>
            <input
              type="number"
              name="quantidade"
              value={formData.quantidade}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Status</label>
            <select name="status" value={formData.status} onChange={handleChange}>
              <option value="ativo">Ativo</option>
              <option value="inativo">Inativo</option>
            </select>
          </div>

          <div className="form-group">
            <label>Imagem (URL)</label>
            <input
              type="url"
              name="imagem"
              value={formData.imagem}
              onChange={handleChange}
            />
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? 'Salvando...' : 'Salvar'}
            </button>
            <button 
              type="button" 
              onClick={() => navigate('/products')}
              className="btn-secondary"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
