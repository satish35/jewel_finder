
  // Import the functions you need from the SDKs you need
//   import { initializeApp, messaging } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional

  importScripts(
    "https://www.gstatic.com/firebasejs/10.1.0/firebase-app-compat.js"
  );
  importScripts(
    "https://www.gstatic.com/firebasejs/10.1.0/firebase-messaging-compat.js"
  );

  const firebaseConfig = {
    apiKey: "AIzaSyCJF9nc5pmp1D-Y2D-RwS6mIFu2rm1ALSQ",
    authDomain: "flask-project-978a7.firebaseapp.com",
    projectId: "flask-project-978a7",
    storageBucket: "flask-project-978a7.appspot.com",
    messagingSenderId: "108462060386",
    appId: "1:108462060386:web:12be054954e5087720323b",
    measurementId: "G-N6H0HNL0EL"
  };

  // Initialize Firebase
  const app = firebase.initializeApp(firebaseConfig);
  const messaging = firebase.messaging(app);

  messaging.onMessage((payload) => {
    // Handle incoming FCM messages
    console.log(payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
      body: payload.notification.body
    //   icon: "icon.png", // Customize this with your icon path
    };
    return self.registration.showNotification(
          notificationTitle,
          notificationOptions
        );
  });
  
  messaging.onBackgroundMessage((payload) => {
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
      body: payload.notification.body
    //   icon: "icon.png", // Customize this with your icon path
    };
  
    return self.registration.showNotification(
      notificationTitle,
      notificationOptions
    );
  });