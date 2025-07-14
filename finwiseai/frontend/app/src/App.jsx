// src/App.jsx
import { useState } from "react";
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "./firebase";

function App() {
    const [user, setUser] = useState(null);

    const loginWithGoogle = async () => {
        try {
            const result = await signInWithPopup(auth, provider);
            setUser(result.user);
            console.log("ID Token:", await result.user.getIdToken()); // Send this to your backend later
        } catch (err) {
            console.error("Google Login Error:", err);
        }
    };

    return (
        <div style={{ padding: 32 }}>
            {user ? (
                <>
                    <h2>Welcome, {user.displayName}</h2>
                    <p>Email: {user.email}</p>
                </>
            ) : (
                <button onClick={loginWithGoogle}>Sign in with Google</button>
            )}
        </div>
    );
}

export default App;