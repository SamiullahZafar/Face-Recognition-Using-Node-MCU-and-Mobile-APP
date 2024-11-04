#include <ESP8266WiFi.h>
WiFiClient client;
WiFiServer server(80);

/* WiFi settings */
const char* ssid = "Hello World 3";   // WiFi SSID
const char* password = "paf444406";   // WiFi Password

/* Data received from the application */
String data = ""; 

/* Define motor control pins */
int Relay1 = 12;    // D6
int Relay2 = 16;    // D0
int Relay3 = 4;     // D2
int Relay4 = 5;     // D1

void setup() {
    /* Initialize motor control pins as output */
    pinMode(Relay1, OUTPUT);
    pinMode(Relay2, OUTPUT); 
    pinMode(Relay3, OUTPUT);  
    pinMode(Relay4, OUTPUT);

    digitalWrite(Relay1, LOW);
    digitalWrite(Relay2, LOW);
    digitalWrite(Relay3, LOW);
    digitalWrite(Relay4, LOW);
  
    /* Start server communication */
    Serial.begin(115200);
    connectWiFi();
    server.begin();
}

void loop() {
    /* If the server is available, run the "checkClient" function */  
    client = server.available();
    if (!client) return; 
    data = checkClient();
    Serial.print(data);

    /* Run function according to incoming data from application */
    if (data == "Relay1ON") { 
        digitalWrite(Relay1, HIGH);
    } else if (data == "Relay1OFF") {
        digitalWrite(Relay1, LOW);
    } else if (data == "Relay2ON") {
        digitalWrite(Relay2, HIGH);
    } else if (data == "Relay2OFF") {
        digitalWrite(Relay2, LOW);
    } else if (data == "Relay3ON") {
        digitalWrite(Relay3, HIGH);
    } else if (data == "Relay3OFF") {
        digitalWrite(Relay3, LOW);
    } else if (data == "RELAY4SUCCESS") {
        // Check for face recognition and control relay based on response
        int response = sendRequestToPythonServer();  // Send request to Python server
        if (response == 1) {
            digitalWrite(Relay4, HIGH);  // Turn on Relay 4 if face is recognized
            Serial.println("Face recognized, Relay 4 ON");
            delay(5000); // Adjust delay as needed
            digitalWrite(Relay4, LOW);  // Turn off Relay 4 after delay
            Serial.println("Relay 4 OFF");
        } else {
            Serial.println("Error or face not recognized.");
        }
    }
} 

void connectWiFi() {
    Serial.println("Connecting to WIFI");
    WiFi.begin(ssid, password);
    while (!(WiFi.status() == WL_CONNECTED)) {
        delay(300);
        Serial.print("..");
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("NodeMCU Local IP is: ");
    Serial.print((WiFi.localIP()));
}

/* Receive data from the app */
String checkClient(void) {
    while (!client.available()) delay(1); 
    String request = client.readStringUntil('\r');
    request.remove(0, 5);
    request.remove(request.length() - 9, 9);
    return request;
}

/* Send request to Python server for face recognition */
int sendRequestToPythonServer() {
    if (client.connect("192.168.173.48", 5000)) {  // Change to your Python server IP and port
        String url = "/trigger";  // Request URL for face recognition
        client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                     "Host: 192.168.173.48\r\n" +  // Python server IP
                     "Connection: close\r\n\r\n");
        
        delay(500);  // Wait for the response
        String response = client.readString();
        client.stop();
        
        // Check for HTTP response and parse it
        if (response.indexOf("200 OK") != -1) {
            // Parse the body of the response for "1" or "0"
            int startIndex = response.indexOf("\r\n\r\n") + 4;  // Move past the headers
            String body = response.substring(startIndex);
            Serial.println("Response from server: " + body);  // Print server response for debugging
            if (body.indexOf("1") != -1) {
                return 1;  // Face recognized
            } else {
                return 0;  // Face not recognized
            }
        } else {
            Serial.println("Error: Unexpected response from server");
            return -1;  // Indicate an error occurred
        }
    } else {
        Serial.println("Connection to Python server failed");
        return -1;  // Connection error
    }
} 
