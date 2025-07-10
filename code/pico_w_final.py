import network
import socket
from time import sleep
import machine
from machine import Pin, PWM

# Wi-Fi credentials
ssid = 'TP-Link_Guest_9C6E'
password = 'xxxx'

# Set up PWM on GPIO 16
pwm_pin = PWM(Pin(16))
pwm_pin.freq(1000)
pwm_pin.duty_u16(0)

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    addr = (ip, 80)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    return s

def webpage(duty_percent):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PWM Control July 2nd 20:57 version</title>
    </head>
    <body style="text-align:center; font-family:sans-serif;">
        <h2>GPIO 16 PWM Slider (with reload)</h2>
        <form action="/" method="GET">
            <input type="range" name="duty" min="0" max="100" value="{duty_percent}"
                   onchange="this.form.submit()">
            <output>{duty_percent}</output>%
        </form>
    </body>
    </html>
    """
    return html

def serve(connection):
    duty_percent = 0
    while True:
        client, addr = connection.accept()
        request = client.recv(1024)
        request = request.decode()

        if 'GET /?duty=' in request:
            try:
                duty_str = request.split('GET /?duty=')[1].split(' ')[0]
                duty_percent = int(duty_str)
                duty_percent = max(0, min(100, duty_percent))
                pwm_val = int(duty_percent * 65535 / 100)
                pwm_pin.duty_u16(pwm_val)
                print(f'Set PWM: {duty_percent}% ({pwm_val})')
            except:
                pass

        response = webpage(duty_percent)
        client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        client.send(response)
        client.close()

try:
    ip = connect()
    s = open_socket(ip)
    serve(s)
except KeyboardInterrupt:
    pwm_pin.deinit()
    machine.reset()
