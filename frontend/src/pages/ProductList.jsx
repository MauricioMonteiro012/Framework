import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { productAPI } from '../services/api'
import './Products.css'

export function ProductList() {
  const navigate = useNavigate()
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      const response = await productAPI.list()
      setProducts(response.data || [])
    } catch (err) {
      setError('Erro ao carregar produtos')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Deseja inativar este produto?')) {
      try {
        await productAPI.delete(id)
        loadProducts()
      } catch (err) {
        alert('Erro ao inativar produto')
      }
    }
  }

  return (
    <div className="products-container">
      <div className="products-header">
        <h2>Meus Produtos</h2>
        <button onClick={() => navigate('/product-form')} className="btn-primary">
          + Novo Produto
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
      {loading && <p>Carregando...</p>}

      {!loading && products.length === 0 && (
        <p className="empty-state">Nenhum produto cadastrado. Comece criando um!</p>
      )}

      <div className="products-grid">
        {products.map((product) => (
          <div key={product.id} className="product-card">
            {product.imagem && (
              <img src={product.imagem} alt={product.nome} className="product-image" />
            )}
            <div className="product-info">
              <h3>{product.nome}</h3>
              <p className="product-price">R$ {parseFloat(product.preco).toFixed(2)}</p>
              <p className="product-stock">Estoque: {product.quantidade}</p>
              <p className={`product-status ${product.status}`}>
                {product.status === 'ativo' ? '✓ Ativo' : '✗ Inativo'}
              </p>
              <div className="product-actions">
                <button 
                  onClick={() => navigate(`/product-form/${product.id}`)}
                  className="btn-secondary"
                >
                  Editar
                </button>
                <button 
                  onClick={() => handleDelete(product.id)}
                  className="btn-danger"
                >
                  Inativar
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
