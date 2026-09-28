# 1. Listen to Arduino
# 2. Parse RUN,<revolution count>,<elapsed ms>
# 3. Calculate session values
# 4. Insert run session row into db

import os
import serial
from datetime import datetime, timedelta
from dotenv import load_dotenv
from db import get_wheel_circumference, insert_run_session

load_dotenv()

HAMSTER_ID = int(os.getenv("HAMSTER_ID"))
WHEEL_ID = int(os.getenv("WHEEL_ID"))

arduino = serial.Serial(
    "/dev/ttyACM0", # Linux device path for arduino
    9600,
    timeout=1
)

while True:
    line = arduino.readline().decode().strip()

    if not line:
        continue

    print(line)

    if line.startswith("RUN"):
        try:
            _, revolutions, elapsed_ms = line.split(",")
            
            revolutions = int(revolutions)
            elapsed_ms = int(elapsed_ms)
            elapsed_seconds = elapsed_ms / 1000
    
            ended_at = datetime.now()
            started_at = ended_at - timedelta(milliseconds=elapsed_ms)
    
            wheel_circumference_inches = get_wheel_circumference(WHEEL_ID)
            distance_inches = revolutions * wheel_circumference_inches
            distance_miles = distance_inches / 63360
    
    
            print("Completed session:")
            print(f"Revolutions: {revolutions}")
            print(f"Elapsed seconds: {elapsed_seconds}")
            print(f"Distance miles: {distance_miles:.4f}")
            print()
    
            insert_run_session(
                HAMSTER_ID,
                WHEEL_ID,
                started_at,
                ended_at,
                revolutions,
                distance_miles,
                elapsed_seconds
            )

        except Exception as e:
            print(f"Failed to process run '{line}': {e}")