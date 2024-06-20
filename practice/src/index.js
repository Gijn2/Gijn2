import React from 'react';
import ReactDOM from 'react-dom/client';
// import './index.css';
import reportWebVitals from './reportWebVitals';
// import App from './App';
// import App from './b_conditional/1_truthy';
// import App from './b_conditional/2_inline';
// import App from './b_conditional/3_element_variable';
// import App from './b_conditional/4_stop_rendering';
import App from './b_conditional/prac';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
