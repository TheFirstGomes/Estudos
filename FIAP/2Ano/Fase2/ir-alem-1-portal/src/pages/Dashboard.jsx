import { useMemo } from 'react'
import StatCard from '../components/StatCard.jsx'
import { useAppointments } from '../contexts/AppointmentsContext.jsx'
import { usePatients } from '../contexts/PatientsContext.jsx'
import { toLocalIsoDate } from '../services/appointmentService.js'
import styles from './Dashboard.module.css'

export default function Dashboard() {
  const { patients, loading, error } = usePatients()
  const { appointments } = useAppointments()

  const stats = useMemo(() => {
    const today = toLocalIsoDate()
    const byCondition = {}
    patients.forEach((p) => {
      byCondition[p.condition] = (byCondition[p.condition] ?? 0) + 1
    })
    return {
      highRisk: patients.filter((p) => p.highRisk).length,
      upcoming: appointments.filter((a) => a.date >= today).length,
      today: appointments.filter((a) => a.date === today).length,
      byCondition: Object.entries(byCondition).sort((a, b) => b[1] - a[1]),
    }
  }, [patients, appointments])

  if (error) return <p role="alert">Não foi possível carregar os pacientes.</p>

  const max = Math.max(1, ...stats.byCondition.map(([, n]) => n))

  return (
    <>
      <h1>Dashboard</h1>
      <div className={styles.grid}>
        <StatCard label="Pacientes" value={loading ? '…' : patients.length} />
        <StatCard label="Consultas agendadas" value={appointments.length} hint={`${stats.upcoming} futuras`} tone="ok" />
        <StatCard label="Consultas hoje" value={stats.today} tone="warn" />
        <StatCard label="Pacientes de alto risco" value={loading ? '…' : stats.highRisk} tone="danger" hint="Marcação simulada" />
      </div>

      <section className={styles.panel}>
        <h2>Pacientes por condição</h2>
        {stats.byCondition.map(([name, n]) => (
          <div key={name} className={styles.barRow}>
            <span className={styles.barLabel}>{name}</span>
            <div className={styles.barTrack}>
              <div className={styles.bar} style={{ width: `${(n / max) * 100}%` }} />
            </div>
            <span className={styles.barValue}>{n}</span>
          </div>
        ))}
      </section>
    </>
  )
}
