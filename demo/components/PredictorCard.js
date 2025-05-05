import React, { useState } from "react";
import axios from "axios";

function PredictorCard({ title, endpoint, fields }) {
  const [formData, setFormData] = useState({});
  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(endpoint, formData);
      setPrediction(res.data.prediction);
    } catch (err) {
      console.error("Tahmin hatası:", err);
    }
  };

  return (
    <div className="bg-white text-black p-6 rounded-xl shadow-lg dark:bg-gray-800 dark:text-white">
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      <form onSubmit={handleSubmit}>
        {fields.map((field) => (
          <input
            key={field}
            type="number"
            step="any"
            name={field}
            onChange={handleChange}
            placeholder={field.replace("_", " ")}
            className="w-full mb-3 px-4 py-2 border rounded-md dark:bg-gray-700"
            required
          />
        ))}
        <button type="submit" className="w-full bg-green-700 text-white py-2 rounded-md hover:bg-green-600">
          Tahmin Et
        </button>
      </form>
      {prediction !== null && (
        <div className="mt-4 text-lg font-semibold">
          Tahmin: <span className="text-green-600 dark:text-green-400">{prediction}</span>
        </div>
      )}
    </div>
  );
}

export default PredictorCard;
