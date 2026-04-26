import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Questionnaire from './pages/Candidate/Questionnaire';
import RecruiterDashboard from './pages/Recruiter/RecruiterDashboard';
import AdminPanel from './pages/Admin/AdminPanel';

function App() {
  return (
    <Router>
      <Navigation />
      <Routes>
        {/* Когда в адресной строке /, показываем Опросник */}
        <Route path="/" element={<Questionnaire />} />
        {/* Когда в адресной строке /recruiter, показываем панель Рекрутера */}
        <Route path="/recruiter" element={<RecruiterDashboard />} />
        {/* Когда в адресной строке /admin, показываем панель Админа */}
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
    </Router>
  );
}

export default App;