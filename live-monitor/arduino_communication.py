import serial
import time
import os, requests

arduino_port = "COM5"  # Update with your Arduino port
baud_rate = 9600
ph_live_file = "ph_log_live.txt"
temp_live_file = "temperature_log_live.txt"
ph_history_file = "ph_log.txt"
temp_history_file = "temperature_log.txt"
config_url = "https://www.dropbox.com/scl/fi/24fbs6keuq8n6p9td4zdy/config.txt?rlkey=5rehn90y4j80bd3or404o0ebd&st=4q7y918b&dl=1"
config_file_path = "config.txt"  # Local path to save the config file

# Download the configuration file and save it locally
try:
    response = requests.get(config_url)
    with open(config_file_path, "w") as file:
        file.write(response.text)
    print("Configuration file downloaded successfully.")
except requests.exceptions.RequestException as e:
    print(f"Error downloading configuration file: {e}")
    exit(1)

last_modified_time = os.path.getmtime(config_file_path)

def send_configuration_to_arduino(ser, config_data):
    try:
        ser.write(config_data.encode('utf-8'))
        print("Sent configuration to Arduino.")
        time.sleep(0.1)
    except Exception as e:
        print(f"Error sending configuration: {e}")

def log_sensor_data(ser):
    global last_modified_time  # Use the global last_modified_time variable

    try:
        with open(ph_history_file, "a") as ph_history, open(temp_history_file, "a") as temp_history:
            if ph_history.tell() == 0:
                ph_history.write("Timestamp, pH\n")
            if temp_history.tell() == 0:
                temp_history.write("Timestamp, Temperature (C), Temperature (F)\n")

            while True:
                # Check if the configuration file has been modified every 5 seconds
                time.sleep(5)
                current_modified_time = os.path.getmtime(config_file_path)
                if current_modified_time != last_modified_time:
                    last_modified_time = current_modified_time
                    print("Configuration file updated. Sending new configuration...")
                    # Read the updated config and send it to the Arduino
                    with open(config_file_path, "r") as config_file:
                        send_configuration_to_arduino(ser, config_file.read())

                if ser.in_waiting > 0:
                    line = ser.readline().decode("utf-8").strip()
                    print(line)

                    if "pH:" in line and "Temp:" in line:
                        parts = line.split("|")

                        if len(parts) == 2:
                            try:
                                ph_part = parts[0].split(":")[1].strip()
                                temp_parts = parts[1].split(",")
                                temp_c = temp_parts[0].split(":")[1].strip().replace("°C", "")
                                temp_f = temp_parts[1].strip().replace("°F", "")
                                
                                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                                with open(ph_live_file, "a") as ph_live, open(temp_live_file, "a") as temp_live:
                                    ph_live.write(f"{ph_part}\n")
                                    temp_live.write(f"{temp_c}, {temp_f}\n")

                                ph_history.write(f"{timestamp}, {ph_part}\n")
                                ph_history.flush()
                                temp_history.write(f"{timestamp}, {temp_c}, {temp_f}\n")
                                temp_history.flush()
                            except Exception as e:
                                print(f"Error parsing data: {line}. Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Stopped logging sensor data.")

if __name__ == "__main__":
    try:
        print("Connecting to Arduino...")
        ser = serial.Serial(arduino_port, baud_rate, timeout=3)  # Added timeout
        print(f"Connected to Arduino on {arduino_port}.")
        
        log_sensor_data(ser)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
        print("Disconnected from Arduino.")
