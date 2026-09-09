import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";

import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import AdminDashboard from "./pages/AdminDashboard";
import Events from "./pages/Events";
import EventDetails from "./pages/EventDetails";

import TeamDashboard from "./pages/TeamDashboard";
import TeamEvent from "./pages/TeamEvent";
import CreateGallery from "./pages/CreateGallery";
import CustomerGallery from "./pages/CustomerGallery";


function App() {

  return (

    <BrowserRouter>

      <AuthProvider>

        <Routes>

          <Route
            path="/login"
            element={<Login />}
          />


          {/* ADMIN */}

          <Route
            path="/admin"
            element={
              <ProtectedRoute role="ADMIN">
                <AdminDashboard />
              </ProtectedRoute>
            }
          />


          <Route
            path="/events"
            element={
              <ProtectedRoute role="ADMIN">
                <Events />
              </ProtectedRoute>
            }
          />


          <Route
            path="/events/:eventId"
            element={
              <ProtectedRoute>
                <EventDetails />
              </ProtectedRoute>
            }
          />


          {/* TEAM MEMBER */}

          <Route
            path="/team"
            element={
              <ProtectedRoute role="TEAM_MEMBER">
                <TeamDashboard />
              </ProtectedRoute>
            }
          />


          <Route
            path="/team/events/:eventId"
            element={
              <ProtectedRoute role="TEAM_MEMBER">
                <TeamEvent />
              </ProtectedRoute>
            }
          />
          <Route
  path="/events/:eventId/gallery"
  element={
    <ProtectedRoute role="ADMIN">
      <CreateGallery />
    </ProtectedRoute>
  }
/>

<Route
path="/gallery/:token"
element={<CustomerGallery />}
/>  

          <Route
            path="*"
            element={<Login />}
          />

        </Routes>

      </AuthProvider>

    </BrowserRouter>
  );
}


export default App;