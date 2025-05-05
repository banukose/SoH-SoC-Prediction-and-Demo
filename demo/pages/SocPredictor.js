import React, { useState } from 'react';
import axios from 'axios';

/**
 * Bu bileşen, kullanıcıdan CSV formatında 50 satırlık zaman serisi alarak
 * SoC tahmini için Flask API'ye gönderir.
 */
const SocPredictor = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handlePredict = async () => {
    if (!file) return alert("Lütfen bir CSV dosyası yükleyin.");
    setLoading(true);
    setResult(null);

    try {
      const text = await file.text();
      const lines = text.trim().split('\n').slice(1); // header'ı atla
      const sequence = lines.map(line => line.split(',').map(Number));

      if (sequence.length !== 50 || sequence[0].length !== 3) {
        return alert("CSV dosyası 50 satır ve 3 sütun (voltage,current,temperature) içermelidir.");
      }

      const response = await axios.post('http://localhost:5001/predict-soc', {
        sequence: sequence
      });

      setResult(response.data.predicted_soc);
    } catch (err) {
      console.error(err);
      setResult("Tahmin hatası oluştu.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>📊 SOC Tahmini</h3>
      <p>CSV dosyası yükleyin: 50 satır, 3 sütun: <b>voltage,current,temperature</b></p>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <br /><br />
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Tahmin yapılıyor...' : 'Tahmin Al'}
      </button>
      {result && <p>🔋 Tahmin Edilen SOC: {result.toFixed(4)}</p>}
    </div>
  );
};

export default SocPredictor;
