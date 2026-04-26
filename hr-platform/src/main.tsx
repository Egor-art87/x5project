import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

// Важно: Мы просто рендерим <App />, внутри которого уже будет Router
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)