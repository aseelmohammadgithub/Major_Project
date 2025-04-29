// frontend/src/services/historyService.js

import axios from 'axios';

export const fetchPreviousActions = async () => {
  const email = localStorage.getItem('email');
  const res = await axios.get(`http://localhost:5000/predict/previous-actions?email=${email}`);
  return res.data;
};
