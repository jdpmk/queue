import './App.css';
import { useEffect, useState } from 'react';

const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

function deserializeWeeklyMetadata(metadata) {
  const occurs = [];

  for (let i = 0; i < 7; i++) {
    occurs.push(metadata & 1);
    metadata >>= 1;
  }

  occurs.reverse();

  return DAYS.filter((_, i) => occurs[i]).join(", ");
}

function formatDate(dateAsString) {
  const date = new Date(Date.parse(dateAsString));

  const dayOfTheWeek = DAYS[date.getUTCDay()];
  const month = date.getUTCMonth() + 1;
  const day = date.getUTCDate();
  const year = date.getUTCFullYear();

  return `${dayOfTheWeek}, ${month}/${day}/${year}`;
}

function Upcoming({ userId }) {
  const [courses, setCourses] = useState([]);
  const [courseToAssignments, setCourseToAssignments] = useState({});

  const [today, setToday] = useState([]);
  const [tomorrow, setTomorrow] = useState([]);
  const [thisWeek, setThisWeek] = useState([]);
  const [nextWeek, setNextWeek] = useState([]);

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

  useEffect(() => {
    if (Object.keys(courseToAssignments).length === courses.length) {
      const assignments = Object.values(courseToAssignments).reduce(
        (acc, assignments) => [...acc, ...assignments],
        []);

      Promise.all(assignments.map(assignment =>
        fetch(`http://localhost:5000/assignment/${assignment.assignment_id}/upcoming`)
          .then(res => res.json())
          .then(res => res)))
        .then(upcomingAssignments =>
          upcomingAssignments.map((assignment, i) => {
            if (assignment.today) setToday(today => [...today, [formatDate(assignment.today[0]), assignments[i]]]);
            if (assignment.tomorrow) setTomorrow(tomorrow => [...tomorrow, [formatDate(assignment.tomorrow[0]), assignments[i]]]);
            if (assignment.this_week) setThisWeek(thisWeek => [...thisWeek, [formatDate(assignment.this_week[0]), assignments[i]]]);
            if (assignment.next_week) setNextWeek(nextWeek => [...nextWeek, [formatDate(assignment.next_week[0]), assignments[i]]]);
          }));
    }
  }, [courseToAssignments]);

  return (
    <div className="Upcoming">
      <h3>Today</h3>
      {today.map(dateAssignment => {
        const [date, assignment] = dateAssignment;
        return (
          <div>
            <p><strong>{assignment.name}</strong> | {assignment.description} | {date}</p>
          </div>
        );
      })}
      <h3>Tomorrow</h3>
      {tomorrow.map(dateAssignment => {
        const [date, assignment] = dateAssignment;
        return (
          <div>
            <p><strong>{assignment.name}</strong> | {assignment.description} | {date}</p>
          </div>
        );
      })}
      <h3>This Week</h3>
      {thisWeek.map(dateAssignment => {
        const [date, assignment] = dateAssignment;
        return (
          <div>
            <p><strong>{assignment.name}</strong> | {assignment.description} | {date}</p>
          </div>
        );
      })}
      <h3>Next Week</h3>
      {nextWeek.map(dateAssignment => {
        const [date, assignment] = dateAssignment;
        return (
          <div>
            <p><strong>{assignment.name}</strong> | {assignment.description} | {date}</p>
          </div>
        );
      })}
    </div>
  );
}

export default Upcoming;
