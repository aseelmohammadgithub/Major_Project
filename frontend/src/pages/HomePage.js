// frontend/src/pages/HomePage.js

import React from 'react';
import Navbar from '../Components/Navbar';
import RegisterForm from '../Components/RegisterForm';
import img from './home.png';

function HomePage() {
  return (
    <div className="bg-light" style={{ minHeight: '100vh' }}>
      <Navbar loggedIn={false} />

      <div
        className="container d-flex align-items-center justify-content-center"
        style={{ minHeight: '90vh' }}
      >
        <div className="row w-100">

          {/* Left: Illustration */}
          <div className="col-md-6 d-none d-md-flex justify-content-center align-items-center">
            <img
              src={img}
              alt="Welcome Illustration"
              className="img-fluid shadow-lg rounded"
              style={{ maxHeight: '400px' , boxShadow:'rgba(0, 0, 0, 0.24) 0px 3px 8px'}}
            />
          </div>

          {/* Right: Register Card */}
          <div className="col-md-6 d-flex justify-content-center align-items-center">
            <div
              className="card p-5 shadow"
              style={{ width: '100%', maxWidth: '500px' }}
            >
              {/* If you want a title above your form, you can uncomment: */}
              {/* <h3 className="text-center mb-4">Get Started</h3> */}
              <RegisterForm />
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default HomePage;
