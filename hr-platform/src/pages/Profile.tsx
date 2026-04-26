export default function Profile({ user }: { user: any }) {
  return (
    <div style={{ maxWidth: '500px', margin: '50px auto', textAlign: 'center', background: 'rgba(255,255,255,0.05)', padding: '40px', borderRadius: '30px', border: '1px solid rgba(255,255,255,0.1)' }}>
      <div style={{ width: '120px', height: '120px', background: '#006a4e', borderRadius: '50%', margin: '0 auto 20px', display: 'flex', justifyContent: 'center', alignItems: 'center', fontSize: '3rem' }}>
        👤
      </div>
      <h2 style={{ color: '#00ff00' }}>{user?.name}</h2>
      <div style={{ textAlign: 'left', marginTop: '20px', lineHeight: '2' }}>
        <p><strong>Телефон:</strong> {user?.phone}</p>
        <p><strong>Дата рождения:</strong> {user?.birthDate}</p>
        <p><strong>Гражданство:</strong> {user?.citizenship}</p>
      </div>
    </div>
  );
}