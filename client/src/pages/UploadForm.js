import { useState } from "react";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (!file) {
      alert("Please select a file first!");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("prompt", prompt);

    try {
        const response = await fetch("http://localhost:8000/api/analyze", {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        console.log(data);
        setAnalysisResult(data);
        alert(data.message);
    } catch (error) {
        console.error('Error:', error);
        alert("Failed to upload the file.");
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="p-12 min-h-screen">
      <div className="bg-white p-12 rounded-2xl shadow-xl w-full max-w-4xl mx-auto">
        <h2 className="text-4xl font-extrabold text-center mb-4 text-gray-800">Auto EDA Chart</h2>
        <h3 className="text-xl font-semibold text-center mb-8 text-gray-600">Upload Your Dataset 📊</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <label className="flex items-center justify-center w-full px-6 py-3 border-2 border-gray-300 rounded-lg cursor-pointer bg-white text-purple-600 hover:bg-purple-50 transition-colors duration-200">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L6.293 6.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
              <span className="text-lg font-medium">
                {file ? file.name : "Choose File"}
              </span>
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="hidden"
              />
            </label>
            <input
              type="text"
              placeholder="Enter prompt (e.g., Compare salary vs experience)"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            <button
              type="submit"
              className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors duration-200"
              disabled={loading}
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </form>

          {analysisResult && (
            <div className="mt-8 p-6 bg-gray-100 rounded-xl">
              <h3 className="font-bold text-xl mb-3">Analysis Results</h3>
              <h4 className="font-semibold text-lg">Summary Statistics:</h4>
              <pre className="text-sm overflow-auto max-h-40 bg-gray-200 p-2 rounded-lg mt-2">{JSON.stringify(analysisResult.summary, null, 2)}</pre>
              
              {analysisResult.plot && (
                <div className="mt-4">
                  <h4 className="font-semibold text-lg">Generated Plot:</h4>
                  <img src={`data:image/png;base64,${analysisResult.plot}`} alt="Data Plot" className="mt-2 w-full rounded-lg" />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default UploadForm;