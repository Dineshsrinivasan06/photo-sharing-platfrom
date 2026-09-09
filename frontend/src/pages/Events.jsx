import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../services/api.js";



function Events() {

  const [events, setEvents] = useState([]);

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const [error, setError] = useState("");
}