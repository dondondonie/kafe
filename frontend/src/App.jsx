import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Provider } from 'react-redux'
import { Toaster } from 'react-hot-toast'
import { GoogleOAuthProvider } from '@react-oauth/google'
import store from './store'

// Pages
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Menu from './pages/Menu'
import Inventory from './pages/Inventory'
import Orders from './pages/Orders'
import Reservations from './pages/Reservations'
import Customers from './pages/Customers'
import Analytics from './pages/Analytics'
import Employees from './pages/Employees'

// Layout
import MainLayout from './layout/MainLayout'

function App() {
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

  return (
    <Provider store={store}>
      <GoogleOAuthProvider clientId={googleClientId}>
        <Router>
          <Toaster position="top-right" />
          <Routes>
            <Route path="/login" element={<Login />} />
            
            <Route element={<MainLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/menu" element={<Menu />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/orders" element={<Orders />} />
              <Route path="/reservations" element={<Reservations />} />
              <Route path="/customers" element={<Customers />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/employees" element={<Employees />} />
            </Route>

            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </Router>
      </GoogleOAuthProvider>
    </Provider>
  )
}

export default App
