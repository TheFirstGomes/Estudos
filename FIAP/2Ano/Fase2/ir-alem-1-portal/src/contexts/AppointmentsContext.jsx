import { createContext, useContext, useEffect, useMemo, useReducer } from 'react'
import { loadAppointments, saveAppointments } from '../services/appointmentService.js'

const AppointmentsContext = createContext(null)

function appointmentsReducer(state, action) {
  switch (action.type) {
    case 'ADD':
      return [...state, { ...action.appointment, id: crypto.randomUUID() }]
    case 'REMOVE':
      return state.filter((a) => a.id !== action.id)
    default:
      return state
  }
}

export function AppointmentsProvider({ children }) {
  const [appointments, dispatch] = useReducer(appointmentsReducer, undefined, loadAppointments)

  useEffect(() => {
    saveAppointments(appointments)
  }, [appointments])

  const value = useMemo(
    () => ({
      appointments,
      addAppointment: (appointment) => dispatch({ type: 'ADD', appointment }),
      removeAppointment: (id) => dispatch({ type: 'REMOVE', id }),
    }),
    [appointments],
  )
  return <AppointmentsContext.Provider value={value}>{children}</AppointmentsContext.Provider>
}

export function useAppointments() {
  const ctx = useContext(AppointmentsContext)
  if (!ctx) throw new Error('useAppointments deve ser usado dentro de <AppointmentsProvider>')
  return ctx
}
