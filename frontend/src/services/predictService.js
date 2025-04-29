// frontend/src/services/predictService.js

import axios from 'axios';

export const uploadCTScan = async (formData) => {
  const email = localStorage.getItem('email');
  const token = localStorage.getItem('token');

  const payload = new FormData();
  payload.append('doctor_name', formData.doctorName);
  payload.append('hospital_name', formData.hospitalName);
  payload.append('email', email);
  payload.append('image', formData.image);

  const res = await axios.post('http://localhost:5000/predict/predict', payload, {
    headers: { Authorization: `Bearer ${token}` }
  });

  return res.data; // ✅ very important to return res.data here
};
