// // frontend/src/services/authService.js

// import axios from 'axios';

// export const registerUser = async (data) => {
//   await axios.post('http://localhost:5000/auth/register', data);
// };

// export const loginUser = async (data) => {
//   const res = await axios.post('http://localhost:5000/auth/login', data);
//   localStorage.setItem('token', res.data.token);
//   localStorage.setItem('email', data.email);
//   return true;
// };
// frontend/src/services/authService.js

import axios from 'axios';

export const registerUser = async (data) => {
  try {
    const response = await axios.post('http://localhost:5000/auth/register', data);
    return response.data;
  } catch (err) {
    throw new Error(err.response?.data?.error || 'Registration failed. Please try again.');
  }
};

export const loginUser = async (data) => {
  try {
    const response = await axios.post('http://localhost:5000/auth/login', data);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('email', data.email);
      return true;
    } else {
      return false;
    }
  } catch (err) {
    throw new Error(err.response?.data?.error || 'Login failed. Please try again.');
  }
};
