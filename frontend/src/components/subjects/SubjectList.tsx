import React, { useState, useEffect } from 'react';
import { subjectsAPI } from '../../api/subjects.js';

interface Subject {
  id: number;
  name: string;
  order: number;
}

interface SubjectListProps {
  onSubjectSelect?: (subjectId: number, subjectName: string) => void;
}

const SubjectList: React.FC<SubjectListProps> = ({ onSubjectSelect }) => {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newSubjectName, setNewSubjectName] = useState('');
  const [creating, setCreating] = useState(false);

  const loadSubjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await subjectsAPI.list();
      setSubjects(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки предметов');
      console.error('Error loading subjects:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSubjects();
  }, []);

  const handleCreateSubject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSubjectName.trim()) return;

    try {
      setCreating(true);
      const newSubject = await subjectsAPI.create({ name: newSubjectName.trim() });
      setSubjects([...subjects, newSubject]);
      setNewSubjectName('');
      setShowCreateForm(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания предмета');
      console.error('Error creating subject:', err);
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteSubject = async (subjectId: number, subjectName: string) => {
    if (!window.confirm(`Вы уверены, что хотите удалить предмет "${subjectName}"?`)) {
      return;
    }

    try {
      await subjectsAPI.delete(subjectId);
      setSubjects(subjects.filter(s => s.id !== subjectId));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка удаления предмета');
      console.error('Error deleting subject:', err);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader">Загрузка...</div>
      </div>
    );
  }

  return (
    <div className="subject-list-container">
      <div className="subject-list-header">
        <h2>Предметы</h2>
        <button
          className="btn btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Отмена' : '+ Добавить предмет'}
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
          <form onSubmit={handleCreateSubject}>
            <div className="form-row">
              <div className="form-group" style={{ flex: 1 }}>
                <input
                  type="text"
                  placeholder="Введите название предмета"
                  value={newSubjectName}
                  onChange={(e) => setNewSubjectName(e.target.value)}
                  autoFocus
                  disabled={creating}
                />
              </div>
              <button
                type="submit"
                className="btn btn-success"
                disabled={creating || !newSubjectName.trim()}
              >
                {creating ? 'Создание...' : 'Создать'}
              </button>
            </div>
          </form>
        </div>
      )}

      {subjects.length === 0 ? (
        <div className="empty-state">
          <p>Нет предметов. Создайте первый предмет!</p>
        </div>
      ) : (
        <div className="subject-grid">
          {subjects.map((subject) => (
            <div key={subject.id} className="subject-card">
              <div 
                className="subject-card-content"
                onClick={() => onSubjectSelect && onSubjectSelect(subject.id, subject.name)}
                style={{ cursor: onSubjectSelect ? 'pointer' : 'default' }}
              >
                <div className="subject-name">{subject.name}</div>
                <div className="subject-order">Порядок: {subject.order}</div>
                <div className="subject-id">ID: {subject.id}</div>
              </div>
              <div className="subject-card-actions">
                <button
                  className="btn btn-danger btn-sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteSubject(subject.id, subject.name);
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

export default SubjectList;