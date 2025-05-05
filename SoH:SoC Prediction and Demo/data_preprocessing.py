import scipy.io
import pandas as pd
import numpy as np
import os

#SoH için veri hazırlığı
def extract_battery_data_for_soh(file_path: str, battery_id: str) -> pd.DataFrame:
    mat = scipy.io.loadmat(file_path)
    data_key = next((k for k in mat.keys() if not k.startswith('__')), None)
    data = mat[data_key]
    
    cycles = data[0, 0]['cycle'][0]
    initial_capacity = None
    output = []

    for i, cycle in enumerate(cycles):
        op_type = str(cycle['type'][0])
        if op_type != 'discharge':
            continue

        cycle_data = cycle['data'][0, 0]
        if initial_capacity is None:
            initial_capacity = float(cycle_data['Capacity'][0][0])

        try:
            voltage = np.array(cycle_data['Voltage_measured']).flatten().astype(np.float64)
            current = np.array(cycle_data['Current_measured']).flatten().astype(np.float64)
            temperature = np.array(cycle_data['Temperature_measured']).flatten().astype(np.float64)
            capacity = float(cycle_data['Capacity'][0][0])
        except Exception as e:
            print(f"[Uyarı] {battery_id} döngü {i} veri işlenemedi: {e}")
            continue

        soh = capacity / initial_capacity if initial_capacity else np.nan

        output.append({
            'battery_id': battery_id,
            'cycle': i,
            'capacity': capacity,
            'soh': soh,
            'avg_voltage': np.mean(voltage),
            'avg_current': np.mean(current),
            'avg_temperature': np.mean(temperature),
            'max_temperature': np.max(temperature),
        })

    return pd.DataFrame(output)

#SoC için veri hazırlığı
def extract_battery_data_for_soc(file_path: str, battery_id: str) -> pd.DataFrame:

    mat = scipy.io.loadmat(file_path)
    data_key = next((k for k in mat.keys() if not k.startswith('__')), None)
    data = mat[data_key]

    cycles = data[0, 0]['cycle'][0]
    initial_capacity = None
    output = []

    for i, cycle in enumerate(cycles):
        op_type = str(cycle['type'][0])
        if op_type != 'discharge':
            continue

        cycle_data = cycle['data'][0, 0]
        if initial_capacity is None:
            try:
                initial_capacity = float(cycle_data['Capacity'][0][0])
                if initial_capacity <= 0:
                    print(f"[Uyarı] {battery_id} döngü {i} geçersiz kapasite: {initial_capacity}")
                    continue
            except:
                continue

        try:
            voltage = np.array(cycle_data['Voltage_measured']).flatten().astype(np.float64)
            current = np.array(cycle_data['Current_measured']).flatten().astype(np.float64)
            temperature = np.array(cycle_data['Temperature_measured']).flatten().astype(np.float64)
            time = np.array(cycle_data['Time']).flatten().astype(np.float64)
        except Exception as e:
            print(f"[Uyarı] {battery_id} döngü {i} zaman serisi verisi alınamadı: {e}")
            continue

        if len(time) == 0 or len(current) == 0 or initial_capacity is None:
            continue

        # Zamanın monoton olup olmadığını kontrol et
        if not np.all(np.diff(time) >= 0):
            print(f"[Uyarı] {battery_id} döngü {i} zaman monoton değil, atlanıyor.")
            continue

        # SOC'yi her zaman adımında hesapla
        delta_t = np.diff(time, prepend=time[0])  # zaman farkı
        discharged_ah_t = np.cumsum(np.abs(current) * delta_t) / 3600  # Ah cinsinden deşarj
        # SOC = 1 - (deşarj edilen enerji) / (başlangıç kapasitesi)
        # Burada zaman serisi boyunca anlık akımın entegrali alınarak deşarj miktarı Ah cinsinden hesaplanır.
        soc_series = 1 - discharged_ah_t / initial_capacity
        soc_series = np.clip(soc_series, 0, 1)  # SOC'yi 0-1 aralığına sınırla

        for t, v, c, temp, soc in zip(time, voltage, current, temperature, soc_series):
            output.append({
                'battery_id': battery_id,
                'cycle': i,
                'time': t,
                'voltage': v,
                'current': c,
                'temperature': temp,
                'soc': soc
            })

    return pd.DataFrame(output)

#Veri yükleme(SoH)
def load_all_batteries_soh(folder_path: str) -> pd.DataFrame:
    files = ['B0005.mat', 'B0006.mat', 'B0018.mat']
    all_data = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        battery_id = file.split('.')[0]
        battery_data = extract_battery_data_for_soh(file_path, battery_id)
        all_data.append(battery_data)
    return pd.concat(all_data, ignore_index=True)

#Veri yükleme(SoC)
def load_all_batteries_soc(folder_path: str) -> pd.DataFrame:
    files = ['B0005.mat', 'B0006.mat', 'B0018.mat']
    all_data = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        battery_id = file.split('.')[0]
        battery_data = extract_battery_data_for_soc(file_path, battery_id)
        all_data.append(battery_data)
    return pd.concat(all_data, ignore_index=True)

# Veri setlerinin kaydedileceği konumlar ve sonuç
if __name__ == "__main__":
    folder_path = "data/BatteryData"
    soh_output_path = "data/processed/battery_data_soh.csv"
    soc_output_path = "data/processed/battery_data_soc.csv"

    df_soh = load_all_batteries_soh(folder_path)
    df_soh.to_csv(soh_output_path, index=False)
    print(f"SOH verisi kaydedildi: {soh_output_path}")

    df_soc = load_all_batteries_soc(folder_path)
    df_soc.to_csv(soc_output_path, index=False)
    print(f"SOC verisi kaydedildi: {soc_output_path}")
