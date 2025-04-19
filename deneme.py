from orbit_controller import Controller
import time
orbit = Controller("192.168.31.57", 9090)
orbit.connect()
orbit.move_forward(0.0)
print("Moving forward")
# while True:
print(orbit.get_temperature())
time.sleep(0.2)

# orbit.terminate()