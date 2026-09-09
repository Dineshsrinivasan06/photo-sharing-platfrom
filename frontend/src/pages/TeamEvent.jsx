import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import api from "../services/api.js";


function TeamEvent() {

  const { eventId } = useParams();

  const [event, setEvent] = useState(null);
  const [photos, setPhotos] = useState([]);

  const [selectedFiles, setSelectedFiles] = useState([]);

  const [uploading, setUploading] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");


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
        `/photos/my-photos/${eventId}`
      );

      setPhotos(response.data);

    } catch (error) {

      setError(
        error.response?.data?.detail ||
        "Unable to load photos"
      );
    }
  };


  useEffect(() => {

    loadEvent();
    loadPhotos();

  }, [eventId]);


  const handleFileChange = (e) => {

    setSelectedFiles(
      Array.from(e.target.files)
    );

    setMessage("");
    setError("");
  };


  const uploadPhotos = async () => {

    if (selectedFiles.length === 0) {

      setError("Please select at least one photo");

      return;
    }

    setUploading(true);
    setMessage("");
    setError("");

    try {

      const formData = new FormData();

      selectedFiles.forEach((file) => {

        formData.append(
          "files",
          file
        );

      });


      const response = await api.post(
        `/photos/upload-multiple/${eventId}`,
        formData
      );


      setMessage(
        `${response.data.count} photo(s) uploaded successfully`
      );

      setSelectedFiles([]);

      document.getElementById(
        "photo-input"
      ).value = "";


      await loadPhotos();

    } catch (error) {

      setError(
        error.response?.data?.detail ||
        "Photo upload failed"
      );

    } finally {

      setUploading(false);
    }
  };


  if (!event) {
    return (
      <div className="page">
        <p>Loading...</p>
      </div>
    );
  }


  return (
    <div className="page">

      <h1>{event.name}</h1>

      <p>{event.description}</p>


      {message && (
        <div className="success">
          {message}
        </div>
      )}


      {error && (
        <div className="error">
          {error}
        </div>
      )}


      <section className="upload-section">

        <h2>Upload Photos</h2>

        <input
          id="photo-input"
          type="file"
          accept="image/jpeg,image/png,image/webp"
          multiple
          onChange={handleFileChange}
        />


        {selectedFiles.length > 0 && (

          <div>

            <p>
              {selectedFiles.length} photo(s) selected
            </p>

            <button
              onClick={uploadPhotos}
              disabled={uploading}
            >

              {uploading
                ? "Uploading..."
                : "Upload Photos"}

            </button>

          </div>
        )}

      </section>


      <section>

        <h2>
          My Uploaded Photos
        </h2>


        {photos.length === 0 ? (

          <p>
            You haven't uploaded any photos yet.
          </p>

        ) : (

          <div className="photo-grid">

            {photos.map((photo) => (

              <div
                className="photo-card"
                key={photo.id}
              >

                <h4>
                  {photo.filename}
                </h4>

                <p>
                  Size:{" "}
                  {(photo.file_size / 1024).toFixed(1)}
                  {" "}KB
                </p>

                <small>
                  Uploaded by you
                </small>

              </div>

            ))}

          </div>
        )}

      </section>

    </div>
  );
}


export default TeamEvent;