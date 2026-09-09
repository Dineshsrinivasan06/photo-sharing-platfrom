import { useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

function CustomerGallery() {
  const { token } = useParams();

  const [pin, setPin] = useState("");
  const [gallery, setGallery] = useState(null);
  const [photos, setPhotos] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const verifyPin = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      // Verify PIN
      const response = await api.post(
        `/gallery/${token}/verify`,
        {
          pin: pin,
        }
      );

      const galleryToken = response.data.access_token;

      // Get gallery photos
      const photosResponse = await api.get(
        `/gallery/${token}/photos`,
        {
          headers: {
            Authorization: `Bearer ${galleryToken}`,
          },
        }
      );

      setGallery(photosResponse.data.gallery);
      setPhotos(photosResponse.data.photos);

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Invalid PIN or gallery unavailable."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="customer-gallery">

      {!gallery && (
        <div className="pin-container">

          <h1>Photo Gallery</h1>

          <p>
            Enter the PIN provided by the event organizer.
          </p>

          <form onSubmit={verifyPin}>

            <input
              type="password"
              placeholder="Enter PIN"
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              required
            />

            <button type="submit" disabled={loading}>
              {loading ? "Verifying..." : "View Gallery"}
            </button>

          </form>

          {error && (
            <p className="error">
              {error}
            </p>
          )}

        </div>
      )}

      {gallery && (
        <div className="gallery-container">

          <div className="gallery-header">
            <h1>Photo Gallery</h1>

            <p>
              {photos.length} photos
            </p>
          </div>

          {photos.length === 0 ? (
            <p>No photos available.</p>
          ) : (
            <div className="customer-photo-grid">

              {photos.map((photo) => (
                <div
                  className="customer-photo-card"
                  key={photo.id}
                >
                  <img
                    src={photo.storage_location}
                    alt={photo.filename}
                  />
                </div>
              ))}

            </div>
          )}

        </div>
      )}

    </div>
  );
}

export default CustomerGallery;