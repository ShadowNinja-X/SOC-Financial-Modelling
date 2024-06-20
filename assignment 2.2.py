import numpy as np
from datetime import datetime
dirty_price = float(input("Enter last traded (dirty) price PD: "))
coupon_rate = float(input("Enter coupon rate rC (in percentage): ")) / 100
coupon_frequency = int(input("Enter coupon frequency m: "))
face_value = float(input("Enter face value PT: "))
maturity_date = input("Enter maturity date T (in format DD-MM-YYYY): ")
purchase_date = input("Enter current date t (in format DD-MM-YYYY): ")
last_coupon_date = input("Enter recent past coupon payment date (in format DD-MM-YYYY): ")

def ytm_newton_raphson(face_value, dirty_price, coupon_rate, coupon_frequency, last_coupon_date, purchase_date,
                       maturity_date, max_iter=10, tol=1e-6):
    # Convert dates to datetime objects
    last_coupon_date = datetime.strptime(last_coupon_date, "%d-%m-%Y")
    purchase_date = datetime.strptime(purchase_date, "%d-%m-%Y")
    maturity_date = datetime.strptime(maturity_date, "%d-%m-%Y")

    # Calculate days since last coupon and accrued interest
    days_since_last_coupon = (purchase_date - last_coupon_date).days
    days_in_year = 365
    accrued_interest = (coupon_rate * face_value) * (days_since_last_coupon / days_in_year)

    # Calculate clean price
    clean_price = dirty_price - accrued_interest

    # Calculate cash flows
    coupon_payment = (coupon_rate * face_value) / coupon_frequency
    years_to_maturity = (maturity_date - purchase_date).days / days_in_year
    num_coupons = int(np.ceil(years_to_maturity * coupon_frequency))

    # Newton-Raphson method
    def bond_price_ytm(ytm):
        return sum(
            [coupon_payment / (1 + ytm / coupon_frequency) ** (i + 1) for i in range(num_coupons)]) + face_value / (
                    1 + ytm / coupon_frequency) ** num_coupons

    def bond_price_derivative_ytm(ytm):
        return sum([-(i + 1) * coupon_payment / coupon_frequency / (1 + ytm / coupon_frequency) ** (i + 2) for i in
                    range(num_coupons)]) - num_coupons * face_value / coupon_frequency / (
                    1 + ytm / coupon_frequency) ** (num_coupons + 1)

    ytm = coupon_rate  # Initial guess
    for _ in range(max_iter):
        price = bond_price_ytm(ytm)
        derivative = bond_price_derivative_ytm(ytm)
        ytm_new = ytm - (price - clean_price) / derivative
        if abs(ytm_new - ytm) < tol:
            ytm = ytm_new
            break
        ytm = ytm_new

    return ytm



# Calculate YTM
ytm = ytm_newton_raphson(face_value, dirty_price, coupon_rate, coupon_frequency, last_coupon_date, purchase_date,
                         maturity_date)
ytm_annual = ytm * coupon_frequency  # Adjust for coupon payment frequency

print(f"Yield to Maturity (YTM): {ytm_annual:.4f} or {ytm_annual * 100:.2f}%")
