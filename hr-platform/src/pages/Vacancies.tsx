export default function Vacancies({ setVacancy }: { setVacancy: (v: string) => void }) {
  const jobs = ["Frontend", "Backend", "DevOps", "Data Science"];

  return (
    <div>
      <h1>Выбор вакансии</h1>
      {jobs.map(j => (
        <button key={j} onClick={() => setVacancy(j)} style={{ margin: 10 }}>
          {j}
        </button>
      ))}
    </div>
  );
}