import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { productAPI, saleAPI } from '../services/api'
import './Dashboard.css'

export function Dashboard() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalStock: 0,
    totalSales: 0,
    totalRevenue: 0
  })
  const [loading, setLoading] = useState(true)
  const [products, setProducts] = useState([])
  const [sales, setSales] = useState([])

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [productsRes, salesRes] = await Promise.all([
        productAPI.list(),
        saleAPI.list()
      ])

      const productsData = productsRes.data || []
      const salesData = salesRes.data || []

      setProducts(productsData)
      setSales(salesData)

      // Calcula estatísticas
      const totalProducts = productsData.length
      const totalStock = productsData.reduce((sum, p) => sum + (p.quantidade || 0), 0)
      const totalSales = salesData.length
      const totalRevenue = salesData.reduce((sum, s) => sum + (parseFloat(s.preco_venda || 0) * (s.quantidade || 0)), 0)

      setStats({
        totalProducts,
        totalStock,
        totalSales,
        totalRevenue
      })
    } catch (err) {
      console.error('Erro ao carregar dados:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (loading) {
    return <div className="dashboard-loading">Carregando...</div>
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Dashboard</h1>
        <div className="user-info">
          <span>Bem-vindo, {user?.nome || 'Vendedor'}!</span>
          <button onClick={handleLogout} className="btn-logout">Sair</button>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button onClick={() => navigate('/products')} className="nav-btn">
          📦 Produtos
        </button>
        <button onClick={() => navigate('/product-form')} className="nav-btn">
          ➕ Novo Produto
        </button>
        <button onClick={() => navigate('/sale')} className="nav-btn">
          💳 Registrar Venda
        </button>
      </nav>

      <div className="dashboard-content">
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📦</div>
            <div className="stat-info">
              <p className="stat-label">Total de Produtos</p>
              <p className="stat-value">{stats.totalProducts}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-info">
              <p className="stat-label">Itens em Estoque</p>
              <p className="stat-value">{stats.totalStock}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">💳</div>
            <div className="stat-info">
              <p className="stat-label">Total de Vendas</p>
              <p className="stat-value">{stats.totalSales}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">💰</div>
            <div className="stat-info">
              <p className="stat-label">Receita Total</p>
              <p className="stat-value">R$ {stats.totalRevenue.toFixed(2)}</p>
            </div>
          </div>
        </div>

        <div className="dashboard-sections">
          <section className="section">
            <h2>Últimos Produtos Cadastrados</h2>
            {products.length === 0 ? (
              <p>Nenhum produto cadastrado ainda.</p>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Preço</th>
                    <th>Estoque</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {products.slice(0, 5).map((product) => (
                    <tr key={product.id}>
                      <td>{product.nome}</td>
                      <td>R$ {parseFloat(product.preco).toFixed(2)}</td>
                      <td>{product.quantidade}</td>
                      <td>
                        <span className={`status ${product.status}`}>
                          {product.status === 'ativo' ? '✓ Ativo' : '✗ Inativo'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>

          <section className="section">
            <h2>Últimas Vendas</h2>
            {sales.length === 0 ? (
              <p>Nenhuma venda registrada ainda.</p>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Data</th>
                    <th>Quantidade</th>
                    <th>Preço Unit.</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {sales.slice(0, 5).map((sale, index) => (
                    <tr key={index}>
                      <td>{new Date(sale.data_venda).toLocaleDateString('pt-BR')}</td>
                      <td>{sale.quantidade}</td>
                      <td>R$ {parseFloat(sale.preco_venda).toFixed(2)}</td>
                      <td>R$ {(parseFloat(sale.preco_venda) * sale.quantidade).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        </div>
      </div>
    </div>
  )
}
