import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../services/api";
import { useAuth } from "../context/AuthContext";


function TeamDashboard() {

  const { logout } = useAuth();

  const [events, setEvents] = useState([]);
  const [error, setError] = useState("");

  const loadEvents = async () => {

    try {

      const response = await api.get("/events/");

      setEvents(response.data);

    } catch (error) {

      setError(
        error.response?.data?.detail ||
        "Unable to load assigned events"
      );
    }
  };


  useEffect(() => {
    loadEvents();
  }, []);


  return (
    <div>

      <header className="navbar">

        <h2>PhotoShare</h2>

        <button onClick={logout}>
          Logout
        </button>

      </header>


      <main className="page">

        <h1>Team Dashboard</h1>

        <p>
          Your assigned photography events
        </p>

        {error && (
          <div className="error">
            {error}
          </div>
        )}


        <div className="event-grid">

          {events.map((event) => (

            <Link
              key={event.id}
              to={`/team/events/${event.id}`}
              className="event-card"
            >

              <h3>{event.name}</h3>

              <p>
                {event.description}
              </p>

              <span>
                Open Event →
              </span>

            </Link>

          ))}

        </div>


        {events.length === 0 && !error && (
          <p>
            No events have been assigned to you yet.
          </p>
        )}

      </main>

    </div>
  );
}


export default TeamDashboard;