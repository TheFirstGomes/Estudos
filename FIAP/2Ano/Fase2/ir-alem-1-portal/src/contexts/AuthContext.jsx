import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import * as authService from '../services/authService.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  // Lazy initializer: restaura a sessão a partir do token salvo (se ainda válido).
  const [user, setUser] = useState(() => {
    const token = authService.getStoredToken()
    return token ? authService.decodeToken(token) : null
  })

  const login = useCallback(async (email, password) => {
    const token = await authService.login(email, password)
    setUser(authService.decodeToken(token))
  }, [])

  const logout = useCallback(() => {
    authService.logout()
    setUser(null)
  }, [])

  // Encerra a sessão automaticamente quando o token expira.
  useEffect(() => {
    if (!user) return undefined
    const ms = user.exp * 1000 - Date.now()
    const id = setTimeout(logout, Math.max(ms, 0))
    return () => clearTimeout(id)
  }, [user, logout])

  const value = useMemo(() => ({ user, isAuthenticated: !!user, login, logout }), [user, login, logout])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth deve ser usado dentro de <AuthProvider>')
  return ctx
}
