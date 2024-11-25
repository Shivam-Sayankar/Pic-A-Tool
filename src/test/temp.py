from datetime import datetime

# Generate the timestamp
current_time = datetime.now()
timestamp = current_time.strftime("%d-%b-%Y_%H-%M-%S")

# Create the filename
filename = f"{timestamp}.json"

print(filename)  # Outputs something like "25-Nov-2024_22-53-32.json"
