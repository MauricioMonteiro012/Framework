import React, { createContext, useState, useEffect } from 'react'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(null)

  // Carrega token do localStorage ao iniciar
  useEffect(() => {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      setToken(savedToken)
      try {
        const userData = JSON.parse(localStorage.getItem('user') || '{}')
        setUser(userData)
      } catch (e) {
        console.error('Erro ao restaurar usuário:', e)
      }
    }
    setLoading(false)
  }, [])

  const login = (userData, authToken) => {
    setUser(userData)
    setToken(authToken)
    localStorage.setItem('token', authToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return React.useContext(AuthContext)
}
