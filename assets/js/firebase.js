import { initializeApp } from "https://www.gstatic.com/firebasejs/9.1.1/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/9.1.1/firebase-firestore.js"
import { collection, getDocs, addDoc, Timestamp } from "https://www.gstatic.com/firebasejs/9.1.1/firebase-firestore.js"
import { query, orderBy, limit, where, onSnapshot } from "https://www.gstatic.com/firebasejs/9.1.1/firebase-firestore.js"

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyChcoDH9YP09TZcx5fatDdBWcFzi7A476s",
    authDomain: "pothole-4a96f.firebaseapp.com",
    projectId: "pothole-4a96f",
    storageBucket: "pothole-4a96f.appspot.com",
    messagingSenderId: "829275371861",
    appId: "1:829275371861:web:d6485f64d2be88a24317dc",
    measurementId: "G-MF1GHZFNQ9"
};
    
export async function getData() {
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const db = getFirestore(app);
  return await getDocs(collection(db, "markers"));
}

// export { app, db, collection, getDocs, Timestamp, addDoc };
// export { query, orderBy, limit, where, onSnapshot };
