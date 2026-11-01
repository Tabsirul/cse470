   import { useEffect, useState } from "react";

   function App() {
     const [status, setStatus] = useState("loading...");

     useEffect(() => {
       fetch("http://localhost:8000/api/health")
         .then((res) => res.json())
         .then((data) => setStatus(data.status + ", database " + data.database))
         .catch(() => setStatus("backend not reachable"));
     }, []);

     return <h1>StudyBuddy backend: {status}</h1>;
   }

   export default App;