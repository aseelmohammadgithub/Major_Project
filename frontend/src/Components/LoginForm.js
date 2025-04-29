import React, { useState } from 'react';
import { loginUser } from '../services/authService';
import { useNavigate } from 'react-router-dom';  
import Navbar from './Navbar';
import img from './home1.png'; // Make sure the path is correct

function LoginForm() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const success = await loginUser(formData);
      if (success) {
        window.location.href = "/dashboard";
      }
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  const goToRegister = () => {
    navigate('/'); // Navigate to Registration page
  };

  return (
    <div className="bg-light" style={{ minHeight: '100vh' }}>
      <Navbar />
      <div className="container d-flex align-items-center justify-content-center" style={{ minHeight: '90vh' }}>
        <div className="row w-100">

          {/* Left Side for Image */}
          <div className="col-md-6 d-none d-md-flex justify-content-center align-items-center">
            <img 
              src={img}
              alt="CT Scan Example" 
              className="img-fluid shadow-lg rounded"
              style={{ maxHeight: '400px' }}
            />
          </div>

          {/* Right Side for Login Form */}
          <div className="col-md-6 d-flex justify-content-center align-items-center">
            <div className="card p-5 shadow" style={{ width: '100%', maxWidth: '400px' }}>
              <h3 className="text-center mb-4">Login</h3>
              <form onSubmit={handleSubmit}>
                <div className="mb-3 mx-4">
                  <input
                    className="form-control"
                    type="email"
                    name="email"
                    placeholder="Email"
                    onChange={handleChange}
                    value={formData.email}
                    required
                  />
                </div>
                <div className="mb-3 mx-4">
                  <input
                    className="form-control"
                    type="password"
                    name="password"
                    placeholder="Password"
                    onChange={handleChange}
                    value={formData.password}
                    required
                  />
                </div>
                {error && <div className="text-danger mb-3 text-center">{error}</div>}
                <button className="btn btn-success w-100" type="submit">Login</button>
              </form>

              {/* Text and Button to Register */}
              <div className="text-center mt-3">
                <p className="mb-2">New here?</p>
                <button className="btn btn-outline-primary w-100" onClick={goToRegister}>
                  Register Yourself
                </button>
              </div>

            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default LoginForm;
