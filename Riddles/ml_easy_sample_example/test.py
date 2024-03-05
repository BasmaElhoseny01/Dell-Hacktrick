import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the data
data = pd.read_csv('E:\MY Work\Dell_Competation\Dell-Hacktrick\Riddles\ml_easy_sample_example\series_data.csv')
data = data.dropna()

data['timestamp'] = pd.to_datetime(data['timestamp'])
# remove rows with null values
data = data.set_index('timestamp')

# Fit ARIMA model
model = ARIMA(data, order=(5, 1, 1))
model_fit = model.fit()

# Make predictions
predictions = model_fit.forecast(steps=50).values  # Convert to array
predictions=predictions.tolist()
print(predictions)
print(type(predictions))

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

