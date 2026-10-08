import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import { PatientsProvider } from '../contexts/PatientsContext.jsx'
import { AppointmentsProvider } from '../contexts/AppointmentsContext.jsx'

// Rota protegida: sem sessão válida, redireciona ao login. Os providers de dados
// só são montados após a autenticação — nenhum dado é buscado/exibido antes disso.
export default function ProtectedRoute() {
  const { isAuthenticated } = useAuth()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  return (
    <PatientsProvider>
      <AppointmentsProvider>
        <Outlet />
      </AppointmentsProvider>
    </PatientsProvider>
  )
}
