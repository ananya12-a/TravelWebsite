import React from "react";
import { createRoot } from "react-dom/client"; // Import createRoot from react-dom/client
import { BrowserRouter as Router } from "react-router-dom";
import Routes from "./Routes";

// Render the root component using createRoot
createRoot(document.getElementById("root")).render(
  <Router>
    <Routes />
  </Router>
);