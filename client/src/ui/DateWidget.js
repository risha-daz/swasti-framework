import React from "react";

const DateWidget = () => {
  const dayNames = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursdsay",
    "Friday",
    "Saturday",
  ];
  const month = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  var today = new Date(),
    date =
      month[today.getMonth() + 1] +
      "  " +
      today.getDay() +
      ", " +
      today.getFullYear();
  return (
    <div>
      <h1>{dayNames[today.getDay()]}</h1> <h4>{date}</h4>
    </div>
  );
};

export default DateWidget;
