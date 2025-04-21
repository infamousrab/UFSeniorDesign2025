import bluetooth

ble = bluetooth.BLE()
ble.active(True)
mac_address = ble.config('mac')[1]
formatted_mac = ':'.join(f'{b:02x}' for b in mac_address)
print("Bluetooth address:", formatted_mac)