import pandas as pd
import numpy as np

# Örnek CSV için rastgele ama mantıklı değerler üreten kod bloğu
np.random.seed(42)
data = {
    "voltage": np.random.normal(3.7, 0.05, 50),        # Ortalama 3.7V
    "current": np.random.normal(0.5, 0.1, 50),         # Ortalama 0.5A
    "temperature": np.random.normal(25, 1.5, 50)       # Ortalama 25°C
}

df = pd.DataFrame(data)
csv_path = "./example_soc_input.csv"
df.to_csv(csv_path, index=False)