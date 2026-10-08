const KEY = 'cardioia.appointments'

export const APPOINTMENT_TYPES = ['Consulta', 'Retorno', 'Eletrocardiograma', 'Ecocardiograma', 'Teste ergométrico']

// Data local no formato AAAA-MM-DD (evita o deslocamento de fuso do toISOString).
export function toLocalIsoDate(date = new Date()) {
  const pad = (n) => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`
}

const inDays = (n) => {
  const d = new Date()
  d.setDate(d.getDate() + n)
  return toLocalIsoDate(d)
}

const SEED = [
  { id: 'seed-1', patientId: 3, date: inDays(1), time: '09:00', type: 'Consulta', notes: 'Primeira avaliação.' },
  { id: 'seed-2', patientId: 5, date: inDays(2), time: '14:30', type: 'Eletrocardiograma', notes: '' },
  { id: 'seed-3', patientId: 9, date: inDays(5), time: '10:15', type: 'Retorno', notes: 'Trazer exames anteriores.' },
]

export function loadAppointments() {
  try {
    const raw = localStorage.getItem(KEY)
    if (raw) return JSON.parse(raw)
  } catch {
    /* cai no seed */
  }
  return SEED
}

export function saveAppointments(list) {
  try {
    localStorage.setItem(KEY, JSON.stringify(list))
  } catch {
    /* ignore */
  }
}
