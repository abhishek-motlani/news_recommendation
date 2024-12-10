import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/navbar";
import Dashboard from "./components/Dashboard";
import SearchBar from "./components/SearchBar";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/news-recommendation" element={<SearchBar />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
};

export default App;
