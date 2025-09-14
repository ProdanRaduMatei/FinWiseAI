import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Train from './pages/Train';
import Predict from './pages/Predict';

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/train" element={<Train />} />
            <Route path="/predict" element={<Predict />} />
        </Routes>
    );
}

export default App;