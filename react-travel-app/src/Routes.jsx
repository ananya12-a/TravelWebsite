// Routes.jsx
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import App from "./App";
import Register from "./components/register";

function AppRoutes() {
  return (
    <Routes>
      <Route path="*" exact element={<App />} /> {/* Use 'element' prop for the component */}
      <Route path="/register" element={<Register heading="Register" />} /> {/* Pass heading prop */}
    </Routes>
  );
}

export default AppRoutes;