import pandas as pd
import random
import string
from datetime import datetime, timedelta

# Generate random booking ID
def generate_booking_id(prefix):
    return prefix + ''.join(random.choices(string.digits, k=5)) + ''.join(random.choices(string.ascii_uppercase, k=3))

# Generate random customer ID
def generate_customer_id():
    return ''.join(random.choices(string.digits + string.ascii_uppercase, k=8))

# Generate random location
locations = [
    "Marina Bay Sands", "Gardens by the Bay", "Sentosa Island", "Singapore Zoo", "Universal Studios Singapore",
    "Orchard Road", "Clarke Quay", "Chinatown", "Little India", "Bugis Street", "Suntec City", "Marina Bay Financial Centre",
    "Raffles Place", "East Coast Park", "West Coast Park", "Changi Airport", "Tiong Bahru"
]

# Generate random date
def generate_random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()

# Define car brands and names
car_brands_and_names = [
    ("Toyota", "Corolla"), ("Hyundai", "Elantra"), ("Honda", "Civic"), ("Mercedes", "E-Class"),
    ("Toyota", "Camry"), ("Hyundai", "Sonata"), ("Honda", "Accord"), ("Mercedes", "S-Class")
]

# Initialize dataframe
columns = ["Date", "Time", "Booking ID", "Booking Status", "Customer ID", "Vehicle Type", "Pickup Location",
           "Drop Location", "VTAT", "CTAT", "Reason for Cancellation", "Ride Distance",
           "Driver Ratings", "Customer Ratings", "Booking Value", "Incomplete Rides", "Incomplete Rides Reason",
           "Customer Demand", "Vehicles Breakdown", "Other Issue", "Number of People", "Payment Method", "Car Brand",
           "Car Name", "Surge Amount"]

data = []

# Generate data
for _ in range(20000):
    date = generate_random_date(start_date, end_date)
    time = date.strftime("%H:%M:%S")
    booking_id = generate_booking_id("GR")
    customer_id = generate_customer_id()
    vehicle_type = random.choice(["Mini", "Prime", "Prime Plus", "Sedan"])
    pickup_location = random.choice(locations)
    drop_location = random.choice(locations)
    booking_status = random.choices(["Success", "Cancelled by Customer", "Cancelled by Driver"], weights=[62, 10, 15], k=1)[0]
    vtat = random.randint(5, 15) if booking_status == "Success" else 0
    ctat = random.randint(5, 10) if booking_status == "Success" else 0
    reason_for_cancellation = random.choice(
        ["Driver is not moving", "Driver asked to cancel", "Change of plans", "Wrong Address"]
    ) if booking_status != "Success" else None
    ride_distance = round(random.uniform(1, 25), 2) if booking_status == "Success" else None
    driver_ratings = round(random.uniform(1, 5), 1) if booking_status == "Success" else None
    customer_ratings = round(random.uniform(1, 5), 1) if booking_status == "Success" else None
    booking_value = round(random.uniform(10, 100), 2) if booking_status == "Success" else None
    incomplete_rides = random.choice([0, 1]) if random.uniform(0, 1) < 0.05 else 0
    incomplete_rides_reason = random.choice(["Customer Demand", "Vehicles Breakdown", "Other Issue"]) if incomplete_rides == 1 else None
    customer_demand = random.choice([0, 1])
    vehicles_breakdown = random.choice([0, 1])
    other_issue = random.choice([0, 1])
    number_of_people = random.randint(1, 4) if vehicle_type in ["Sedan", "Prime Plus"] else random.randint(1, 2) if vehicle_type == "Prime" else random.randint(1, 3)
    payment_method = random.choice(["QR code", "Cash", "eWallet", "Card"])
    car_brand, car_name = random.choice(car_brands_and_names)
    surge_amount = round(random.uniform(1.0, 5.0), 2) if customer_demand == 1 else 0

    data.append(
        [date.strftime("%Y-%m-%d"), time, booking_id, booking_status, customer_id, vehicle_type, pickup_location,
         drop_location, vtat, ctat, reason_for_cancellation, ride_distance, driver_ratings,
         customer_ratings, booking_value, incomplete_rides, incomplete_rides_reason, customer_demand,
         vehicles_breakdown, other_issue, number_of_people, payment_method, car_brand, car_name, surge_amount])

df = pd.DataFrame(data, columns=columns)

# Remove the "Cancelled Rides by Driver" column if present
if "Cancelled Rides by Driver" in df.columns:
    df.drop(columns=["Cancelled Rides by Driver"], inplace=True)

# Save to CSV
df.to_csv("cab_data_singapore.csv", index=False)
