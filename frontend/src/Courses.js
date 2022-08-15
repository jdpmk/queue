import './App.css';
import { useEffect, useState } from 'react';

function deserializeWeeklyMetadata(metadata) {
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const occurs = [];

  for (let i = 0; i < 7; i++) {
    occurs.push(metadata & 1);
    metadata >>= 1;
  }

  occurs.reverse();

  return days.filter((_, i) => occurs[i]).join(", ");
}

function Courses({ userId }) {
  const [courses, setCourses] = useState([]);
  const [courseToAssignments, setCourseToAssignments] = useState({});

  useEffect(() => {
    fetch(`http://localhost:5000/user/${userId}/courses`)
      .then(res => res.json())
      .then(res => setCourses(res));
  }, [userId]);

  useEffect(() => {
    if (courses.length !== 0) {
      Promise.all(courses.map(course =>
        fetch(`http://localhost:5000/course/${course.course_id}/assignments`)
          .then(res => res.json())
          .then(res => res)))
        .then(courseAssignments =>
          courseAssignments.map((assignments, i) =>
            setCourseToAssignments(courseToAssignments =>
              ({...courseToAssignments, [courses[i].course_id]: assignments})
            )
          )
        );
    }
  }, [courses]);

  return (
    <div className="Courses">
      <h2>Courses</h2>
      <p>These are your active assignments.</p>
      {courses && Object.keys(courseToAssignments).length > 0 && courses.map(course =>
        <div key={course.course_id}>
          <h4>{course.department} {course.number} {course.name}</h4>
          {courseToAssignments[course.course_id].map(assignment =>
            <div key={assignment.assignment_id}>
              <p>{assignment.name} | {assignment.frequency === 0
                  ? "Everyday"
                  : `Weekly on ${deserializeWeeklyMetadata(assignment.frequency_metadata)}`
                }
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Courses;
