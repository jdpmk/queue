import './App.css';
import Landing from './Landing.js';
import Nav from './Nav.js';
import Courses from './Courses.js';
import Upcoming from './Upcoming.js';

function App() {
  return (
    <div className="App">
      <Nav />
      <Landing userId={1} />
      <Upcoming userId={1} />
      <Courses userId={1} />
    </div>
  );
}

export default App;
