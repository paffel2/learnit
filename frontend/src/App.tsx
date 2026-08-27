import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ProtectedRoute from './components/common/ProtectedRoute';

const Dashboard = () => {
  const { logout, user } = useAuth();
  
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="container">
          <h1>LearnIt</h1>
          <div className="user-info">
            <span>Привет, {user?.username || 'Пользователь'}!</span>
            <button
              onClick={logout}
              className="btn btn-danger"
            >
              Выйти
            </button>
          </div>
        </div>
      </header>
      <main className="dashboard-content">
        <div className="container">
          <div className="dashboard-card">
            <h2>Добро пожаловать в LearnIt!</h2>
            <p>Здесь будет ваш контент...</p>
          </div>
        </div>
      </main>
    </div>
  );
};

const LoginPage = () => {
  const { login } = useAuth();
  return <Login onLogin={login} />;
};

const RegisterPage = () => {
  const { register } = useAuth();
  return <Register onRegister={register} />;
};

const App = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;