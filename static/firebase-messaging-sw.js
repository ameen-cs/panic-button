// static/firebase-messaging-sw.js
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSy...",
  authDomain: "panic-button.firebaseapp.com",
  projectId: "panic-button",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890"
});

const messaging = firebase.messaging();