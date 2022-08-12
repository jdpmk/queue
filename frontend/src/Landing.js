import './App.css';
import { useEffect, useState } from 'react';

function Landing({ userId }) {
  const [firstName, setFirstName] = useState("");

  useEffect(() => {
    fetch(`http://localhost:5000/user/${userId}`)
      .then(res => res.json())
      .then(res => setFirstName(res.first_name));
  }, [userId]);

  return (
    <div className="Landing">
      <h1>Welcome, {firstName}.</h1>
      <p>Here's what's coming up.</p>
    </div>
  );
}

export default Landing;
