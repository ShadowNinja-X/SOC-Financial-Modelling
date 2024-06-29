import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# Function to calculate model price
def calculate_model_price(spot_price, interest_rate, time_to_maturity):
    return spot_price * np.exp(interest_rate * time_to_maturity)


# Read the input CSV file
input_csv_path = (r"C:\Users\siddh\Desktop\apple.csv")
df = pd.read_csv(input_csv_path)

# Add a column for calculated model price
interest_rate = 0.044  # prevailing interest rate
model_prices = []

for index, row in df.iterrows():
    current_date = datetime.strptime(row['Date'], '%d-%m-%Y')
    expiry_date = datetime.strptime(row['Expiry'], '%d-%m-%Y')
    time_to_maturity = (expiry_date - current_date).days / 365.0

    model_price = calculate_model_price(row['Underlying Value'], interest_rate, time_to_maturity)
    model_prices.append(model_price)

df['Model Price'] = model_prices
df['Spot Price'] = df['Underlying Value']
df['Settle Price'] = df['Close']

# Save the new metrics to a CSV file
output_csv_path = (r"C:\Users\siddh\Desktop\assignment3output.csv")
df.to_csv(output_csv_path, columns=['Date', 'Settle Price', 'Model Price', 'Spot Price'], index=False)

# Generate a graph
plt.figure(figsize=(14, 10))
plt.plot(df['Date'], df['Settle Price'], label='Settle Price', marker='o')
plt.plot(df['Date'], df['Model Price'], label='Model Price', marker='x')
plt.plot(df['Date'], df['Spot Price'], label='Spot Price', marker='s')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Future Pricing Analysis')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('future_pricing_analysis.png')
plt.show()

# Calculate mean interest rate and percentage error
calculated_interest_rates = []

for index, row in df.iterrows():
    current_date = datetime.strptime(row['Date'], '%d-%m-%Y')
    expiry_date = datetime.strptime(row['Expiry'], '%d-%m-%Y')
    time_to_maturity = (expiry_date - current_date).days / 365.0

    calculated_interest_rate = (np.log(row['Settle Price'] / row['Spot Price'])) / time_to_maturity
    calculated_interest_rates.append(calculated_interest_rate)

mean_interest_rate = np.mean(calculated_interest_rates)
percentage_error = abs(mean_interest_rate - interest_rate) / interest_rate * 100

print("A probable reason for the steep decline in the underlying value would be increase in the covid cases in India during early march and also about the news of a potentioal nationwide economic and travel lockdown going to be enforced in the country")
print(f"Mean Interest Rate: {mean_interest_rate:.4f}")
print(f"Percentage Error: {percentage_error:.2f}%")
