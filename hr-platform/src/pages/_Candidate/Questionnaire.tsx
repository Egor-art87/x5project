import { useState } from 'react';

export default function Questionnaire() {
  // useState сохраняет ответы кандидата. 
  // step - текущий вопрос, setStep - функция для переключения вопроса
  const [step, setStep] = useState(1);
  
  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Опросник кандидата (ИИ-скрининг)</h2>
      
      {step === 1 && (
        <div>
          <h3>Шаг 1: Есть ли у вас опыт работы в ритейле?</h3>
          <button onClick={() => setStep(2)}>Да, есть</button>
          <button onClick={() => setStep(2)}>Нет, я без опыта</button>
        </div>
      )}

      {step === 2 && (
        <div>
          <h3>Шаг 2: Готовы ли вы к физическому труду (сборка заказов)?</h3>
          <button onClick={() => alert('Ответы записаны! ИИ анализирует...')}>Готов</button>
          <button onClick={() => alert('Ответы записаны! ИИ анализирует...')}>Не готов</button>
        </div>
      )}
    </div>
  );
}