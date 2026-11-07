const STEPS = [
  {
    title: "Verify",
    text: "Tutors apply for a course with their grade. It is checked against the course's minimum grade.",
  },
  {
    title: "Match",
    text: "Students search by course, budget and rating, and tutors are ranked by a match score.",
  },
  {
    title: "Book",
    text: "Tutors offer one-to-one or group sessions. A seat is never booked twice.",
  },
  {
    title: "Pay",
    text: "The payment is held until the session is completed, then released to the tutor.",
  },
  {
    title: "Review",
    text: "Students who paid rate the session, and the ratings feed back into matching.",
  },
];

const BENEFITS = [
  "A tutor is listed only after their grade is approved.",
  "Sessions cannot overlap, and a full session cannot be booked.",
  "Money is held until the session is done, and refunded if it is cancelled.",
  "Only students who paid can leave a review.",
];

export default function HowItWorks() {
  return (
    <section className="process dark" aria-labelledby="how-title">
      <div className="wrap">
        <h2 id="how-title">How StudyBuddy works</h2>
        <ol className="steps">
          {STEPS.map((step, index) => (
            <li key={step.title}>
              <span className="step-num" aria-hidden="true">
                {index + 1}
              </span>
              <h3>{step.title}</h3>
              <p>{step.text}</p>
            </li>
          ))}
        </ol>
        <div className="why">
          <h2>Built to be fair to both sides</h2>
          <ul>
            {BENEFITS.map((text) => (
              <li key={text}>{text}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
