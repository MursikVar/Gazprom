import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from 'react-router-dom';

const CORRECT_LOGIN = 'admin';
const CORRECT_PASSWORD = 'root'; 

function LoginAdmin() {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();
  
    const handleSubmit = (e) => {
      e.preventDefault();
      
      if (login === CORRECT_LOGIN && password === CORRECT_PASSWORD) {
        setIsAuthenticated(true);
        navigate('/adminPanel');
      } else {
        setError('Неверный логин или пароль');
      }
    };
  
    if (isAuthenticated) {
      return <Navigate to="/adminPanel" />;
    }
  
    return (
      <div className='adminPanel__wrapper' style={{
          padding: '40px 32px',
          maxWidth: '400px',
          margin: '50px auto',
          backgroundColor: '#fff',
          borderRadius: '16px',
          boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.1)',
      }}>
          

          <form onSubmit={handleSubmit} style={{ width: '100%' }}>
              <div style={{ marginBottom: '24px' }}>
                  <label style={{
                      display: 'block',
                      fontSize: '14px',
                      color: '#636E72',
                      marginBottom: '8px'
                  }}>
                      Логин
                  </label>
                  <input
                      type="text"
                      value={login}
                      onChange={(e) => setLogin(e.target.value)}
                      style={{
                          width: '100%',
                          padding: '12px 16px',
                          border: '1px solid #DFE6E9',
                          borderRadius: '8px',
                          fontSize: '16px',
                          transition: 'all 0.3s',
                          outline: 'none'
                      }}
                      placeholder="Введите ваш логин"
                  />
              </div>

              <div style={{ marginBottom: '32px' }}>
                  <label style={{
                      display: 'block',
                      fontSize: '14px',
                      color: '#636E72',
                      marginBottom: '8px'
                  }}>
                      Пароль
                  </label>
                  <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      style={{
                          width: '100%',
                          padding: '12px 16px',
                          border: '1px solid #DFE6E9',
                          borderRadius: '8px',
                          fontSize: '16px',
                          transition: 'all 0.3s',
                          outline: 'none'
                      }}
                      placeholder="Введите пароль"
                  />
              </div>

              <button 
                  type="submit"
                  style={{
                      width: '100%',
                      padding: '14px',
                      backgroundColor: '#0984E3',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      fontSize: '16px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      transition: 'background-color 0.3s',
                      marginBottom: '16px'
                  }}
                  onMouseOver={(e) => e.target.style.backgroundColor = '#0873C4'}
                  onMouseOut={(e) => e.target.style.backgroundColor = '#0984E3'}
              >
                  Войти
              </button>

              {error && <div style={{
                  color: '#D63031',
                  fontSize: '14px',
                  textAlign: 'center',
                  padding: '12px',
                  backgroundColor: '#FFE4E3',
                  borderRadius: '8px',
                  marginTop: '16px'
              }}>
                  {error}
              </div>}
          </form>
      </div>
  );
  }


export {LoginAdmin};
