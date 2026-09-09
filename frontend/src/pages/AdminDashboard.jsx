import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";


function AdminDashboard() {

  const { logout } = useAuth();

  return (
    <div>

      <header className="navbar">

        <h2>PhotoShare Admin</h2>

        <button onClick={logout}>
          Logout
        </button>

      </header>


      <main className="dashboard">

        <h1>Admin Dashboard</h1>

        <div className="dashboard-grid">

          <Link
            to="/events"
            className="dashboard-card"
          >
            <h2>Events</h2>
            <p>
              Create and manage photography events.
            </p>
          </Link>


          <div className="dashboard-card">
            <h2>Photos</h2>
            <p>
              Review and select uploaded photos.
            </p>
          </div>


          <div className="dashboard-card">
            <h2>Galleries</h2>
            <p>
              Create and publish customer galleries.
            </p>
          </div>

        </div>

      </main>

    </div>
  );
}


export default AdminDashboard;