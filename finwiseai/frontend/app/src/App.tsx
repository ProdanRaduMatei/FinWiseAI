import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Train from './pages/Train';
import Predict from './pages/Predict';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/train" element={<Train />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
        </Routes>
    );
}

export default App;