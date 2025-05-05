import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [theme, setTheme] = useState("light");
  const [sohResult, setSohResult] = useState(null);
  const [socResult, setSocResult] = useState(null);
  const [sohInput, setSohInput] = useState({
    avg_voltage: "",
    avg_current: "",
    max_temperature: "",
  });
  const [socFile, setSocFile] = useState(null); // <-- CSV dosyası için eklendi

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
    document.body.className = theme === "light" ? "dark-theme" : "light-theme";
  };

  const handleSohChange = (e) => {
    setSohInput({ ...sohInput, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setSocFile(e.target.files[0]);
  };

  const predictSOH = async () => {
    const data = {
      avg_voltage: parseFloat(sohInput.avg_voltage),
      avg_current: parseFloat(sohInput.avg_current),
      max_temperature: parseFloat(sohInput.max_temperature),
    };
    try {
      const res = await axios.post("http://localhost:5001/predict-soh", data);
      console.log("SOH response:", res.data);
      setSohResult(res.data.soh);
    } catch (err) {
      console.error("SOH prediction error:", err);
    }
  };

  const predictSOC = async () => {
    if (!socFile) {
      alert("Lütfen bir CSV dosyası seçin.");
      return;
    }

    const formData = new FormData();
    formData.append("file", socFile);

    try {
      const res = await axios.post("http://localhost:5001/predict-soc", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("SOC response:", res.data);
      setSocResult(res.data.soc);
    } catch (err) {
      console.error("SOC prediction error:", err);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>🔋 Battery Health Prediction</h1>
        <button onClick={toggleTheme}>🎨 Tema Değiştir</button>
      </header>

      <div className="panels">
        <div className="panel">
          <h2>SOH Tahmini</h2>
          {["avg_voltage", "avg_current", "max_temperature"].map((name) => (
            <input
              key={name}
              name={name}
              placeholder={name.replace("_", " ")}
              onChange={handleSohChange}
            />
          ))}
          <button onClick={predictSOH}>Tahmin Et</button>
          {sohResult !== null && <div className="result">SOH: {Number(sohResult).toFixed(4)}</div>}
        </div>

        <div className="divider"></div>

        <div className="panel">
          <h2>SOC Tahmini</h2>
          <input type="file" accept=".csv" onChange={handleFileChange} />
          <button onClick={predictSOC}>Tahmin Et</button>
          {socResult !== null && <div className="result">SOC: {Number(socResult).toFixed(4)}</div>}
        </div>
      </div>
    </div>
  );
}

export default App;
