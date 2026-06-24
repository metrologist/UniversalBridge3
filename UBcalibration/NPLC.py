import pyvisa
import time

# Initialize the VISA resource manager
rm = pyvisa.ResourceManager()

# Open connection to your 3458A (adjust GPIB address as necessary)
gpib_address = 'GPIB0::23::INSTR'
try:
    dmm = rm.open_resource(gpib_address)
except Exception as e:
    print(f"Error connecting to the DMM at {gpib_address}: {e}")
    exit()

# Configure communication timeouts and termination characters
dmm.timeout = 15000  # 15 seconds (large NPLC values can cause longer command processing times)
dmm.read_termination = '\r\n'
dmm.write_termination = '\r\n'

try:
    print("--- Keysight 3458A NPLC Configuration Utility ---")

    # 1. Query and display the current NPLC setting before making changes
    initial_nplc = dmm.query("NPLC?")
    print(f"Current NPLC setting on the DMM is: {initial_nplc.strip()}")

    # 2. Prompt the user for a new NPLC figure
    user_input = input("Enter the new NPLC value you want to set (e.g., 1, 10, 100): ").strip()

    # Validate that the user actually entered a number
    try:
        nplc_value = float(user_input)
    except ValueError:
        print("Error: Invalid input. Please enter a valid numerical figure.")
        exit()

    # 3. Apply the new NPLC setting
    print(f"Sending command: NPLC {nplc_value} ...")
    dmm.write(f"NPLC {nplc_value}")

    # Small pause to allow the hardware to update its internal registers
    time.sleep(0.2)

    # 4. Query the DMM again to verify the setting was successfully accepted
    verified_nplc = dmm.query("NPLC?")
    print("\n--- Verification ---")
    print(f"The DMM actively reports its NPLC setting is now: {verified_nplc.strip()}")

    if float(verified_nplc) == nplc_value:
        print("Success! The setting has been verified on the instrument.")
        print("Note: This setting will remain active until the DMM is power-cycled or RESET.")
    else:
        print("Warning: The verified NPLC value does not match what you entered.")

except Exception as e:
    print(f"An error occurred during communication: {e}")

finally:
    # Always close the visa resource connection cleanly
    dmm.close()
    print("Connection closed.")

import pyvisa
import time

# Initialize the VISA resource manager
rm = pyvisa.ResourceManager()

# Open connection to your 3458A (replace 'GPIB0::22::INSTR' with your actual GPIB address)
dmm = rm.open_resource('GPIB0::22::INSTR')

# Configure basic timeout and termination characters
dmm.timeout = 10000  # 10 seconds timeout for high NPLC settings
dmm.read_termination = '\r\n'
dmm.write_termination = '\r\n'

try:
    # 1. Clear the instrument to a known state (Optional, but recommended)
    dmm.write("RESET")
    time.sleep(0.5)

    # 2. Set the NPLC value (e.g., 100 for maximum power line noise rejection)
    nplc_value = 100
    dmm.write(f"NPLC {nplc_value}")
    print(f"Successfully sent: NPLC {nplc_value}")

    # 3. Verify the setting by querying it back
    current_nplc = dmm.query("NPLC?")
    print(f"Verified current DMM NPLC setting: {current_nplc.strip()}")

finally:
    # Clean up and close the resource connection
    dmm.close()

# Tell the DMM to automatically execute state 1 whenever it boots up
dmm.write("PST 1")

# Tell the DMM to automatically execute state 1 whenever it boots up
dmm.write("PST 1")

# Save the current configuration (including your NPLC setting) to state slot 1
dmm.write("SSTATE 1")


