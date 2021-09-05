import network

ap = network.WLAN(network.AP_IF) 
ap.config(essid='MomoNoWake') 
ap.config(max_clients=10) 
ap.active(True)         

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('essid', 'password')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


with open('boot.py') as f:
    print(f.read())