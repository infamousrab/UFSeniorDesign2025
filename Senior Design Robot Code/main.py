import time
from wifiService import start_wifi_server  # Starts camera/sensor server in background threads
import initinit

def main():
    initinit.init()
    start_wifi_server()
    try:
        while True:
            time.sleep(1)  # Keep main thread alive without busy-waiting
    except KeyboardInterrupt:
        print("[Main] Interrupted by user.")
    finally:
        print("[Main] Shutdown complete.")

if __name__ == "__main__":
    main()
