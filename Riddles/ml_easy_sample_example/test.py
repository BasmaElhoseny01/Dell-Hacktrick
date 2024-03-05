import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the data
data = pd.read_csv('E:\MY Work\Dell_Competation\Dell-Hacktrick\Riddles\ml_easy_sample_example\series_data.csv')
data['timestamp'] = pd.to_datetime(data['timestamp'])
data = data.set_index('timestamp')

# # Train-test split
# train_size = int(len(data) * 0.8)
# train, test = data[:train_size], data[train_size:]

# Fit ARIMA model
model = ARIMA(data, order=([1,9,5], 1, [1,3,4]))
model_fit = model.fit()

# Make predictions
predictions = model_fit.forecast(steps=50).values  # Convert to array
print(predictions)

result=[]
with open('E:/MY Work/Dell_Competation/Dell-Hacktrick/Riddles/ml_easy_sample_example/result.txt', 'r') as file:
    # Read the content of the file
    content = file.read()
    # Evaluate the content as a Python expression to convert it into a list
    result = eval(content)

print(result)
# Evaluate the model
rmse = np.sqrt(mean_squared_error(result, predictions))
print(f'Root Mean Square Error (RMSE): {rmse}')

# Visualize actual vs predicted values (optional)
# import matplotlib.pyplot as plt

# plt.plot(test, label='Actual')
# plt.plot(predictions, label='Predicted')
# plt.legend()
# plt.show()
# import pandas as pd
# import matplotlib.pyplot as plt
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# from statsmodels.tsa.stattools import adfuller

# # Load the data
# data = pd.read_csv('E:\MY Work\Dell_Competation\Dell-Hacktrick\Riddles\ml_easy_sample_example\series_data.csv')
# data['timestamp'] = pd.to_datetime(data['timestamp'])
# data = data.set_index('timestamp')

# # Check for stationarity
# result = adfuller(data['visits'])
# print(f'ADF Statistic: {result[0]}, p-value: {result[1]}')

# # Plot ACF and PACF
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
# plot_acf(data['visits'], lags=30, ax=ax1)
# plot_pacf(data['visits'], lags=30, ax=ax2)
# plt.show()

