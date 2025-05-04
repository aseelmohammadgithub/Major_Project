import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchPreviousActions } from '../services/historyService';

function PreviousActions() {
  const [actions, setActions] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      // Token is not found, redirect to login
      navigate('/login');
      return;
    }

    const getData = async () => {
      try {
        const data = await fetchPreviousActions();
        setActions(data);
      } catch (err) {
        console.error('Failed to fetch previous actions:', err);
        // Redirect to login if fetching fails or token is invalid
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };

    getData();
  }, [navigate]);

  const downloadAll = () => {
    const headers = ['Date', 'Doctor Name', 'Hospital Name', 'Input Image URL', 'Output Image URL'];
    const rows = actions.map(a => [
      new Date(a.date).toLocaleString(),
      a.doctor_name,
      a.hospital_name,
      `http://localhost:5000/${a.input_image_path}`,
      `http://localhost:5000/${a.output_image_path}`
    ]);
    const csv =
      headers.join(',') + '\n' +
      rows.map(r => r.map(f => `"${f}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = 'previous_actions.csv';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  const handleDownloadFile = (imagePath) => {
    const url = `http://localhost:5000/${imagePath}`;
    fetch(url)
      .then(res => res.blob())
      .then(blob => {
        const objectUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = objectUrl;
        a.download = imagePath.split('/').pop();
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(objectUrl);
      })
      .catch(err => console.error('Download error:', err));
  };

  if (loading) {
    return <div>Loading...</div>; // Loading screen while fetching data
  }

  return (
    <div className="container my-5 d-flex justify-content-center">
      <div className="card shadow-lg w-100" style={{ maxWidth: '1200px' }}>
        <div className="card-body p-4">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h3 className="card-title mb-0">Previous Actions</h3>
            <button className="btn btn-outline-primary" onClick={downloadAll}>
              Download All
            </button>
          </div>

          <div className="table-responsive">
            <table className="table table-striped table-bordered align-middle text-center">
              <thead className="table-dark">
                <tr>
                  <th>Date</th>
                  <th>Doctor Name</th>
                  <th>Hospital Name</th>
                  <th>Input Image</th>
                  <th>Output Image</th>
                </tr>
              </thead>
              <tbody>
                {actions.length === 0 && (
                  <tr>
                    <td colSpan="5" className="text-center py-4">
                      No previous actions found.
                    </td>
                  </tr>
                )}
                {actions.map((action, idx) => (
                  <tr key={idx}>
                    <td>{new Date(action.date).toLocaleString()}</td>
                    <td>{action.doctor_name}</td>
                    <td>{action.hospital_name}</td>

                    <td>
                      <div className="d-flex align-items-center justify-content-center">
                        <img
                          src={`http://localhost:5000/${action.input_image_path}`}
                          alt="Input"
                          className="img-thumbnail"
                          style={{ height: '75px', width: 'auto' }}
                        />
                        <button
                          className="btn btn-sm btn-outline-secondary ms-2"
                          onClick={() => handleDownloadFile(action.input_image_path)}
                        >
                          Download
                        </button>
                      </div>
                    </td>

                    <td>
                      <div className="d-flex align-items-center justify-content-center">
                        <img
                          src={`http://localhost:5000/${action.output_image_path}`}
                          alt="Output"
                          className="img-thumbnail"
                          style={{ height: '75px', width: 'auto' }}
                        />
                        <button
                          className="btn btn-sm btn-outline-secondary ms-2"
                          onClick={() => handleDownloadFile(action.output_image_path)}
                        >
                          Download
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PreviousActions;
