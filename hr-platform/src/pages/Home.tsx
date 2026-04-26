import { useState } from 'react';

export default function Home({ user, setUser }: { user:  any | null, setUser: any }) {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<User>({
    name: '',
    phone: '',
    birthDate: '',
    citizenship: ''
  });

  const news = [
    "X5 Tech внедряет AI в логистику",
    "Автоматизация складов увеличена на 40%",
    "Новые облачные решения X5 Cloud"
  ];

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Работай с нами <span style={{ color: '#00ff99' }}>X5 Tech Team</span></h1>

      {!user && (
        <button onClick={() => setOpen(true)} style={btn}>Log In</button>
      )}

      <div style={{ marginTop: 40 }}>
        {news.map((n, i) => (
          <div key={i} style={card}>{n}</div>
        ))}
      </div>

      {open && (
        <div style={overlay}>
          <div style={modal}>
            <h2>Регистрация</h2>
            <input placeholder="ФИО" onChange={e => setForm({...form, name: e.target.value})} style={input}/>
            <input placeholder="Телефон" onChange={e => setForm({...form, phone: e.target.value})} style={input}/>
            <input type="date" onChange={e => setForm({...form, birthDate: e.target.value})} style={input}/>
            <input placeholder="Гражданство" onChange={e => setForm({...form, citizenship: e.target.value})} style={input}/>
            <button onClick={() => {setUser(form); setOpen(false)}} style={btn}>Войти</button>
          </div>
        </div>
      )}
    </div>
  );
}

const btn = { padding: 15, background: '#00ff99', border: 'none', borderRadius: 10, cursor: 'pointer' };
const card = { margin: 10, padding: 20, background: 'rgba(255,255,255,0.05)', borderRadius: 10 };
const input = { padding: 10, margin: 5, width: '100%' };
const overlay = { position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.7)', display: 'flex', justifyContent: 'center', alignItems: 'center' };
const modal = { background: 'rgba(0,0,0,0.8)', padding: 30, borderRadius: 15 };