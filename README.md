# 🗑️ Smart Waste Management System

![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Python](https://img.shields.io/badge/Backend-Flask-black?style=flat-square&logo=flask)
![ESP32](https://img.shields.io/badge/Hardware-ESP32-lightgrey?style=flat-square)
![Wokwi](https://img.shields.io/badge/Simulation-Wokwi-purple?style=flat-square)

## 📖 Project Overview
The **Smart Waste Management System** is an end-to-end IoT solution designed to monitor waste bin fill levels in real-time. By utilizing an ESP32 microcontroller equipped with an ultrasonic sensor, it measures trash levels and provides local visual/audio feedback. The hardware seamlessly communicates with a Flask backend and MongoDB database, pushing live data to a modern, interactive web dashboard that features optimized collection routing. 

---

## 🎯 Problem It Solves
Traditional waste collection relies on fixed routes and schedules, often resulting in:
- **Overflowing Bins:** Leading to unhygienic environments and public health hazards.
- **Wasted Resources:** Fuel and time are wasted driving to empty bins.
- **High Carbon Footprint:** Inefficient routing increases emissions.

**Our Solution:** Real-time monitoring allows for dynamic, priority-based route optimization, ensuring bins are collected *only* when necessary and in the most efficient order.

---

## 👥 Target Users
- **Smart City Administrators:** For city-wide sanitation planning.
- **University Campuses & Tech Parks:** To maintain clean facilities.
- **Waste Management Companies:** To optimize fleet operations and reduce fuel costs.
- **Hospitality & Mall Management:** For internal hygiene maintenance.

---

## 🛠️ Tech Stack

**Hardware & Simulation:**
- **Microcontroller:** ESP32
- **Sensors/Actuators:** HC-SR04 (Ultrasonic), SSD1306 (OLED Display), LEDs (RGB Status), Buzzer
- **Platform:** [Wokwi](https://wokwi.com/) / Arduino IDE (C++)

**Backend:**
- **Language/Framework:** Python 3, Flask, Flask-CORS
- **Database:** MongoDB

**Frontend:**
- **Technologies:** HTML5, Vanilla CSS3 (Modern Dark Theme), JavaScript (Vanilla)
- **Mapping:** Leaflet.js (CartoDB Dark Matter tiles)

---

## ✨ Key Features
- 📡 **Real-Time Monitoring:** Live calculation of bin fill levels based on distance.
- 🚨 **Local Alerts:** OLED display shows current status, LEDs indicate level (Green/Yellow/Red), and a buzzer sounds when the bin is critical (>80%).
- 🗺️ **Live Interactive Map:** A beautiful dark-themed map showing all deployed IoT bins.
- 🛣️ **Smart Route Optimization:** Nearest-neighbor TSP algorithm to generate collection routes prioritized by fill level (Red → Amber → Green).
- ⚡ **Simulation Mode:** One-click dashboard button to generate simulated IoT data for testing.
- 📱 **Responsive UI:** A modern, glass-morphic dashboard that works across devices.

---

## 📂 Project Structure

```text
├── CodeFiles/
│   ├── HackathonCodeFile/
│   │   ├── app.py                 # Flask Backend server
│   │   ├── index.html             # Main Dashboard UI
│   │   └── requirements.txt       # Python dependencies
│   └── SimulationCodeFile/
│       ├── diagram.json           # Wokwi circuit configuration
│       ├── libraries.txt          # Wokwi library dependencies
│       └── sketch.ino             # ESP32 C++ firmware
├── Photos/                        # Project screenshots and diagrams
└── README.md                      # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- [Python 3.8+](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/try/download/community) (Running locally on port 27017, or update the URI in `app.py` to use MongoDB Atlas)
- Wokwi Account (for simulation) or Arduino IDE (for physical hardware)

### 1. Backend Setup
Clone the repository and set up the Python environment:
```bash
# Navigate to the backend folder
cd CodeFiles/HackathonCodeFile

# (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```
*The server will start at `http://127.0.0.1:5000`.*

### 2. Frontend Setup
The frontend is a lightweight HTML file. You can simply open it in any modern browser:
```bash
# Double click the file or use a live server
open CodeFiles/HackathonCodeFile/index.html
```

### 3. Hardware Simulation (Wokwi)
1. Go to [Wokwi.com](https://wokwi.com/) and create a new ESP32 project.
2. Replace the contents of `diagram.json` and `sketch.ino` with the files provided in the `SimulationCodeFile/` directory.
3. Ensure the Wokwi libraries are set up based on `libraries.txt`.
4. Click the **Play** button to start the simulation. Adjust the distance on the Ultrasonic sensor to see the LEDs, OLED, and Buzzer react in real-time.

---

## 🔌 API Details

| Endpoint | Method | Description | Payload Example |
| :--- | :--- | :--- | :--- |
| `/data` | `POST` | Accepts live readings from IoT bins and saves to MongoDB. | `{"binId": "BIN-001", "level": 85, "location": "Main Hall"}` |
| `/data` | `GET` | Returns the latest aggregated status of all bins. | - |
| `/simulate`| `GET` | Generates random mock data for demonstration purposes. | - |
| `/clear` | `DELETE`| Wipes all records from the database (Dev use only). | - |

> **💡 Tip:** Use the *Simulate Bins* button on the dashboard UI to quickly populate the map and test the routing algorithm without physical hardware.

---

## 🖼️ Screenshots & Demo

- **Hardware Working:** `![Hardware Image 1](./Photos/Hardware/Pic1.jpeg)`
- **Hardware Working:** `![Hardware Image 2](./Photos/Hardware/Pic2.jpeg)`
- **Wokwi Simulation:** `![Wokwi Setup Architecture](./Photos/Simulation/Simulation1.png)`
- **Wokwi Simulation:** `![Green Stage](./Photos/Simulation/SimulationGreen.png)`
- **Wokwi Simulation:** `![Amber Stage](./Photos/Simulation/SimulationYellow.png)`
- **Wokwi Simulation:** `![Red Stage](./Photos/Simulation/SimulationRed.png)`
- **Software View:** `![Dashboard UI](./Photos/Software/SoftwareBins.png)`
- **Software View:** `![Map & Routing](./Photos/Software/SoftwarePath.png)`

---

## 🤝 Contributors
- **[Shreenidhi R]**
- **[Srisurya M]**
- **[Subhakshan K V]**
- **[Vikashini V]**
- **[Vishal K R]**
- **[Vishalakshi PL]**

---

## 📄 License
This project is licensed under the [MIT License](LICENSE). You are free to modify and distribute the code for personal or commercial use.
