import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ProtectedRoute from './components/common/ProtectedRoute';
import SubjectList from './components/subjects/SubjectList';
import ThemeList from './components/themes/ThemeList';
import QuestionList from './components/questions/QuestionList';

// Компонент Dashboard с навигацией
const Dashboard = () => {
  const { logout } = useAuth();
  
  // Состояния для навигации
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null);
  const [selectedSubjectName, setSelectedSubjectName] = useState<string>('');
  const [selectedTheme, setSelectedTheme] = useState<number | null>(null);
  const [selectedThemeName, setSelectedThemeName] = useState<string>('');
  const [view, setView] = useState<'subjects' | 'themes' | 'questions'>('subjects');

  // Переход к темам
  const handleSubjectSelect = (subjectId: number, subjectName: string) => {
    setSelectedSubject(subjectId);
    setSelectedSubjectName(subjectName);
    setSelectedTheme(null);
    setSelectedThemeName('');
    setView('themes');
  };

  // Переход к вопросам
  const handleThemeSelect = (themeId: number, themeName: string) => {
    setSelectedTheme(themeId);
    setSelectedThemeName(themeName);
    setView('questions');
  };

  // Назад к предметам
  const handleBackToSubjects = () => {
    setSelectedSubject(null);
    setSelectedSubjectName('');
    setSelectedTheme(null);
    setSelectedThemeName('');
    setView('subjects');
  };

  // Назад к темам
  const handleBackToThemes = () => {
    setSelectedTheme(null);
    setSelectedThemeName('');
    setView('themes');
  };

  const handleQuestionSelect = (questionId: number) => {
    console.log('Selected question:', questionId);
    // Здесь позже добавим просмотр вопроса
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="container">
          <div className="header-content">
            <h1>LearnIt</h1>
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
          {view === 'subjects' && (
            <SubjectList onSubjectSelect={handleSubjectSelect} />
          )}
          
          {view === 'themes' && selectedSubject && (
            <ThemeList
              subjectId={selectedSubject}
              subjectName={selectedSubjectName}
              onBack={handleBackToSubjects}
              onThemeSelect={handleThemeSelect}
            />
          )}
          
          {view === 'questions' && selectedSubject && selectedTheme && (
            <QuestionList
              subjectId={selectedSubject}
              themeId={selectedTheme}
              themeName={selectedThemeName}
              subjectName={selectedSubjectName}
              onBack={handleBackToThemes}
              onQuestionSelect={handleQuestionSelect}
            />
          )}
        </div>
      </main>
    </div>
  );
};

// Страницы
const LoginPage = () => {
  const { login } = useAuth();
  return <Login onLogin={login} />;
};

const RegisterPage = () => {
  const { register } = useAuth();
  return <Register onRegister={register} />;
};

// Главный компонент
const App: React.FC = () => {
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