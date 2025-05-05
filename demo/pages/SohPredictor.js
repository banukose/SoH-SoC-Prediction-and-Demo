import React, { useState } from 'react';
import axios from 'axios';

/**
 * Bu bileşen, kullanıcıdan voltaj, akım ve sıcaklık alarak
 * Flask API üzerinden SoH tahmini yapar.
 */
const SohPredictor = () => {
  const [avgVoltage, setAvgVoltage] = useState(3.7);
  const [avgCurrent, setAvgCurrent] = useState(2.0);
  const [maxTemp, setMaxTemp] = useState(35.0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post('http://localhost:5001/predict-soh', {
        avg_voltage: avgVoltage,
        avg_current: avgCurrent,
        max_temperature: maxTemp,
      });
      setResult(response.data.predicted_soh);
    } catch (err) {
      console.error(err);
      setResult('Hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>🔋 SOH Tahmini</h3>
      <label>Ortalama Voltaj (V):</label>
      <input type="number" step="0.01" value={avgVoltage} onChange={e => setAvgVoltage(parseFloat(e.target.value))} />
      <br />
      <label>Ortalama Akım (A):</label>
      <input type="number" step="0.1" value={avgCurrent} onChange={e => setAvgCurrent(parseFloat(e.target.value))} />
      <br />
      <label>Maksimum Sıcaklık (°C):</label>
      <input type="number" step="1" value={maxTemp} onChange={e => setMaxTemp(parseFloat(e.target.value))} />
      <br /><br />
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Tahmin yapılıyor...' : 'Tahmin Al'}
      </button>
      {result && <p>🔮 Tahmin Edilen SoH: {result.toFixed(4)}</p>}
    </div>
  );
};

export default SohPredictor;
