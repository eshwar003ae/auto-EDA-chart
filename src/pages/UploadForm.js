import { useState } from "react";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("File:", file);
    console.log("Prompt:", prompt);
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-purple-500 to-pink-600">
      <div className="bg-white p-8 rounded-xl shadow-lg w-96">
        <h2 className="text-xl font-bold text-center mb-6">Upload Your Dataset 📊</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full p-2 border rounded"
          />
          <input
            type="text"
            placeholder="Enter prompt (e.g., Compare average vs topper)"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full p-2 border rounded"
          />
          <button
            type="submit"
            className="w-full bg-purple-600 text-white py-2 rounded hover:bg-purple-700"
          >
            Analyze
          </button>
        </form>
      </div>
    </div>
  );
}

export default UploadForm;
