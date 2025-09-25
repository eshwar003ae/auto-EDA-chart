import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-white shadow-lg p-4 flex justify-between items-center fixed top-0 w-full z-10">
      <div className="text-2xl font-bold text-gray-800">
        <Link to="/upload">Auto EDA Chart</Link>
      </div>
      <div className="flex space-x-4">
        <Link
          to="/upload"
          className="text-gray-600 hover:text-blue-600 transition duration-200"
        >
          Dashboard
        </Link>
        <Link
          to="/login"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-200"
        >
          Login
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;