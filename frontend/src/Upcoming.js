import './App.css';
import { useEffect, useState } from 'react';

function Upcoming({ userId }) {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5000/user/${userId}/courses`)
      .then(res => res.json())
      .then(res => setCourses(res));
  }, [userId]);

  return (
    <div className="Upcoming">
      {courses.map(course =>
        <div key={course.course_id}>
          <h4>{course.department} {course.number} {course.name}</h4>
        </div>
      )}
    </div>
  );
}

export default Upcoming;
