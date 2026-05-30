import os
import json
import time
import random
import datetime
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing command: {cmd}\nStdout: {result.stdout}\nStderr: {result.stderr}")
    return result.returncode == 0

def update_pulse():
    pulse_path = "pulse.json"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    pulse_data = {
        "status": "online",
        "last_pulse": current_time,
        "type": "automated-ci-ping"
    }
    
    with open(pulse_path, "w", encoding="utf-8") as f:
        json.dump(pulse_data, f, indent=2)
        
    print(f"Pulse index updated successfully at {current_time}.")
    return True

def git_push():
    if not run_cmd("git add pulse.json"):
        return False
    if not run_cmd('git commit -m "chore: automated continuous integration build pulse"'):
        print("Nothing to commit or commit failed.")
    if not run_cmd("git push origin main"):
        return False
    print("Successfully pushed website build pulse to GitHub!")
    return True

if __name__ == "__main__":
    # Delay randomly between 0 and 90 minutes (0 to 5400 seconds) for human-like organic timing
    delay_seconds = random.randint(0, 5400)
    print(f"Applying organic delay: Sleeping for {delay_seconds} seconds (~{delay_seconds // 60} minutes)...")
    time.sleep(delay_seconds)
    
    if update_pulse():
        git_push()
