import pandas as pd
from datetime import datetime
import os
from config import (
    DEFAULT_GREEN_DURATION_S, 
    THRESHOLD_LOW_CROWD_X, 
    THRESHOLD_HIGH_CROWD_Y, 
    DURATION_INCREMENT_S, 
    DURATION_DECREMENT_S,
    LOG_FILE
)

# Global tracker for status logging (best practice for simple state management)
# Note: Python modules are initialized once, so this variable persists across calls.
previous_crowd_status = "" 

def evaluate_crowd_status(person_count: int) -> tuple[str, int, tuple]:
    """
    Determines the crowd status, calculates the next green light duration, 
    and sets the corresponding display color based on defined thresholds.

    Args:
        person_count: The total number of people detected in the frame.

    Returns:
        A tuple: (status_string, green_duration, status_color)
    """
    
    # Use constants to evaluate the crowd density
    if person_count > THRESHOLD_HIGH_CROWD_Y:
        # High Density Scenario
        crowd_status = "HIGH DENSITY"
        green_duration = DEFAULT_GREEN_DURATION_S + DURATION_INCREMENT_S
        status_color = (0, 0, 255)  # RED for high alert
        
    elif person_count <= THRESHOLD_LOW_CROWD_X:
        # Low Density Scenario
        crowd_status = "LOW DENSITY"
        green_duration = DEFAULT_GREEN_DURATION_S - DURATION_DECREMENT_S
        status_color = (255, 255, 0) # CYAN/YELLOW for low density
        
    else:
        # Default Density Scenario
        crowd_status = "DEFAULT DENSITY"
        green_duration = DEFAULT_GREEN_DURATION_S
        status_color = (0, 255, 0)  # GREEN for normal operation
        
    log_status_change(person_count, crowd_status, green_duration)
    
    return crowd_status, green_duration, status_color


def log_status_change(person_count: int, current_status: str, green_duration: int):
    """
    Logs the status change to a CSV file only if the status has actually transitioned.
    """
    global previous_crowd_status # Access the global state tracker
    
    if current_status != previous_crowd_status:
        
        # 1. Prepare the log entry using a dictionary for clarity
        log_data = {
            'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'crowd_count': [person_count],
            'status_from': [previous_crowd_status if previous_crowd_status else "START"],
            'status_to': [current_status],
            'green_duration_s': [green_duration]
        }
        
        # 2. Convert to DataFrame
        log_df = pd.DataFrame(log_data)
        
        # 3. Append to CSV file (creates file if it doesn't exist)
        log_df.to_csv(
            LOG_FILE, 
            mode='a', # 'a' for append is crucial for logging!
            header=(not os.path.exists(LOG_FILE)), # Write header only if file is new
            index=False 
        )
        
        print(f"🚨 LOGGED: Status switched from '{previous_crowd_status if previous_crowd_status else 'START'}' to '{current_status}' (Count: {person_count})")
        
        # 4. Update the tracker for the next frame
        previous_crowd_status = current_status