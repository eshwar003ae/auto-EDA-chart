import React from "react";
import UploadForm from "../pages/UploadForm";

const Home = () => {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Upload Your Dataset</h2>
      <UploadForm />
    </div>
  );
};

export default Home;
