export default function Vacancies({ setVacancy }: any) {
  const jobs = [
    "Frontend","Backend","Fullstack","Mobile",
    "Data Science","DevOps","QA","UX/UI"
  ];

  return (
    <div>
      <h1>Выбери вакансию</h1>
      {jobs.map(j => (
        <button key={j} onClick={() => setVacancy(j)} style={btn}>{j}</button>
      ))}
    </div>
  );
}

const btn = { margin: 10, padding: 10 };