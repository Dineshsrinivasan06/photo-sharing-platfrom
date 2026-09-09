import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import api from "../services/api.js";


function EventDetails() {

  const { eventId } = useParams();

  const [event, setEvent] = useState(null);

  const [photos, setPhotos] = useState([]);

  const [error, setError] = useState("");

  const[message, setMessage] = useState("");
  


  useEffect(() => {

    loadEvent();
    loadPhotos();

  }, [eventId]);


  const loadEvent = async () => {

    try {

      const response = await api.get(
        `/events/${eventId}`
      );

      setEvent(response.data);

    } catch (error) {

      setError(
        error.response?.data?.detail ||
        "Unable to load event"
      );
    }
  };


  const loadPhotos = async () => {

    try {

      const response = await api.get(
        `/photos/event/${eventId}`
      );

      setPhotos(response.data);

    } catch (error) {

      console.log(error);
    }
  };


  if (!event) {
    return <p>Loading...</p>;
  }


  return (
    <div className="page">

      <h1>{event.name}</h1>

      <p>{event.description}</p>

      {error && (
        <div className="error">
          {error}
        </div>
      )}


      <h2>Photos</h2>

      <div className="photo-grid">

        {photos.map((photo) => (

          <div
            className="photo-card"
            key={photo.id}
          >

            <p>{photo.filename}</p>

            <span>
              {photo.is_selected
                ? "Selected"
                : "Not selected"}
            </span>

          </div>

        ))}

      </div>

    </div>
  );
}


export default EventDetails;