import localUsers from '../data/patients.json'

const API_URL = 'https://jsonplaceholder.typicode.com/users'
const CONDITIONS = [
  'Hipertensão arterial',
  'Arritmia cardíaca',
  'Insuficiência cardíaca',
  'Angina estável',
  'Pós-infarto',
  'Check-up de rotina',
]

// A API pública só traz dados cadastrais; idade e condição são derivadas do id
// de forma determinística, apenas para DEMONSTRAÇÃO (não são dados clínicos).
function toPatient(user) {
  const condition = CONDITIONS[user.id % CONDITIONS.length]
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    phone: user.phone,
    city: user.address?.city ?? '—',
    age: 35 + ((user.id * 7) % 45),
    condition,
    highRisk: condition !== 'Check-up de rotina' && user.id % 3 === 0,
  }
}

// Tenta a API pública; se estiver offline ou bloqueada, usa o JSON local.
export async function fetchPatients(signal) {
  try {
    const res = await fetch(API_URL, { signal })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return { patients: (await res.json()).map(toPatient), source: 'api' }
  } catch (err) {
    if (err.name === 'AbortError') throw err
    return { patients: localUsers.map(toPatient), source: 'local' }
  }
}
