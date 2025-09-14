import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { signup } from '../services/auth';

export default function Signup() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const data = await signup(email, password);
            localStorage.setItem('token', data.access_token);
            navigate('/');
        } catch (err) {
            // optionally, add proper error handling later
        }
    };


    return (
        <div className="min-h-screen flex items-center justify-center bg-muted/30">
            <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-md border border-gray-200">
                <h1 className="text-2xl font-semibold text-center mb-6">Create a FinWise AI Account</h1>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <input
                            type="email"
                            placeholder="Email"
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <input
                            type="password"
                            placeholder="Password"
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 rounded-md transition"
                    >
                        Sign Up
                    </button>
                </form>
                <p className="text-center text-sm text-gray-600 mt-4">
                    Already have an account?{' '}
                    <Link to="/login" className="text-green-600 hover:underline">
                        Log in
                    </Link>
                </p>
            </div>
        </div>
    );
}