import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'

// Pages
import { Register } from './pages/Register'
import { Activation } from './pages/Activation'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'
import { ProductList } from './pages/ProductList'
import { ProductForm } from './pages/ProductForm'
import { SaleForm } from './pages/SaleForm'

import './App.css'

function AppRoutes() {
  const { user, loading } = useAuth()

  if (loading) {
    return <div style={{textAlign:'center', padding:'50px'}}>Carregando...</div>
  }

  return (
    <Routes>
      {/* Rotas públicas */}
      <Route path="/register" element={<Register />} />
      <Route path="/ativacao" element={<Activation />} />
      <Route path="/login" element={<Login />} />

      {/* Rotas protegidas */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      <Route path="/products" element={
        <ProtectedRoute>
          <ProductList />
        </ProtectedRoute>
      } />
      <Route path="/product-form" element={
        <ProtectedRoute>
          <ProductForm />
        </ProtectedRoute>
      } />
      <Route path="/product-form/:id" element={
        <ProtectedRoute>
          <ProductForm />
        </ProtectedRoute>
      } />
      <Route path="/sale" element={
        <ProtectedRoute>
          <SaleForm />
        </ProtectedRoute>
      } />

      {/* Rota padrão */}
      <Route path="/" element={
        user ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />
      } />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}
