import json
import uuid
import pyfiglet
from colorama import Fore, Style, init
import os

# Initialize colorama
init(autoreset=True)

def cursor_or_windsurf():
    # Fetch the current user's home directory
    user_home = os.path.expanduser("~")

    # Dynamically construct the paths for Cursor and Windsurf
    cursor = os.path.join(user_home, r'AppData\Roaming\Cursor\User\globalStorage\storage.json')
    windsurf = os.path.join(user_home, r'AppData\Roaming\Windsurf\User\globalStorage\storage.json')

    try:
        print(Fore.CYAN + "Select an AI option:")
        ide = int(input(Fore.YELLOW + '1. Cursor AI\n2. Windsurf AI\nInput: >> '))

        # Function to generate random UUID-like strings
        def generate_random_id():
            return str(uuid.uuid4()).replace('-', '')
        
        if ide == 1:
            # Generate ASCII art for the text "CURSOR AI"
            ai_art = pyfiglet.figlet_format("CURSOR AI")
            print(Fore.GREEN + ai_art)
           
            # Read the existing JSON data
            try:
                with open(cursor, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
            except FileNotFoundError:
                print(Fore.RED + f"Error: The file {cursor} was not found.")
                exit(1)
                
            except json.JSONDecodeError:
                print(Fore.RED + "Error: Failed to decode JSON data from the file.")
                exit(1)

            # Update telemetry values with random UUID-based values
            data["telemetry.macMachineId"] = generate_random_id()
            data["telemetry.sqmId"] = "{" + generate_random_id() + "}"
            data["telemetry.machineId"] = generate_random_id()
            data["telemetry.devDeviceId"] = generate_random_id()
            
            # Write modified data back to the JSON file
            try:
                with open(cursor, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
                    
                print(Fore.GREEN + f"Successfully updated the telemetry data for Cursor AI!")
                
            except IOError as e:
                print(Fore.RED + f"Error writing to the file: {e}")
                    
        elif ide == 2:
            # Generate ASCII art for the text "WINDSURF AI"
            ai_art = pyfiglet.figlet_format("WINDSURF AI")
            print(Fore.BLUE + ai_art)
            
            # Read the existing JSON data
            try:
                with open(windsurf, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
            except FileNotFoundError:
                print(Fore.RED + f"Error: The file {windsurf} was not found.")
                exit(1)
                
            except json.JSONDecodeError:
                print(Fore.RED + "Error: Failed to decode JSON data from the file.")
                exit(1)
            
            # Update telemetry values with random UUID-based values
            data["telemetry.machineId"] = generate_random_id()
            data["telemetry.sqmId"] = "{" + generate_random_id() + "}"
            data["telemetry.devDeviceId"] = generate_random_id()
            
            # Write modified data back to the JSON file
            try:
                with open(windsurf, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
                    
                print(Fore.GREEN + f"Successfully updated the telemetry data for Windsurf AI!")
                
            except IOError as e:
                print(Fore.RED + f"Error writing to the file: {e}")
        else:
            print(Fore.LIGHTRED_EX + 'Invalid input. Please enter 1 or 2.')
            cursor_or_windsurf()
            
    except KeyboardInterrupt:
        print(Fore.RED + '\nExiting...\nExited!!!')
        exit(0)
        
    except ValueError:
        print(Fore.LIGHTRED_EX + 'Only integers are supported! Try again.')
        cursor_or_windsurf()
          
def main():
    print(Fore.MAGENTA + '=' * 66)
    print(Fore.CYAN + pyfiglet.figlet_format('Knowledge is POWER'))
    print(Fore.GREEN + '\t\t\t\tFilippo De Silva Jan 1 2025')
    print(Fore.MAGENTA + '=' * 66 + '\n\n\n')
    
    cursor_or_windsurf()

main()
