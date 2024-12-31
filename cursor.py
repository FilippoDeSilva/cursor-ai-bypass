import json
import uuid
import pyfiglet

# Generate ASCII art for the text "CURSOR AI"
cursor_ai_art = pyfiglet.figlet_format("CURSOR AI")

# Print the ASCII art
print(cursor_ai_art)

# Path to the storage.json file
json_file_path = r'C:\Users\Filip\AppData\Roaming\Cursor\User\globalStorage\storage.json'

# Function to generate random UUID-like strings
def generate_random_id():
    return str(uuid.uuid4()).replace('-', '')

# Read the existing JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Failed to decode JSON data from the file.")
    exit(1)

# Change the telemetry values to random UUID-based values
data["telemetry.macMachineId"] = generate_random_id()
data["telemetry.sqmId"] = "{" + generate_random_id() + "}"
data["telemetry.machineId"] = generate_random_id()
data["telemetry.devDeviceId"] = generate_random_id()

# Write the modified data back to the JSON file
try:
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print("Successfully updated the telemetry data.")
except IOError as e:
    print(f"Error writing to the file: {e}")
