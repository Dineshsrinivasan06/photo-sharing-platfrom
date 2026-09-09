import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import api from "../services/api";


function CreateGallery() {

  const { eventId } = useParams();

  const navigate = useNavigate();

  const [pin, setPin] = useState("");

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [gallery, setGallery] = useState(null);

  const [loading, setLoading] = useState(false);


  const createGallery = async (e) => {

    e.preventDefault();

    setError("");
    setMessage("");
    setLoading(true);


    if (!/^\d+$/.test(pin)) {

      setError(
        "PIN must contain only numbers"
      );

      setLoading(false);

      return;
    }


    if (pin.length < 4) {

      setError(
        "PIN must contain at least 4 digits"
      );

      setLoading(false);

      return;
    }


    try {

      const response = await api.post(
        "/galleries/",
        {
          event_id: Number(eventId),
          pin
        }
      );


      setGallery(response.data);

      setMessage(
        "Gallery created successfully"
      );

    } catch (error) {

      setError(
        error.response?.data?.detail ||
        "Unable to create gallery"
      );

    } finally {

      setLoading(false);
    }
  };


  const publishGallery = async () => {

    if (!gallery) {
      return;
    }


    try {

      const response = await api.patch(
        `/galleries/${gallery.id}/publish`
      );


      setGallery({
        ...gallery,
        is_published: true
      });


      setMessage(
        "Gallery published successfully!"
      );


    } catch (error) {

      setError(
        error.response?.data?.detail ||
        "Unable to publish gallery"
      );
    }
  };


  return (

    <div className="page">

      <h1>Create Gallery</h1>

      <p>
        Select photos first, then create your
        customer gallery.
      </p>


      {error && (
        <div className="error">
          {error}
        </div>
      )}


      {message && (
        <div className="success">
          {message}
        </div>
      )}


      {!gallery ? (

        <form
          className="gallery-form"
          onSubmit={createGallery}
        >

          <label>
            Gallery PIN
          </label>

          <input
            type="password"
            inputMode="numeric"
            placeholder="Enter PIN"
            value={pin}
            onChange={(e) =>
              setPin(e.target.value)
            }
            maxLength={8}
            required
          />

          <p>
            Customers will use this PIN to
            access the gallery.
          </p>


          <button
            type="submit"
            disabled={loading}
          >

            {loading
              ? "Creating..."
              : "Create Gallery"}

          </button>

        </form>

      ) : (

        <div className="gallery-created">

          <h2>
            Gallery Created
          </h2>

          <p>
            Gallery ID: {gallery.id}
          </p>

          <p>
            Status:{" "}
            {gallery.is_published
              ? "Published"
              : "Not Published"}
          </p>


          {!gallery.is_published && (

            <button
              className="primary-button"
              onClick={publishGallery}
            >
              Publish Gallery
            </button>

          )}


          {gallery.is_published && (

            <div className="share-box">

              <h3>
                Share with Customer
              </h3>

              <p>
                Gallery Link:
              </p>

              <code>
                {window.location.origin}
                /gallery/
                {gallery.gallery_token}
              </code>

              <p>
                PIN: Use the PIN you created.
              </p>

            </div>

          )}

        </div>

      )}

    </div>
  );
}


export default CreateGallery;