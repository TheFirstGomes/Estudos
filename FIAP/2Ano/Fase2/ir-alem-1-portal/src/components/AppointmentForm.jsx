import { useReducer, useState } from 'react'
import { useAppointments } from '../contexts/AppointmentsContext.jsx'
import { usePatients } from '../contexts/PatientsContext.jsx'
import { APPOINTMENT_TYPES, toLocalIsoDate } from '../services/appointmentService.js'
import styles from './AppointmentForm.module.css'

const initialForm = { patientId: '', date: '', time: '', type: APPOINTMENT_TYPES[0], notes: '' }

// useReducer: os campos do formulário mudam juntos e o reset é uma ação única.
function formReducer(state, action) {
  switch (action.type) {
    case 'SET_FIELD':
      return { ...state, [action.field]: action.value }
    case 'RESET':
      return initialForm
    default:
      return state
  }
}

function validate(form) {
  const errors = {}
  if (!form.patientId) errors.patientId = 'Selecione um paciente.'
  if (!form.date) errors.date = 'Informe a data.'
  if (!form.time) errors.time = 'Informe o horário.'
  if (form.date && form.time) {
    const when = new Date(`${form.date}T${form.time}`)
    if (when.getTime() < Date.now()) errors.date = 'O agendamento deve ser no futuro.'
  }
  return errors
}

export default function AppointmentForm() {
  const { patients, loading } = usePatients()
  const { addAppointment } = useAppointments()
  const [form, dispatch] = useReducer(formReducer, initialForm)
  // useState: estado de interface (erros e mensagem de sucesso), independente dos campos.
  const [errors, setErrors] = useState({})
  const [success, setSuccess] = useState('')

  const onChange = (e) => {
    dispatch({ type: 'SET_FIELD', field: e.target.name, value: e.target.value })
    setSuccess('')
  }

  const onSubmit = (e) => {
    e.preventDefault()
    const found = validate(form)
    setErrors(found)
    if (Object.keys(found).length > 0) return
    addAppointment({ ...form, patientId: Number(form.patientId) })
    dispatch({ type: 'RESET' })
    setSuccess('Consulta agendada com sucesso!')
  }

  return (
    <form className={styles.form} onSubmit={onSubmit} noValidate>
      <h2>Novo agendamento</h2>

      <label className={styles.field}>
        Paciente
        <select name="patientId" value={form.patientId} onChange={onChange} disabled={loading} aria-invalid={!!errors.patientId}>
          <option value="">{loading ? 'Carregando pacientes…' : 'Selecione…'}</option>
          {patients.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        {errors.patientId && <span className={styles.error}>{errors.patientId}</span>}
      </label>

      <div className={styles.row}>
        <label className={styles.field}>
          Data
          <input type="date" name="date" min={toLocalIsoDate()} value={form.date} onChange={onChange} aria-invalid={!!errors.date} />
          {errors.date && <span className={styles.error}>{errors.date}</span>}
        </label>
        <label className={styles.field}>
          Horário
          <input type="time" name="time" value={form.time} onChange={onChange} aria-invalid={!!errors.time} />
          {errors.time && <span className={styles.error}>{errors.time}</span>}
        </label>
      </div>

      <label className={styles.field}>
        Tipo
        <select name="type" value={form.type} onChange={onChange}>
          {APPOINTMENT_TYPES.map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
      </label>

      <label className={styles.field}>
        Observações
        <textarea name="notes" rows={3} value={form.notes} onChange={onChange} />
      </label>

      <button type="submit" className={styles.submit}>
        Agendar
      </button>
      {success && (
        <p className={styles.success} role="status">
          {success}
        </p>
      )}
    </form>
  )
}
