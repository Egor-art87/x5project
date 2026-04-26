import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Tests from './pages/Tests';
import Vacancies from './pages/Vacancies';
import Applications from './pages/Applications';
import Profile from './pages/Profile';

export interface User {
  name: string;
  phone: string;
  birthDate: string;
  citizenship: string;
}

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [vacancy, setVacancy] = useState<string>("");

  return (
    <Router>
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #003d2b, #006a4e)',
        color: 'white'
      }}>
        <Navigation />
        <div style={{ padding: '20px' }}>
          <Routes>
            <Route path="/" element={<Home setUser={setUser} user={user} />} />
            <Route path="/vacancies" element={<Vacancies setVacancy={setVacancy} />} />
            <Route path="/tests" element={<Tests vacancy={vacancy} />} />
            <Route path="/applications" element={user ? <Applications /> : <Navigate to="/" />} />
            <Route path="/profile" element={user ? <Profile user={user} /> : <Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}