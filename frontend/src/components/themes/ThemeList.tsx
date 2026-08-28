import React, { useState, useEffect } from 'react';
import { themesAPI } from '../../api/themes.js';

interface Theme {
  id: number;
  name: string;
  order: number;
  is_deleted?: boolean;
}

interface ThemeListProps {
  subjectId: number;
  subjectName: string;
  onBack: () => void;
  onThemeSelect?: (themeId: number, themeName: string) => void;
}

const ThemeList: React.FC<ThemeListProps> = ({ 
  subjectId, 
  subjectName, 
  onBack,
  onThemeSelect 
}) => {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newThemeName, setNewThemeName] = useState('');
  const [creating, setCreating] = useState(false);

  const loadThemes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await themesAPI.list(subjectId);
      setThemes(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки тем');
      console.error('Error loading themes:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadThemes();
  }, [subjectId]);

  const handleCreateTheme = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newThemeName.trim()) return;

    try {
      setCreating(true);
      const newTheme = await themesAPI.create(subjectId, { 
        name: newThemeName.trim() 
      });
      setThemes([...themes, newTheme]);
      setNewThemeName('');
      setShowCreateForm(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания темы');
      console.error('Error creating theme:', err);
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteTheme = async (themeId: number, themeName: string) => {
    if (!window.confirm(`Вы уверены, что хотите удалить тему "${themeName}"?`)) {
      return;
    }

    try {
      await themesAPI.delete(subjectId, themeId);
      setThemes(themes.filter(t => t.id !== themeId));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка удаления темы');
      console.error('Error deleting theme:', err);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader">Загрузка тем...</div>
      </div>
    );
  }

  return (
    <div className="theme-list-container">
      <div className="theme-list-header">
        <div className="header-left">
          <button 
            className="btn btn-secondary btn-sm" 
            onClick={onBack}
          >
            ← Назад к предметам
          </button>
          <h2>Темы: {subjectName}</h2>
        </div>
        <button
          className="btn btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Отмена' : '+ Добавить тему'}
        </button>
      </div>

      {error && (
        <div className="alert alert-danger">
          {error}
          <button 
            className="alert-close"
            onClick={() => setError(null)}
          >
            ×
          </button>
        </div>
      )}

      {showCreateForm && (
        <div className="create-form">
          <form onSubmit={handleCreateTheme}>
            <div className="form-row">
              <div className="form-group" style={{ flex: 1 }}>
                <input
                  type="text"
                  placeholder="Введите название темы"
                  value={newThemeName}
                  onChange={(e) => setNewThemeName(e.target.value)}
                  autoFocus
                  disabled={creating}
                />
              </div>
              <button
                type="submit"
                className="btn btn-success"
                disabled={creating || !newThemeName.trim()}
              >
                {creating ? 'Создание...' : 'Создать'}
              </button>
            </div>
          </form>
        </div>
      )}

      {themes.length === 0 ? (
        <div className="empty-state">
          <p>Нет тем. Создайте первую тему!</p>
        </div>
      ) : (
        <div className="theme-grid">
          {themes.map((theme) => (
            <div 
              key={theme.id} 
              className="theme-card"
              onClick={() => onThemeSelect && onThemeSelect(theme.id)}
            >
              <div 
                className="theme-card-content"
                onClick={() => onThemeSelect && onThemeSelect(theme.id, theme.name)}
                style={{ cursor: onThemeSelect ? 'pointer' : 'default' }}
              >
                <div className="theme-name">{theme.name}</div>
                <div className="theme-order">Порядок: {theme.order}</div>
                <div className="theme-id">ID: {theme.id}</div>
              </div>
              <div className="theme-card-actions">
                <button
                  className="btn btn-danger btn-sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteTheme(theme.id, theme.name);
                  }}
                >
                  Удалить
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ThemeList;