import axios from 'axios';

export const fetchPreviousActions = async () => {
  const token = localStorage.getItem('token');

  const res = await axios.get('http://localhost:5000/predict/previous-actions', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    withCredentials: true, // Optional depending on your CORS config
  });

  return res.data;
};
