import { useState } from "react";
import "./App.css";

function App() {
  const [listings, setListings] = useState([]);
  const [searchParams, setSearchParams] = useState({
    make: "",
    model: "",
    minPrice: "",
    maxPrice: "",
    minYear: "",
    maxYear: "",
    minMileage: "",
    maxMileage: "",
    transmission: "",
    daysListed: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSearchParams({ ...searchParams, [name]: value });
  };

  const handleSearch = () => {
    const { make, model } = searchParams;
    fetch("http://localhost:5000/api/scrape", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ make, model }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Response data:", data);
        if (data.success) {
          setListings(data.data);
        } else {
          console.error("Scrape failed:", data.error);
        }
      })
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6">
        Search Facebook Marketplace Cars in Calgary
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <input
          type="text"
          name="make"
          placeholder="Make"
          value={searchParams.make}
          onChange={handleChange}
          className="p-2 border rounded-lg w-full"
        />
        <input
          type="text"
          name="model"
          placeholder="Model"
          value={searchParams.model}
          onChange={handleChange}
          className="p-2 border rounded-lg w-full"
        />
        <button
          onClick={handleSearch}
          className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600"
        >
          Search
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {listings.map((car, index) => (
          <div key={index} className="bg-white p-4 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold">{car.title}</h2>
            <p className="text-gray-600">Price: {car.price}</p>
            <p className="text-gray-600">Location: {car.location}</p>
            <p className="text-gray-600">Mileage: {car.mileage}</p>
            <p className="text-gray-600">Year: {car.year}</p>
            <a
              href={car.link}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 inline-block text-blue-500 hover:underline"
            >
              View Listing
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
