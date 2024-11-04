import cv2
import face_recognition
import pickle
import imutils
from imutils.video import VideoStream, FPS
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Initialize 'currentname' to track the last recognized person
currentname = "dataset"
encodingsP = "encodings.pickle"
latest_result = 0  # Global variable to hold the latest recognition result (1 for recognized, 0 otherwise)

# Load the known faces and embeddings
print("[INFO] loading encodings + face detector...")
with open(encodingsP, "rb") as f:
    data = pickle.load(f)

def face_recognition_generator():
    """Generator function for continuous face recognition."""
    global currentname, latest_result
    
    vs = VideoStream(src=0).start()
    time.sleep(2.0)  # Allow the camera to warm up
    fps = FPS().start()

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)

        boxes = face_recognition.face_locations(frame)
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []
        recognized = 0  # Default to 0 (not recognized)

        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"

            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                name = max(counts, key=counts.get)

                if currentname != name:
                    currentname = name
                    print(f"Recognized: {currentname}")

                recognized = 1  # Set recognized to 1 if a known face is matched

            names.append(name)

        # Update the global variable with the latest recognition result
        latest_result = recognized

        # Display the results on the frame
        for ((top, right, bottom, left), name) in zip(boxes, names):
            color = (255, 255, 255) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 1)
            y = top - 10 if top - 10 > 10 else top + 10
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        cv2.imshow("Facial Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        fps.update()

    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    vs.stop()

# HTTP server to handle recognition requests
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/trigger':
            print("Trigger received. Sending the latest recognition result...")
            
            # Send the latest recognition result back to the Arduino
            result_string = str(latest_result)  # "1" if recognized, "0" otherwise
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(result_string.encode())
            print(f"Sent recognition result: {result_string}")

# Run the generator in a separate thread
def start_face_recognition_thread():
    face_gen = face_recognition_generator()
    for _ in face_gen:
        pass

if __name__ == "__main__":
    # Start the face recognition in a background thread
    threading.Thread(target=start_face_recognition_thread, daemon=True).start()
    
    # Start the HTTP server
    server_address = ('192.168.173.48', 5000)  # Use your IP and port
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("HTTP server running...")
    httpd.serve_forever()
