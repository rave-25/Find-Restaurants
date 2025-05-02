import React from "react";

const SearchRestaurants = ({ restaurants }) => {
  if (!restaurants.length) return null;

  return (
    <table style={{ marginTop: "2rem", width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th>Name</th>
          <th>Address</th>
          <th>Cuisine</th>
          <th>Rating</th>
          <th>Price Level</th>
          <th>Hours</th>
        </tr>
      </thead>
      <tbody>
        {restaurants.map((r, index) => (
          <tr key={index}>
            <td>{r.name}</td>
            <td>{r.address}</td>
            <td>{r.cuisine || "N/A"}</td>
            <td>{r.rating || "N/A"}</td>
            <td>{r.price_level || "N/A"}</td>
            <td>{r.hours || "N/A"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default SearchRestaurants;
