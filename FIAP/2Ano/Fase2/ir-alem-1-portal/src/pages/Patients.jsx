import { useMemo, useState } from 'react'
import { usePatients } from '../contexts/PatientsContext.jsx'
import styles from './Patients.module.css'

export default function Patients() {
  const { patients, source, loading, error } = usePatients()
  const [query, setQuery] = useState('')

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return q ? patients.filter((p) => p.name.toLowerCase().includes(q) || p.condition.toLowerCase().includes(q)) : patients
  }, [patients, query])

  if (loading) return <p role="status">Carregando pacientes…</p>
  if (error) return <p role="alert">Não foi possível carregar os pacientes.</p>

  return (
    <>
      <h1>Pacientes</h1>
      <p className={styles.source}>
        Fonte dos dados:{' '}
        {source === 'api' ? 'API pública JSONPlaceholder' : 'arquivo JSON local (API indisponível)'} · dados simulados
      </p>
      <input
        type="search"
        className={styles.search}
        placeholder="Buscar por nome ou condição…"
        aria-label="Buscar pacientes"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <div className={styles.grid}>
        {filtered.map((p) => (
          <article key={p.id} className={styles.card}>
            <header className={styles.cardHead}>
              <h2>{p.name}</h2>
              {p.highRisk && <span className={styles.badge}>Alto risco</span>}
            </header>
            <p className={styles.cond}>{p.condition}</p>
            <dl className={styles.meta}>
              <dt>Idade</dt>
              <dd>{p.age} anos</dd>
              <dt>Cidade</dt>
              <dd>{p.city}</dd>
              <dt>E-mail</dt>
              <dd>{p.email}</dd>
              <dt>Telefone</dt>
              <dd>{p.phone}</dd>
            </dl>
          </article>
        ))}
      </div>
      {filtered.length === 0 && <p>Nenhum paciente encontrado.</p>}
    </>
  )
}
