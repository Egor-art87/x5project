export default function RecruiterDashboard() {
  // Имитация данных, которые потом будут приходить от бэкенда/ИИ
  const candidates = [
    { id: 1, name: 'Иван Иванов', score: 95, status: 'Рекомендован' },
    { id: 2, name: 'Анна Смирнова', score: 40, status: 'Не подходит' },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2>Панель рекрутера (Отбор)</h2>
      <p>Здесь отображается скоринг, сформированный ИИ.</p>
      
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
        <thead>
          <tr style={{ background: '#eee', textAlign: 'left' }}>
            <th>Имя</th>
            <th>Совпадение (%)</th>
            <th>Вердикт ИИ</th>
            <th>Действие</th>
          </tr>
        </thead>
        <tbody>
          {candidates.map((cand) => (
            <tr key={cand.id} style={{ borderBottom: '1px solid #ccc' }}>
              <td>{cand.name}</td>
              <td>{cand.score}%</td>
              <td>{cand.status}</td>
              <td><button>Посмотреть анкету</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}