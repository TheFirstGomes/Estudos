import { createContext, useContext, useEffect, useState } from 'react'
import { fetchPatients } from '../services/patientService.js'

const PatientsContext = createContext(null)

// Só é montado dentro das rotas protegidas: a busca ocorre somente após o login.
export function PatientsProvider({ children }) {
  const [state, setState] = useState({ patients: [], source: null, loading: true, error: null })

  useEffect(() => {
    const controller = new AbortController()
    fetchPatients(controller.signal)
      .then(({ patients, source }) => setState({ patients, source, loading: false, error: null }))
      .catch((error) => {
        if (error.name !== 'AbortError') setState({ patients: [], source: null, loading: false, error })
      })
    return () => controller.abort()
  }, [])

  return <PatientsContext.Provider value={state}>{children}</PatientsContext.Provider>
}

export function usePatients() {
  const ctx = useContext(PatientsContext)
  if (!ctx) throw new Error('usePatients deve ser usado dentro de <PatientsProvider>')
  return ctx
}
