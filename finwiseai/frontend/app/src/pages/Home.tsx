import { Link } from 'react-router-dom';

export default function Home() {
    return (
        <div className="text-center mt-10">
            <h1 className="text-3xl font-bold">Welcome to FinWise AI</h1>
            <div className="mt-6 space-x-4">
                <Link to="/login" className="text-blue-600 underline">
                    Login
                </Link>
                <Link to="/signup" className="text-green-600 underline">
                    Signup
                </Link>
            </div>
        </div>
    );
}