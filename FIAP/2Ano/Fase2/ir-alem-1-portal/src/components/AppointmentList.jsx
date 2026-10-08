import { useMemo } from 'react'
import { useAppointments } from '../contexts/AppointmentsContext.jsx'
import { usePatients } from '../contexts/PatientsContext.jsx'
import styles from './AppointmentList.module.css'

const formatDate = (iso) => new Date(`${iso}T00:00`).toLocaleDateString('pt-BR')

export default function AppointmentList() {
  const { appointments, removeAppointment } = useAppointments()
  const { patients } = usePatients()

  const rows = useMemo(() => {
    const names = new Map(patients.map((p) => [p.id, p.name]))
    return [...appointments]
      .sort((a, b) => `${a.date}T${a.time}`.localeCompare(`${b.date}T${b.time}`))
      .map((a) => ({ ...a, patientName: names.get(a.patientId) ?? `Paciente #${a.patientId}` }))
  }, [appointments, patients])

  return (
    <section className={styles.box}>
      <h2>Consultas agendadas ({rows.length})</h2>
      {rows.length === 0 ? (
        <p className={styles.empty}>Nenhum agendamento ainda.</p>
      ) : (
        <ul className={styles.list}>
          {rows.map((a) => (
            <li key={a.id} className={styles.item}>
              <div>
                <strong>{a.patientName}</strong>
                <div className={styles.meta}>
                  {formatDate(a.date)} às {a.time} · {a.type}
                </div>
                {a.notes && <div className={styles.notes}>{a.notes}</div>}
              </div>
              <button
                type="button"
                className={styles.remove}
                onClick={() => removeAppointment(a.id)}
                aria-label={`Cancelar consulta de ${a.patientName}`}
              >
                Cancelar
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
