// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyD5bWDZc4zlB-ULWxf1MnBz7N65m1NR5xQ",
    authDomain: "finwiseai-5564c.firebaseapp.com",
    projectId: "finwiseai-5564c",
    storageBucket: "finwiseai-5564c.appspot.com",
    messagingSenderId: "65638226176",
    appId: "1:65638226176:web:0e8aafad7640c992763be5",
    measurementId: "G-W2N23WQXX1"
};

const app = initializeApp(firebaseConfig);

// Auth exports
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();