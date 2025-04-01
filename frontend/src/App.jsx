import React, { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

const App = () => {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState(null);

  const fetchWeather = async () => {
    try {
      setError(null); const response = await axios.get(`${import.meta.env.VITE_API_URL}/weather?city=${city}`);     
       setWeather(response.data);
    } catch (err) {
      setError("City not found or server error");
      setWeather(null);
    }
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black text-white overflow-hidden">
      
      {/* Animated Sun */}
      <motion.div
        initial={{ y: 300 }}
        animate={{ y: 200 }}
        transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}
        className="absolute top-10 left-20 w-20 h-20 bg-yellow-500 rounded-full shadow-lg"
      ></motion.div>

    {/* Cloud - More Realistic */}
<motion.div
  initial={{ x: -100 }}
  animate={{ x: 500 }}
  transition={{ duration: 8, repeat: Infinity, repeatType: "reverse" }}
  className="absolute top-10 left-20 flex items-center justify-center"
>
  <div className="relative w-32 h-20 bg-gray-100 rounded-full opacity-90">
    <div className="absolute w-32 h-16 bg-gray-100 rounded-full top-[-10px] left-10"></div>
    <div className="absolute w-32 h-18 bg-gray-100 rounded-full top-[11px] left-20"></div>
  </div>
</motion.div>
<motion.div
  initial={{ x: 800 }}
  animate={{ x: -300 }}
  transition={{ duration: 8, repeat: Infinity, repeatType: "reverse" }}
  className="absolute top-10 right-10 flex items-center justify-center"
>
  <div className="relative w-36 h-22 bg-gray-100 rounded-full opacity-90">
    <div className="absolute w-28 h-18 bg-gray-100 rounded-full top-[-8px] left-6"></div>
    <div className="absolute w-32 h-20 bg-gray-100 rounded-full top-[10px] left-16"></div>
  </div>
</motion.div>

      {/* Rain Effect */}
      <div className="absolute inset-0 pointer-events-none">
        {Array(30)
          .fill(0)
          .map((_, i) => (
            <motion.div
              key={i}
              initial={{ y: -10, opacity: 0.8 }}
              animate={{ y: "100vh", opacity: 0 }}
              transition={{ duration: Math.random() * 2 + 1, repeat: Infinity }}
              className="absolute w-1 h-6 bg-blue-400 opacity-50"
              style={{
                left: `${Math.random() * 100}vw`,
                top: `${Math.random() * 100}vh`,
              }}
            ></motion.div>
          ))}
      </div>

      {/* Weather Title */}
      <h1 className="text-4xl font-bold mb-6 drop-shadow-lg flex items-center">
        🌧️ Weather App
      </h1>

      {/* Weather Card */}
      <div className="relative bg-black/40 backdrop-blur-lg shadow-xl rounded-xl p-6 w-96 text-center border border-gray-700">
        <input
          type="text"
          placeholder="Enter city name"
          className="w-full p-3 rounded-lg bg-black/50 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <button
          onClick={fetchWeather}
          className="mt-4 w-full p-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-500 transition duration-200 shadow-md hover:shadow-blue-400"
        >
          Get Weather
        </button>

        {error && <p className="text-red-400 mt-4">{error}</p>}

        {weather && (
          <div className="mt-6 p-6 bg-black/20 rounded-xl text-white border border-gray-600">
            <h2 className="text-2xl font-semibold">{weather.city}</h2>
            <p className="text-4xl font-bold">{weather.temperature}°C</p>
            <p className="text-lg italic">{weather.description}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
