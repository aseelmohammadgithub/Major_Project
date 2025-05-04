import React from 'react';
import Navbar from './Navbar';
import saif from '../static/Personal/saif.jpg';
import vamshi from '../static/Personal/vamshi.jpg';
import venkatesh from '../static/Personal/venkatesh.jpg';
import aseel from '../static/Personal/aseel.jpg';
import vishwanath from '../static/Personal/vishwanath.jpg';
import './Aboutus.css';
function AboutPage() {
  const team = [
    {
      img: aseel,
      name: 'Shaik Mohammad Aseel',
      roll: '21BD1A12C0',
      link: 'https://www.linkedin.com/in/shaik-mohammad-aseel-910a82249',
    },
    {
      img: saif,
      name: 'Mohammed Saifuddin',
      roll: '21BD1A12A6',
      link: 'https://www.linkedin.com/in/mohammed-saifuddin-124b751b9/',
    },
    {
      img: vamshi,
      name: 'Parvatam Vamshi',
      roll: '21BD1A12B3',
      link: 'https://www.linkedin.com/',
    },
    {
      img: venkatesh,
      name: 'Thoguta Venkatesh',
      roll: '21BD1A12C3',
      link: 'https://www.linkedin.com/in/venkatesh-thoguta-b30345215',
    },
    {
      img: vishwanath,
      name: 'CH N.V. Vishwanatha Sai',
      roll: '21BD1A1278',
      link: 'https://www.linkedin.com/in/vishwanatha-sai-4ba745362/',
    },
  ];
  return (
    <>
      <Navbar />

      <main className="about-section">
        <section className="main-info">
          <h2>About The Project</h2>
          <p>
            Lung cancer remains one of the leading causes of cancer-related deaths globally, with early detection playing
            a critical role in patient prognosis. In this project, we propose a hybrid deep learning model combining
            CNN and Vision Transformer (ViT) architectures to classify lung CT images into four categories:
            adenocarcinoma, large cell carcinoma, squamous cell carcinoma, and normal.
          </p>
          <p>
            The dataset was preprocessed using CLAHE (Contrast Limited Adaptive Histogram Equalization) and Gaussian
            blurring for enhanced contrast and noise reduction. The hybrid model architecture effectively combines local
            feature extraction of CNN with the global contextual attention mechanism of ViT, enabling it to capture
            complex medical patterns.
          </p>
          <p>
            Despite challenges of class imbalance—with 315 adenocarcinoma images versus only 54 normal cases—the model
            achieved a macro F1-score of 89% and overall accuracy of 93%. It performed exceptionally well in detecting
            normal (F1-score: 0.96) and adenocarcinoma (F1-score: 0.90) classes. Additionally, Grad-CAM visualizations
            were employed to enhance model interpretability, highlighting regions of diagnostic interest.
          </p>
          <p>
            This solution demonstrates potential as a decision-support tool for radiologists, aiding in the timely and
            accurate diagnosis of lung cancer subtypes.
          </p>
        </section>

        <hr className="divider" />

        <section className="team-section">
          <h2>Our Team</h2>
          <div className="card-container">
            {team.map((member, index) => (
              <div className="card" key={index}>
                <img src={member.img} alt={member.name} className="team-img" />
                <div className="card-content">
                  <h3 className="student-name">{member.name}</h3>
                  <p className="roll-no">{member.roll}</p>
                  <a
                    href={member.link}
                    className="linkedin-link"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View LinkedIn →
                  </a>
                </div>
              </div>
            ))}
          </div>
        </section>

        <footer className="footer">
          <p>All Rights Reserved &copy; 2025 Team RespAiration</p>
        </footer>
      </main>
    </>
  );
}

export default AboutPage;
