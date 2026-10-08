import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import styles from './Layout.module.css'

const links = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/pacientes', label: 'Pacientes' },
  { to: '/agendamentos', label: 'Agendamentos' },
]

export default function Layout() {
  const { user, logout } = useAuth()

  return (
    <div className={styles.shell}>
      <header className={styles.header}>
        <div className={styles.brand}>
          <span aria-hidden="true">♥</span> CardioIA
        </div>
        <nav className={styles.nav} aria-label="Navegação principal">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              className={({ isActive }) => (isActive ? `${styles.link} ${styles.active}` : styles.link)}
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className={styles.user}>
          <span>{user?.name}</span>
          <button type="button" className={styles.logout} onClick={logout}>
            Sair
          </button>
        </div>
      </header>
      <main className={styles.main}>
        <Outlet />
      </main>
      <footer className={styles.footer}>
        Protótipo educacional — dados simulados. Não utilizar para fins clínicos.
      </footer>
    </div>
  )
}
