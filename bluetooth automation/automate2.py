import re

def extract_connection_times(log_file_path, device_name):
    connection_time = None
    disconnection_time = None

    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    for line in lines:
        if device_name in line:
            timestamp_match = re.match(r"(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})", line)
            if not timestamp_match:
                continue
            timestamp = timestamp_match.group(1)

            if connection_time is None:
                connection_time = timestamp  # First appearance as connection time

            if ("setConnectedState: connected 0" in line or 
                "DisconnectDevice" in line or 
                "prepareToDisconnectExternalDevice" in line):
                disconnection_time = timestamp  # Last known disconnect

    return connection_time, disconnection_time

# Example usage
log_file = "bt_logcat.txt"
device = "Airdopes 141 ANC"

connected, disconnected = extract_connection_times(log_file, device)

print("Device:", device)
print("Connection Time:", connected if connected else "Not found")
print("Disconnection Time:", disconnected if disconnected else "Not found")
