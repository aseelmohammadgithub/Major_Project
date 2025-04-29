// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

// frontend/src/App.js

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import LoginForm from './Components/LoginForm';
import PreviousActions from './Components/PreviousActions';
import Aboutus from './Components/Aboutus';
import AboutAlgorithm from './Components/AboutAlgorithm';
function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/login" element={<LoginForm />} />
      <Route path='/previous-actions' element={<PreviousActions/>}/>
      <Route path='/about-us' element={<Aboutus/>}/>
      <Route path='/about-algorithm' element={<AboutAlgorithm/>}/>
    </Routes>
  );
}

export default App;
