import { useState } from 'react';

export default function Tests({ vacancy }: { vacancy: string }) {
  const [step, setStep] = useState(0);

  const questions = [
    { q: "Как ты начинаешь новую задачу?", a: ["Сразу делаю", "Сначала планирую", "Ищу примеры", "Жду уточнений"] },
    { q: "Что тебе ближе в работе?", a: ["Чёткий план", "Полная свобода", "Смесь обоих", "Как получится"] },
    { q: "Если задача неясна, ты:", a: ["Начинаю пробовать", "Задаю вопросы", "Жду инструкций", "Смотря на других"] },
  ];

  if (!vacancy) return <div style={{textAlign: 'center', marginTop: '50px'}}><h2>Сначала выберите вакансию!</h2></div>;

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', background: 'rgba(255,255,255,0.05)', padding: '30px', borderRadius: '20px' }}>
      <h3>Вопрос {step + 1}: {questions[step]?.q || "Тест завершен"}</h3>
      <div style={{ display: 'grid', gap: '10px', marginTop: '20px' }}>
        {questions[step]?.a.map((ans: string, i: number) => (
          <button key={i} onClick={() => setStep(step + 1)} style={testBtnStyle}>{ans}</button>
        ))}
      </div>
    </div>
  );
}
const testBtnStyle = { padding: '15px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(255,255,255,0.1)', color: 'white', cursor: 'pointer', textAlign: 'left' as 'left' };