import { Link } from 'react-router-dom';

export default function Navigation() {
  const style = {
    padding: '10px 20px',
    borderRadius: '10px',
    background: 'rgba(255,255,255,0.1)',
    textDecoration: 'none',
    color: 'white',
    fontWeight: 'bold'
  };

  return (
    <nav style={{
      display: 'flex',
      justifyContent: 'center',
      gap: '15px',
      padding: '20px',
      background: 'rgba(0,0,0,0.3)'
    }}>
      <Link style={style} to="/">Главная</Link>
      <Link style={style} to="/tests">Тесты</Link>
      <Link style={style} to="/vacancies">Вакансии</Link>
      <Link style={style} to="/applications">Отклики</Link>
      <Link style={style} to="/profile">Профиль</Link>
    </nav>
  );
}