import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Register = ({ onRegister }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    repeated_password: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

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
    if (!formData.email) newErrors.email = 'Email обязателен';
    if (!formData.username) newErrors.username = 'Имя пользователя обязательно';
    if (formData.password.length < 6) {
      newErrors.password = 'Пароль должен быть не менее 6 символов';
    }
    if (formData.password !== formData.repeated_password) {
      newErrors.repeated_password = 'Пароли не совпадают';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    const result = await onRegister(formData);
    setLoading(false);

    if (result.success) {
      navigate('/login', { 
        state: { message: 'Регистрация успешна! Теперь войдите в систему.' }
      });
    } else {
      setErrors({ general: result.error });
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <h2>Регистрация</h2>
          <p>
            Или <Link to="/login">войдите в существующий аккаунт</Link>
          </p>
        </div>

        {errors.general && (
          <div className="alert alert-danger">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="Введите email"
              value={formData.email}
              onChange={handleChange}
            />
            {errors.email && <div className="error">{errors.email}</div>}
          </div>
          
          <div className="form-group">
            <label htmlFor="username">Имя пользователя</label>
            <input
              id="username"
              name="username"
              type="text"
              placeholder="Введите имя пользователя"
              value={formData.username}
              onChange={handleChange}
            />
            {errors.username && <div className="error">{errors.username}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Введите пароль (мин. 6 символов)"
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && <div className="error">{errors.password}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="repeated_password">Подтверждение пароля</label>
            <input
              id="repeated_password"
              name="repeated_password"
              type="password"
              placeholder="Повторите пароль"
              value={formData.repeated_password}
              onChange={handleChange}
            />
            {errors.repeated_password && <div className="error">{errors.repeated_password}</div>}
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-block"
            disabled={loading}
          >
            {loading ? 'Регистрация...' : 'Зарегистрироваться'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;