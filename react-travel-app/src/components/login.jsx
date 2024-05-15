import React, { useState } from "react";
import "/src/App.css"; // Import the CSS file for login component styles

function Login(props) {
  const { heading } = props;
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name == "username") {
      setUsername(value);
    } else if (name === "password") {
      setPassword(value);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Perform additional checks here
    if (username == "validUsername" && password == "validPassword") {
      // Handle form submission, e.g., send data to server
      console.log("Form submitted:", { username, password });
      // Log the user in if the credentials are valid
      console.log("User logged in successfully");
    } 
    else {
      // Display an error message if the user hasn't registered
      setError("User not registered. Please sign up.");
      // Clear form fields after submission
      setUsername("");
      setPassword("");
    }
  };

  return (
    <div>
      {error && (
        <div className="alert alert-warning" role="alert">
          {error}
        </div>
      )}
      <div className="heading">{heading}</div>
      <form onSubmit={handleSubmit}>
        <input
          className="login-entry"
          type="text"
          name="username"
          value={username}
          onChange={handleChange}
          placeholder="Username"
        />
        <input
          className="login-entry"
          type="password"
          name="password"
          value={password}
          onChange={handleChange}
          placeholder="Password"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Login;
