// frontend/src/pages/DashboardPage.js

import React from 'react';
import Navbar from '../Components/Navbar';
import UploadForm from '../Components/UploadForm';
import PreviousActions from '../Components/PreviousActions';
import img from './home2.png';
function DashboardPage() {
  return (
    <div>
      <Navbar loggedIn={true} />
      <div className="container d-flex mt-5">
        <div className="w-50">
          {/* Image Display after upload if needed */}
          <div className="col-md-7 d-none d-md-flex justify-content-center align-items-center">
                      <img
                        src={img}
                        alt="Welcome Illustration"
                        className="img-fluid shadow-lg rounded"
                        style={{ maxHeight: '300px' }}
                      />
                    </div>

        </div>
        <div className="w-50">
          <UploadForm />
        </div>
      </div>
      <div id="previous-actions" className="container mt-5">
        <PreviousActions />
      </div>
    </div>
  );
}

export default DashboardPage;
