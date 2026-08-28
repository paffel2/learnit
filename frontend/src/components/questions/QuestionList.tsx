import React, { useState, useEffect } from 'react';
import { questionsAPI } from '../../api/questions.js';

interface Question {
  id: number;
  name: string;
  text: string;
  content: string;
  order: number;
  is_deleted?: boolean;
}

interface QuestionListProps {
  subjectId: number;
  themeId: number;
  themeName: string;
  subjectName: string;
  onBack: () => void;
  onQuestionSelect?: (questionId: number) => void;
}

const QuestionList: React.FC<QuestionListProps> = ({
  subjectId,
  themeId,
  themeName,
  subjectName,
  onBack,
  onQuestionSelect,
}) => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newQuestion, setNewQuestion] = useState({
    name: '',
    text: '',
    content: '',
    order: 0,
    is_deleted: false,
  });
  const [creating, setCreating] = useState(false);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await questionsAPI.list(subjectId, themeId);
      setQuestions(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки вопросов');
      console.error('Error loading questions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQuestions();
  }, [subjectId, themeId]);

  const handleCreateQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newQuestion.name.trim() || !newQuestion.text.trim()) return;

    try {
      setCreating(true);
      const questionData = {
        name: newQuestion.name.trim(),
        text: newQuestion.text.trim(),
        content: newQuestion.content.trim() || 'Описание вопроса',
        order: questions.length + 1,
        is_deleted: false,
      };
      
      const created = await questionsAPI.create(subjectId, themeId, questionData);
      setQuestions([...questions, created]);
      setNewQuestion({ name: '', text: '', content: '', order: 0, is_deleted: false });
      setShowCreateForm(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания вопроса');
      console.error('Error creating question:', err);
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteQuestion = async (questionId: number, questionName: string) => {
    if (!window.confirm(`Вы уверены, что хотите удалить вопрос "${questionName}"?`)) {
      return;
    }

    try {
      await questionsAPI.delete(subjectId, themeId, questionId);
      setQuestions(questions.filter(q => q.id !== questionId));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка удаления вопроса');
      console.error('Error deleting question:', err);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader">Загрузка вопросов...</div>
      </div>
    );
  }

  return (
    <div className="question-list-container">
      <div className="question-list-header">
        <div className="header-left">
          <button 
            className="btn btn-secondary btn-sm" 
            onClick={onBack}
          >
            ← Назад к темам
          </button>
          <div>
            <h2>Вопросы: {themeName}</h2>
            <p className="breadcrumb">{subjectName} / {themeName}</p>
          </div>
        </div>
        <button
          className="btn btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Отмена' : '+ Добавить вопрос'}
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
          <form onSubmit={handleCreateQuestion}>
            <div className="form-group">
              <label>Название вопроса *</label>
              <input
                type="text"
                placeholder="Например: Основы React"
                value={newQuestion.name}
                onChange={(e) => setNewQuestion({ ...newQuestion, name: e.target.value })}
                disabled={creating}
                required
              />
            </div>
            <div className="form-group">
              <label>Текст вопроса *</label>
              <input
                type="text"
                placeholder="Введите текст вопроса"
                value={newQuestion.text}
                onChange={(e) => setNewQuestion({ ...newQuestion, text: e.target.value })}
                disabled={creating}
                required
              />
            </div>
            <div className="form-group">
              <label>Содержание (опционально)</label>
              <textarea
                placeholder="Подробное описание или подсказка"
                value={newQuestion.content}
                onChange={(e) => setNewQuestion({ ...newQuestion, content: e.target.value })}
                disabled={creating}
                rows={3}
              />
            </div>
            <div className="form-actions">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setShowCreateForm(false)}
                disabled={creating}
              >
                Отмена
              </button>
              <button
                type="submit"
                className="btn btn-success"
                disabled={creating || !newQuestion.name.trim() || !newQuestion.text.trim()}
              >
                {creating ? 'Создание...' : 'Создать вопрос'}
              </button>
            </div>
          </form>
        </div>
      )}

      {questions.length === 0 ? (
        <div className="empty-state">
          <p>Нет вопросов. Создайте первый вопрос!</p>
        </div>
      ) : (
        <div className="question-grid">
          {questions.map((question) => (
            <div 
              key={question.id} 
              className="question-card"
              onClick={() => onQuestionSelect && onQuestionSelect(question.id)}
            >
              <div className="question-card-content">
                <div className="question-name">{question.name}</div>
                <div className="question-text">{question.text}</div>
                {question.content && (
                  <div className="question-content">{question.content}</div>
                )}
                <div className="question-order">Порядок: {question.order}</div>
                <div className="question-id">ID: {question.id}</div>
              </div>
              <div className="question-card-actions">
                <button
                  className="btn btn-danger btn-sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteQuestion(question.id, question.name);
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

export default QuestionList;