import { Link } from 'react-router-dom';

export default function Navigation() {
  return (
    <nav style={{ padding: '10px', background: '#f0f0f0', marginBottom: '20px', display: 'flex', gap: '15px' }}>
      <Link to="/">Интерфейс Кандидата</Link>
      <Link to="/recruiter">Панель Рекрутера</Link>
      <Link to="/admin">Панель Админа</Link>
    </nav>
  );
}