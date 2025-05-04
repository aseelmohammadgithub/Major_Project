
// frontend/src/components/RegisterForm.js

import React, { useState } from 'react';
import { registerUser } from '../services/authService';
import { useNavigate } from 'react-router-dom';

function RegisterForm() {
  const [formData, setFormData] = useState({ name: '', email: '', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const { password, confirmPassword } = formData;

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    try {
      await registerUser(formData);
      setSuccessMessage('Registration successful!');
      setError('');

      setTimeout(() => {
        navigate('/login');
      }, 1500);
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.');
      setSuccessMessage('');
    }
  };

  const goToLogin = () => {
    navigate('/login');
  };

  // Inline style with !important override using style string
  const inputStyle = {
    height: '50px',
    fontSize: '16px',
    padding: '10px',
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <h3 style={{textAlign:'center'}}>Register</h3>

        <input
          className="form-control mb-2 mx-4"
          style={{ ...inputStyle }}
          type="text"
          name="name"
          placeholder="Name"
          onChange={handleChange}
          required
        />

        <input
          className="form-control mb-2 mx-4"
          style={{ ...inputStyle }}
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          required
        />
        <p className="text-danger mx-4" style={{ fontSize: '14px' }}>
        Password must be minimum 6 characters <br></br>
        Password must contain at least one lowercase letter, one uppercase letter, and one symbol (!, @, or $)
       </p>
       
        <input
          className="form-control mb-2 mx-4"
          style={{ ...inputStyle }}
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          required
        />

        <input
          className="form-control mb-2 mx-4"
          style={{ ...inputStyle }}
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          onChange={handleChange}
          required
        />

        {error && <p className="text-danger mx-4">{error}</p>}
        {successMessage && <p className="text-success mx-4">{successMessage}</p>}

        <button className="btn btn-primary w-100 mx-4" type="submit">Register</button>
      </form>

      <div className="text-center mt-3">
        <p className="mb-2">Already Registered?</p>
        <button className="btn btn-outline-primary w-100" onClick={goToLogin}>
          Login
        </button>
      </div>
    </>
  );
}

export default RegisterForm;
