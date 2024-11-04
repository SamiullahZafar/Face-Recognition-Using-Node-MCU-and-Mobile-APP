Face Recognition with HTTP Server Trigger

This project is a Pythonbased facial recognition system using OpenCV and `face_recognition` libraries. It continuously recognizes faces using a webcam feed and provides a recognition status (recognized or not recognized) through an HTTP server that responds to GET requests from external devices, such as an Arduino.

Features

 RealTime Face Recognition: Uses a webcam to recognize faces continuously.
 HTTP Trigger Response: Responds with the recognition status (1 for recognized, 0 for not recognized) when it receives a GET request.
 Easy Integration with Arduino: Allows simple integration with an Arduino or similar microcontroller to perform actions based on the recognition status.

Requirements

 Python 3.6+
 Libraries:
   `face_recognition`
   `imutils`
   `opencvpython`
   `pickle`

Installation

1. Clone the Repository:
   bash
   git clone https://github.com/YourUsername/YourRepositoryName.git
   cd YourRepositoryName
   

2. Install Dependencies:
   Make sure to install the necessary Python libraries:
   bash
   pip install face_recognition imutils opencvpython
   

3. Prepare Face Encodings:
   This project uses a file named `encodings.pickle` to store known face encodings and their labels. You can create this file by following steps to encode faces, or use a preexisting one.

4. Update IP Address:
   In the code, update the IP address in the line below to match your servers IP:
   python
   server_address = (192.168.173.48, 5000)
   

Usage

1. Run the Face Recognition and HTTP Server:
   Start the script with:
   bash
   python main.py
   

   This will launch the webcam and start the HTTP server on the specified IP and port.

2. Send a Trigger Request:
   To get the recognition status, make a GET request to:
  
   http://192.168.173.48:5000/trigger
   The server will respond with:
    1 if a recognized face is detected.
    0 if no recognized face is detected.

Project Structure

 `main.py`: Main script to run face recognition and HTTP server.
 `encodings.pickle`: File containing the face encodings for known faces.

Example Usage with Arduino

If you have an Arduino or similar device connected to the same network, you can send GET requests to check for face recognition results and trigger actions based on the responses.

Acknowledgements

 [Face Recognition Library](https://github.com/ageitgey/face_recognition)
 [OpenCV](https://opencv.org/)

License

This project is licensed under the MIT License. See `LICENSE` for details.

