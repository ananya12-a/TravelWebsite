import React, { useState } from "react";

function Register(props) {
  const { heading } = props;
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmpassword, setConfirmpassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name == "username") {
      setUsername(value);
    } else if (name == "password") {
      setPassword(value);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password !== confirmpassword) {
      setError("Passwords do not match!");
      setPassword("");
      setConfirmpassword("");
      return;
    }
    // Handle form submission, e.g., send data to server
    console.log("Form submitted:", {
      username,
      password,
      confirmpassword,
      email,
      firstname,
      lastname,
    });
    // Clear form fields after submission
    setUsername("");
    setPassword("");
    setConfirmpassword("");
    setEmail("");
    setFirstname("");
    setLastname("");
    setError("");
  };

  return (
    <div>
      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}
      <div className="heading">{heading}</div>
      <form onSubmit={handleSubmit} className="register-container">
        <input
          className="register-entry"
          type="text"
          name="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          className="register-entry"
          type="password"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <input
          className="register-entry"
          type="password"
          name="password"
          value={confirmpassword}
          onChange={(e) => setConfirmpassword(e.target.value)}
          placeholder="Confirm Password"
        />
        <input
          className="register-entry"
          type="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          className="register-entry"
          type="name"
          name="firstname"
          value={firstname}
          onChange={(e) => setFirstname(e.target.value)}
          placeholder="First Name"
        />
        <input
          className="register-entry"
          type="name"
          name="lastname"
          value={lastname}
          onChange={(e) => setLastname(e.target.value)}
          placeholder="Last Name"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Register;