import { useState } from 'react';

export default function Tests({ vacancy }: { vacancy: string }) {
  const [step, setStep] = useState(0);

  const questions = [
    "Как ты начинаешь задачу?",
    "Что тебе ближе?"
  ];

  if (!vacancy) return <h2>Сначала выбери вакансию</h2>;

  return (
    <div>
      <h2>{vacancy}</h2>
      <h3>{questions[step]}</h3>

      <button onClick={() => setStep(step + 1)}>Далее</button>
    </div>
  );
}