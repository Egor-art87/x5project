export default function Applications() {
  const candidatesList = [
    { id: 1, name: "Иван Иванов", vacancy: "Frontend", status: "Прошел", decision: "Одобрено" },
    { id: 2, name: "Мария Сидорова", vacancy: "Data Science", status: "Не прошел", decision: "Отказ" },
  ];

  return (
    <div>
      <h1>Отклики</h1>
      {candidatesList.map(c => (
        <div key={c.id} style={{ padding: '15px', background: 'rgba(255,255,255,0.05)', marginBottom: '10px', borderRadius: '10px' }}>
          {c.name} — {c.vacancy} — <strong>{c.status}</strong>
        </div>
      ))}
    </div>
  );
}