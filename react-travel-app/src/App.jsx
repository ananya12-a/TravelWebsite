import React, { useState } from "react";
import { Route, Routes } from "react-router-dom"; // Import Route, not BrowserRouter
import Login from "./components/login";
import Register from "./components/register";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <div id="root" className="container">
      <div className="left-half">Welcome to Travel App!</div>
      <div className="right-half">
        {isLoggedIn ? (
          <div>
            <div className="heading">Logged in</div>
            <button onClick={handleLogout}>Logout</button>
          </div>
        ) : (
          <div>
            <Login heading="Login" />
            <div className="subheading">
              Don't have an account? <a href="/register">Register</a>
            </div>
          </div>
        )}
        <Routes>
          <Route exact path="/register" element={<Register heading="Register" className="heading" />}>
          </Route>
        </Routes>
      </div>
    </div>
  );
}

export default App;
