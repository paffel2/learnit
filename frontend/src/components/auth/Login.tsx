import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

const Login = ({ onLogin }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [successMessage] = useState(location.state?.message || '');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.email && !formData.username) {
      newErrors.general = 'Укажите email или имя пользователя';
    }
    if (!formData.password) {
      newErrors.password = 'Введите пароль';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    const credentials = { password: formData.password };
    
    if (formData.email) credentials.email = formData.email;
    if (formData.username) credentials.username = formData.username;

    const result = await onLogin(credentials);
    setLoading(false);

    if (result.success) {
      navigate('/');
    } else {
      setErrors({ general: result.error });
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <h2>Вход в систему</h2>
          <p>
            Или <Link to="/register">зарегистрируйтесь</Link>
          </p>
        </div>

        {successMessage && (
          <div className="alert alert-success">
            {successMessage}
          </div>
        )}

        {errors.general && (
          <div className="alert alert-danger">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email (опционально)</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="Введите email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="username">Имя пользователя (опционально)</label>
            <input
              id="username"
              name="username"
              type="text"
              placeholder="Введите имя пользователя"
              value={formData.username}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Введите пароль"
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && (
              <div className="error">{errors.password}</div>
            )}
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-block"
            disabled={loading}
          >
            {loading ? 'Вход...' : 'Войти'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;