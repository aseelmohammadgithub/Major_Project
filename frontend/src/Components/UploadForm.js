import React, { useState, useRef } from 'react';
import { uploadCTScan } from '../services/predictService';

function UploadForm() {
  const [formData, setFormData] = useState({ doctorName: '', hospitalName: '', image: null });
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [outputUrl, setOutputUrl] = useState('');
  const [loading, setLoading] = useState(false); // 👈 new loading state
  const formRef = useRef();

  const handleChange = (e) => {
    if (e.target.name === 'image') {
      setFormData({ ...formData, image: e.target.files[0] });
    } else {
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMsg('');
    setErrorMsg('');
    setOutputUrl('');
    setLoading(true); // 👈 start loading

    try {
      const res = await uploadCTScan(formData);
      setSuccessMsg(res.message || 'Upload successful!');
      setOutputUrl(`http://localhost:5000/${res.output_image_url}`);
      formRef.current.reset();
      setFormData({ doctorName: '', hospitalName: '', image: null });
    } catch (err) {
      console.error(err);
      setErrorMsg(err.response?.data?.error || err.message || 'Upload failed.');
    } finally {
      setLoading(false); // 👈 end loading
    }
  };

  return (
    <form ref={formRef} onSubmit={handleSubmit}>
      <h3>Upload CT Scan</h3>

      <input
        className="form-control mb-2"
        type="text"
        name="doctorName"
        placeholder="Doctor Name"
        onChange={handleChange}
        required
      />
      <input
        className="form-control mb-2"
        type="text"
        name="hospitalName"
        placeholder="Hospital Name"
        onChange={handleChange}
        required
      />
      <input
        className="form-control mb-2"
        type="file"
        name="image"
        accept="image/*"
        onChange={handleChange}
        required
      />

      {successMsg && <div className="alert alert-success mt-2">{successMsg}</div>}
      {errorMsg && <div className="alert alert-danger mt-2">{errorMsg}</div>}

      <button
        className="btn btn-primary w-100 mt-3"
        type="submit"
        disabled={loading}
      >
        {loading ? (
          <>
            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Processing...
          </>
        ) : 'Submit'}
      </button>

      {loading && (
        <div className="text-center mt-3 text-muted">
          <div className="spinner-border text-secondary" role="status"></div>
          <div>Please wait, processing image...</div>
        </div>
      )}

      {outputUrl && (
        <div className="text-center mt-4">
          <h5>Prediction Result</h5>
          <img
            src={outputUrl}
            alt="Grad-CAM Output"
            className="img-fluid rounded shadow"
            style={{ maxHeight: '300px' }}
          />
          <div className="mt-2">
            <a href={outputUrl} download className="btn btn-outline-secondary">Download Result</a>
          </div>
        </div>
      )}
    </form>
  );
}

export default UploadForm;
