import React, { useState, useEffect } from 'react'
import { productAPI, saleAPI } from '../services/api'
import './Sales.css'

export function SaleForm() {
  const [products, setProducts] = useState([])
  const [formData, setFormData] = useState({
    produto_id: '',
    quantidade: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      const response = await productAPI.list()
      const activeProducts = (response.data || []).filter(p => p.status === 'ativo')
      setProducts(activeProducts)
    } catch (err) {
      setError('Erro ao carregar produtos')
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      await saleAPI.create(formData)
      setSuccess('Venda registrada com sucesso!')
      setFormData({ produto_id: '', quantidade: '' })
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.mensagem || 'Erro ao registrar venda')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="sales-container">
      <div className="sales-card">
        <h2>Registrar Venda</h2>
        
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Produto</label>
            <select
              name="produto_id"
              value={formData.produto_id}
              onChange={handleChange}
              required
            >
              <option value="">Selecione um produto</option>
              {products.map((product) => (
                <option key={product.id} value={product.id}>
                  {product.nome} (Est: {product.quantidade})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Quantidade</label>
            <input
              type="number"
              name="quantidade"
              value={formData.quantidade}
              onChange={handleChange}
              min="1"
              required
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Registrando...' : 'Registrar Venda'}
          </button>
        </form>
      </div>
    </div>
  )
}
