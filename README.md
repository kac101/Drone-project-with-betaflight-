
<h1 align="center">Cleaning Drone Raspberry Pi Pico 2W - Wireless Motor Control</h1>

<p>
Project Team:
<ul style="list-style-position: inside;">
  <li>Donggeon Kim</li>
</ul>
</p>

---

## Project Summary

This project's goal is to build a drone with custom PCB that works both for flight controller and ESC. For now, this work demonstrates wireless control of a motor (LED for now) using a Raspberry Pi Pico 2W  MicroPython, and `ngrok` for remote access (for additional motor for cleaning brush). A web-based interface with a PWM slider adjusts motor speed in real time over Wi-Fi. The backend is hosted on the Pico 2W and made publicly accessible using `ngrok`, eliminating the need for manual router configuration.

## Development Milestones

### Milestone 1  Wireless Control Setup
### Milestone 2  PCB Planning & Betaflight Familiarization
---
##  Milestones 1
**How It Works:**
- A MicroPython script serves an HTML page with a PWM slider.
- User input (0–100) sets the PWM duty cycle for motor control.
- Communication is handled over Wi-Fi; `ngrok` exposes the server via a public HTTPS link.
- A PWM will be generated to control rpm of motor based on PWM control input from website.


<p align="center">
  <img src="Picture1.png" alt="Wi-Fi Router Setup" width="500"/>
</p>
<p align="center" style="font-size:11px;">
Figure 1. Wi-Fi Router Configuration for 2.4GHz and checking option for allowing device-to-device communication
</p>

## System Architecture

1. **Power**  
   - USB supplies power to the Pico 2W  
   - External source powers motor through MOSFET //later

2. **Control**  
   - PWM output from GPIO (e.g., GP16)  
   - MOSFET controls motor RPM (For now, just LED is used to indicate it is sending PWM)  
   - Web server on Pi Pico 2W  
   - Public access via `ngrok`  

   >  **Why ngrok?**  
   If you can’t modify your Wi-Fi router settings to allow local device-to-device communication (e.g., university or guest networks), you can expose your Raspberry Pi Pico W web server to the public internet using **ngrok**.  
   This provides a **free public URL that lasts 4 hours per session**.

   >  **Get your auth token here:**  
   [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)

   The following commands were used in **Ubuntu** to install and configure `ngrok`:

   ```bash
   sudo snap install ngrok
   ngrok config add-authtoken xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ngrok http xxx.xxx.x.xxx:xx


3. **Interface**  
   - HTML slider updates PWM duty via GET requests  
   - URL format: `https://<random-id>.ngrok-free.app/?duty=75`  
   - Slider input controls motor in near real-time


### Milestone 1  details
- Set up Pico 2W with MicroPython
-  Download Thonny IDE from https://github.com/thonny/thonny/releases/tag/v4.1.7
-  Download MicroPython UF2 file for pico 2w board
  --  https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython 
- Verified PWM output to motor  
<p align="center">
  <img src="Picture2.png" alt="Thonny IDE Setup" width="500"/>
</p>
<p align="center" style="font-size:11px;">
Figure 2. Thonny IDE with MicroPython script loaded for Pico 2W
</p>

- HTML interface created using `<input type="range">`  
- Integrated with MicroPython server
  
- `ngrok` tunnel configured to allow external access  
- Tested mobile and cross-device compatibility  


## Hardware Details


- **LED Control Pin**: GP16  



### Component List

- 1x Raspberry Pi Pico 2 W    
- 1x LED 
- 1x USB Cable - Micro


## Software Details

- **Language & SDK**: MicroPython using Thonny IDE  
- **Web Interface**: HTML slider served from the Pico 2W
  <p align="center">
  <img src="Picture3.png" alt="Web Page Outcome" width="500"/>
</p>
<p align="center" style="font-size:11px;">
Figure 3. Web interface with slider to control motor/LED
</p>

- **Back-end Logic**: Parses `?duty=value` from HTTP GET request  
- **PWM Setup**: 1 kHz frequency, 0–100% duty cycle  
- **ngrok**: Tunnels HTTP port (default 80) to a random public URL  
  - Example: `https://abcd-1234-5678.ngrok-free.app/?duty=60`  

<p align="center">
  <img src="Picture4.png" alt="ngrok Tunnel" width="500"/>
</p>
<p align="center" style="font-size:11px;">
Figure 4. ngrok tunnel running and exposing Pico 2W web server
</p>


## Notes

- The `ngrok` URL changes every session unless upgraded to Pro.
- Avoid sharing real IP addresses  for security.

---

### Milestone 2  
- Listing components PCB
- getting used to betaflight by playing with Bliz e-55 + ESC stack
---
