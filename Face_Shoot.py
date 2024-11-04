import cv2
import os

def capture_images(person_name, dataset_path, num_images=10):
    # Create a directory for the person if it doesn't exist
    person_dir = os.path.join(dataset_path, person_name)
    os.makedirs(person_dir, exist_ok=True)

    # Start video capture
    video_capture = cv2.VideoCapture(0)  # 0 for the default camera
    count = 0

    print(f"Capturing images for {person_name}. Press 'Space' to capture an image.")

    while count < num_images:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to grab frame.")
            break

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Wait for key press
        key = cv2.waitKey(1)

        # Capture image when spacebar is pressed
        if key == ord(' '):  # Spacebar
            image_path = os.path.join(person_dir, f"{person_name}_{count + 1}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Captured {image_path}")
            count += 1

    # Release the camera and close windows
    video_capture.release()
    cv2.destroyAllWindows()
    print("Image capture completed.")

# Example usage
dataset_path = 'dataset'  
person_name = input("Enter the name of the person: ")
capture_images(person_name, dataset_path)
