import { useState } from 'react';
interface User {
  name: string;
  phone: string;
  birthDate: string;
  citizenship: string;
}
interface Props {
  setUser: (u: User) => void;
  user: User | null;
}

export default function Home({ setUser, user }: Props) {
  const [show, setShow] = useState(false);
  const [form, setForm] = useState<User>({
    name: '',
    phone: '',
    birthDate: '',
    citizenship: ''
  });

  const register = (e: React.FormEvent) => {
    e.preventDefault();
    setUser(form);
    setShow(false);
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Работай с нами <span style={{ color: '#00ff00' }}>X5 Tech Team</span></h1>

      {!user && (
        <button onClick={() => setShow(true)} style={{ padding: 15, borderRadius: 20 }}>
          Log In
        </button>
      )}

      {show && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        }}>
          <form onSubmit={register} style={{ background: '#222', padding: 30, borderRadius: 20 }}>
            <input placeholder="ФИО" onChange={e => setForm({ ...form, name: e.target.value })} />
            <input placeholder="Телефон" onChange={e => setForm({ ...form, phone: e.target.value })} />
            <input type="date" onChange={e => setForm({ ...form, birthDate: e.target.value })} />
            <input placeholder="Гражданство" onChange={e => setForm({ ...form, citizenship: e.target.value })} />
            <button type="submit">Войти</button>
          </form>
        </div>
      )}
    </div>
  );
}