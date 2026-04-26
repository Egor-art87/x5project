import { useState } from 'react';

interface HomeProps {
  setUser: (user: any) => void;
  user: any;
}

export default function Home({ setUser, user }: HomeProps) {
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ name: '', phone: '', birthDate: '', citizenship: '' });

  const news = [
    { title: "X5 Tech запустила собственную LLM", desc: "Теперь нейросети помогают собирать заказы быстрее." },
    { title: "Роботы в 'Пятерочке'", desc: "Тестирование автономных инвентаризаторов на складах." },
    { title: "X5 Cloud расширяется", desc: "Инфраструктура компании теперь выдерживает пиковые нагрузки в 2 раза лучше." }
  ];

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    setUser(formData);
    setShowModal(false);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Работай с нами <span style={{ color: '#00ff00' }}>x5 Tech Team</span></h1>
      {!user && (
        <button onClick={() => setShowModal(true)} style={btnMainStyle}>Log In / Регистрация</button>
      )}
      <div style={{ marginTop: '60px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
        {news.map((n, i) => (
          <div key={i} style={cardStyle}>
            <h3>{n.title}</h3>
            <p style={{ opacity: 0.8 }}>{n.desc}</p>
          </div>
        ))}
      </div>
      {showModal && (
        <div style={modalOverlayStyle}>
          <div style={modalStyle}>
            <h2>Регистрация</h2>
            <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <input placeholder="ФИО" required onChange={e => setFormData({...formData, name: e.target.value})} style={inputStyle} />
              <input placeholder="Телефон" required onChange={e => setFormData({...formData, phone: e.target.value})} style={inputStyle} />
              <input type="date" required onChange={e => setFormData({...formData, birthDate: e.target.value})} style={inputStyle} />
              <input placeholder="Гражданство" required onChange={e => setFormData({...formData, citizenship: e.target.value})} style={inputStyle} />
              <button type="submit" style={btnSubmitStyle}>Войти</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

const btnMainStyle = { padding: '15px 40px', borderRadius: '30px', border: 'none', background: '#00ff00', cursor: 'pointer', fontWeight: 'bold' as 'bold' };
const cardStyle = { background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '15px', border: '1px solid rgba(255,255,255,0.1)' };
const modalOverlayStyle: React.CSSProperties = { position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.7)', display: 'flex', justifyContent: 'center', alignItems: 'center' };
const modalStyle = { background: 'rgba(40, 40, 40, 0.9)', backdropFilter: 'blur(20px)', padding: '40px', borderRadius: '20px', width: '350px' };
const inputStyle = { padding: '10px', borderRadius: '5px', border: 'none', background: 'rgba(255,255,255,0.2)', color: 'white' };
const btnSubmitStyle = { padding: '10px', background: '#00ff00', border: 'none', borderRadius: '5px', fontWeight: 'bold' as 'bold', cursor: 'pointer' };