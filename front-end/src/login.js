import React, { useState } from "react";
import "./login.css"
import { useNavigate } from 'react-router-dom';
import myImage from './primoPic.png';
export default function LoginComp() {
  
  const navigate = useNavigate();

  const navigateToDestination = () => {
    navigate('/signup');
  };
    return(
    <div className="login-page">
        <div className='loginform-container'>
        <LoginForm></LoginForm>
        </div>

        <div className="loginform-section2">
          
          <p className="login-header-text">Wisher Planner</p>
      
          <p className="login-welcome-text">Welcome back</p>
          <button onClick={navigateToDestination} className="toSignup-page">Sign up</button>
        </div>
        
    </div>
    );
}


function LoginForm() {
    const [formData, setFormData] = useState({
      username: "",
      password: "",
    });
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData({
        ...formData,
        [name]: value,
      });
    };
  
    const handleSubmit = (e) => {
      e.preventDefault();
      console.log("Form data submitted:", formData);
      // You can add your authentication logic here
    };
  
    return (
      <div className="login-form">
        <h2 className="form-header">Log in to Wisher Planner</h2>
        <form onSubmit={handleSubmit}>
          <div className="loginform-group">
            <input
              placeholder="username"
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div className="loginform-group">
          
            <input
              placeholder="password"
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <button className="log-in-button" type="submit">Login</button>
          </div>
        
        </form>
      </div>
    );
  }
  