export default function AdminPanel() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Панель Администратора (Тех. спец)</h2>
      <p>Управление доступом и системными настройками.</p>
      
      <div style={{ marginTop: '20px', padding: '15px', border: '1px solid red', borderRadius: '8px' }}>
        <h3>Управление ролями</h3>
        <label>
          Email пользователя: <input type="email" placeholder="user@x5.ru" />
        </label>
        <select style={{ marginLeft: '10px' }}>
          <option>Рекрутер</option>
          <option>Тех. специалист</option>
        </select>
        <button style={{ marginLeft: '10px' }}>Выдать права</button>
      </div>
    </div>
  );
}