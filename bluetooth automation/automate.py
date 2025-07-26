import os
import time
import subprocess
import signal

print("=== BLUETOOTH CONNECTION TEST SCRIPT ===\n")

# 1. Get Android version
print("[INFO] Getting Android version...")
android_version = subprocess.getoutput("adb shell getprop ro.build.version.sdk")
print(android_version)

# 2. Get Bluetooth version (improved method)
print("\n[INFO] Getting Bluetooth version info...")
bluetooth_info = subprocess.getoutput("adb shell dumpsys bluetooth_manager")
if "Address" in bluetooth_info:
    lines = bluetooth_info.splitlines()
    for line in lines:
        if "Address" in line:
            print("→", line.strip())
else:
    print("⚠️  Could not find Bluetooth address info.")

# 3. Clear previous logs
print("\n[INFO] Clearing previous logs...")
os.system("adb logcat -c")

# 4. Start capturing logs using subprocess
print("[INFO] Capturing logs for 30 seconds...")
log_file = open("bt_logcat.txt", "w", encoding="utf-8")
proc = subprocess.Popen(["adb", "logcat", "-v", "time"], stdout=log_file, stderr=subprocess.STDOUT)

# Wait 30 seconds while logs are captured
time.sleep(30)

# Stop logging
proc.terminate()
proc.wait()
log_file.close()

print("[INFO] Logs saved to bt_logcat.txt")

# 5. Analyze logs
print("\n[INFO] Analyzing logs for Bluetooth connection...")

with open("bt_logcat.txt", "r", encoding="utf-8", errors="ignore") as f:
    log_data = f.read()

start_keywords = ["BluetoothAdapter: startDiscovery", "Starting connection"]
end_keywords = ["onConnectionStateChanged", "Stopping discovery", "Bluetooth connection state changed"]

start_found = any(keyword in log_data for keyword in start_keywords)
end_found = any(keyword in log_data for keyword in end_keywords)

if start_found and end_found:
    print("✅ Found Bluetooth connection start and end logs.")
else:
    print("⚠️ Could not find both start and complete log entries.")
    print("Tip: Try manually toggling Bluetooth ON/OFF during the 30-second window.")

print("\n=== DONE ===")
