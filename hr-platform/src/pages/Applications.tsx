export default function Applications() {
  const list = [
    { name: "Иван", status: "Прошел" },
    { name: "Мария", status: "Отказ" }
  ];

  return (
    <div>
      <h1>Отклики</h1>
      {list.map((c, i) => (
        <div key={i}>{c.name} — {c.status}</div>
      ))}
    </div>
  );
}