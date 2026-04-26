export default function Vacancies({ setVacancy }: any) {
  const categories = [
    { name: "Разработка", jobs: ["Frontend", "Backend", "Fullstack", "Mobile", "Game Dev", "Embedded"] },
    { name: "Данные", jobs: ["Data Science", "Data Analyst", "Machine Learning", "Data Engineering"] },
    { name: "Инфраструктура", jobs: ["DevOps", "SRE", "Cloud Engineering", "System Admin"] },
    { name: "Продукт / Дизайн", jobs: ["UX/UI Design", "Product Design", "Product Management"] }
  ];

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h1>Выберите вакансию</h1>
      {categories.map((cat, i) => (
        <div key={i} style={{ marginBottom: '30px' }}>
          <h2 style={{ color: '#00ff00' }}>{cat.name}</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {cat.jobs.map(job => (
              <button 
                key={job} 
                onClick={() => { setVacancy(job); alert(`Выбрано: ${job}`); }}
                style={{ padding: '10px 20px', borderRadius: '20px', border: '1px solid #00ff00', background: 'transparent', color: 'white', cursor: 'pointer' }}
              >
                {job}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}