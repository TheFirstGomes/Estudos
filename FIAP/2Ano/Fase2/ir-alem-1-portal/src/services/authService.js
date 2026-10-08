// Autenticação SIMULADA: não existe back-end. O "JWT" é gerado no navegador
// e NÃO tem validade de segurança alguma (a assinatura é falsa).
const TOKEN_KEY = 'cardioia.token'
const TTL_SECONDS = 30 * 60

// Credenciais de demonstração (exibidas na tela de login).
export const DEMO_USER = { email: 'demo@cardioia.com', password: 'cardioia123', name: 'Dra. Demo' }

const toB64url = (obj) =>
  btoa(unescape(encodeURIComponent(JSON.stringify(obj))))
    .replace(/=+$/, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')

const fromB64url = (str) => {
  const b64 = str.replace(/-/g, '+').replace(/_/g, '/')
  return JSON.parse(decodeURIComponent(escape(atob(b64))))
}

export function createFakeJwt(user) {
  const now = Math.floor(Date.now() / 1000)
  const header = toB64url({ alg: 'none', typ: 'JWT' })
  const payload = toB64url({ sub: user.email, name: user.name, iat: now, exp: now + TTL_SECONDS })
  return `${header}.${payload}.assinatura-falsa`
}

// Retorna o payload se o token for legível e não estiver expirado; senão, null.
export function decodeToken(token) {
  try {
    const payload = fromB64url(token.split('.')[1])
    return payload.exp * 1000 > Date.now() ? payload : null
  } catch {
    return null
  }
}

export function login(email, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (email.trim().toLowerCase() === DEMO_USER.email && password === DEMO_USER.password) {
        const token = createFakeJwt(DEMO_USER)
        try {
          localStorage.setItem(TOKEN_KEY, token)
        } catch {
          /* armazenamento indisponível: a sessão vale só até recarregar */
        }
        resolve(token)
      } else {
        reject(new Error('E-mail ou senha inválidos.'))
      }
    }, 400) // simula latência de rede
  })
}

export function getStoredToken() {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function logout() {
  try {
    localStorage.removeItem(TOKEN_KEY)
  } catch {
    /* ignore */
  }
}
