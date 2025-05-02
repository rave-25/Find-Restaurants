import React, { useState } from "react";
import SearchRestaurants from "./components/SearchRestaurants";
import "./styles/style.css";

function App() {
  const [query, setQuery] = useState("");
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: query }),
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();
      setRestaurants(data);
    } catch (err) {
      setError("Failed to fetch results.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Restaurants Finder</h1>
      <div className="input-group">
        <input
          type="text"
          className="input-text"
          placeholder="Search for restaurants..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button className="button" onClick={handleSearch}>
          Search
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      <SearchRestaurants restaurants={restaurants} />
    </div>
  );
}

export default App;
