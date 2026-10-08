import AppointmentForm from '../components/AppointmentForm.jsx'
import AppointmentList from '../components/AppointmentList.jsx'
import styles from './Appointments.module.css'

export default function Appointments() {
  return (
    <>
      <h1>Agendamentos</h1>
      <div className={styles.layout}>
        <AppointmentForm />
        <AppointmentList />
      </div>
    </>
  )
}
