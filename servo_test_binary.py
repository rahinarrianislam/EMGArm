import time
import serial
from pylsl import resolve_streams, StreamInlet


# ----------------------------
# Arduino configuration
# ----------------------------

ARDUINO_PORT = "COM6"     # CHANGE THIS
BAUD_RATE = 115200

arduino = serial.Serial(
    ARDUINO_PORT,
    BAUD_RATE,
    timeout=1
)

# Give Arduino time to reset after opening serial connection
time.sleep(2)


# ----------------------------
# OpenBCI LSL
# ----------------------------

print("Looking for LSL streams...")

streams = resolve_streams()

for i, s in enumerate(streams):
    print(
        i,
        s.name(),
        s.type(),
        s.channel_count()
    )

inlet = StreamInlet(streams[0])

print("Connected to OpenBCI LSL stream")


# ----------------------------
# EMG configuration
# ----------------------------

EMG_CHANNEL = 0

# CHANGE THIS after looking at your actual EMG values
THRESHOLD = 0.7

servo_active = False


# ----------------------------
# Main loop
# ----------------------------

while True:

    sample, timestamp = inlet.pull_sample()

    emg = sample[EMG_CHANNEL]

    print(f"EMG: {emg:.4f}")

    # Muscle contracted
    if emg > THRESHOLD and not servo_active:

        print("MUSCLE ACTIVE -> Servo ON")

        arduino.write(b'1')

        servo_active = True


    # Muscle relaxed
    elif emg <= THRESHOLD and servo_active:

        print("Muscle relaxed -> Servo OFF")

        arduino.write(b'0')

        servo_active = False