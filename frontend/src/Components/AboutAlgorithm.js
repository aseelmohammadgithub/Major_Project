import React from 'react';
import Navbar from './Navbar';
import './AboutAlgorithm.css';

function AboutAlgorithm() {
  return (
    <div>
      <Navbar />

      <div className="about-container">
        <div className="about-content">
          <h1 className="title">RespAIration: Lung Cancer Detection and classification</h1>
          
          <section className="section">
            <h2 className="section-title">Overview</h2>
            <p className="section-text">
              RespAiration is a full-stack web application that enables doctors to upload lung CT scan images. 
              The system automatically predicts potential lung diseases using a machine learning model, generates Grad-CAM visualizations, 
              and emails the results back to the doctor. It integrates **React.js** (Frontend), **Flask** (Backend), **MongoDB Atlas** (Database), 
              and **Gmail SMTP** (Email Service).
            </p>
          </section>

          <section className="section">
            <h2 className="section-title">How the System Works</h2>
            <ol className="step-list">
              <li>Doctors upload CT scan images with doctor and hospital details via a user-friendly React form.</li>
              <li>The Flask backend saves the uploaded image and processes it through a deep learning model for disease prediction.</li>
              <li>A Grad-CAM heatmap is generated to visually highlight the areas that influenced the model's prediction.</li>
              <li>All information is securely stored in MongoDB Atlas for record-keeping.</li>
              <li>An email with the prediction result and visualizations is automatically sent to the doctor.</li>
              <li>Doctors can retrieve their previous records using their email address.</li>
            </ol>
          </section>

          <section className="section">
            <h2 className="section-title">Tech Stack</h2>
            <div className="tech-stack">
              <div className="tech-item">
                <h3 className="tech-title">Frontend</h3>
                <p className="tech-description">React.js, Axios</p>
              </div>
              <div className="tech-item">
                <h3 className="tech-title">Backend</h3>
                <p className="tech-description">Flask, Flask-CORS, Flask-Mail</p>
              </div>
              <div className="tech-item">
                <h3 className="tech-title">Database</h3>
                <p className="tech-description">MongoDB Atlas</p>
              </div>
              <div className="tech-item">
                <h3 className="tech-title">Machine Learning</h3>
                <p className="tech-description">PyTorch, Grad-CAM</p>
              </div>
              <div className="tech-item">
                <h3 className="tech-title">Email Service</h3>
                <p className="tech-description">Gmail SMTP</p>
              </div>
              <div className="tech-item">
                <h3 className="tech-title">Hosting</h3>
                <p className="tech-description">Flask Server (Port 5000)</p>
              </div>
            </div>
          </section>

          <section className="section">
            <h2 className="section-title">Core Features</h2>
            <ul className="features-list">
              <li>Secure token-based authentication for safe access.</li>
              <li>Large medical image upload capability.</li>
              <li>Real-time disease prediction based on CT scan analysis.</li>
              <li>Explainable AI with Grad-CAM visualization to highlight key areas in the image.</li>
              <li>Automated email notifications for prediction results and visualizations.</li>
              <li>Database tracking of uploaded records for easy access.</li>
              <li>Proper CORS configuration for seamless React ↔ Flask communication.</li>
            </ul>
          </section>

          <section className="section">
            <h2 className="section-title">API Endpoints</h2>
            <ul className="api-list">
              <li><code className="api-code">POST /predict/predict</code> — Upload CT scan for disease prediction and email results.</li>
              <li><code className="api-code">GET /predict/previous-actions?email=</code> — Fetch all previously uploaded scans for a doctor.</li>
              <li><code className="api-code">POST /auth/login / signup</code> — Handle user authentication and session management.</li>
            </ul>
          </section>

          <section>
            <h2 className="section-title">Presentation Script</h2>
            <p className="section-text">
              RespAiration is a full-stack web application designed to improve the process of diagnosing lung diseases. 
              Doctors can upload CT scan images through an easy-to-use interface, and the system uses a deep learning model to predict potential diseases. 
              Additionally, Grad-CAM visualizations highlight the areas of the image that were important in making the prediction. 
              This tool allows for a more explainable diagnosis, and the results are instantly sent to the doctor’s email. 
              The database integration keeps track of all patient scans for future reference and analysis.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}

export default AboutAlgorithm;
