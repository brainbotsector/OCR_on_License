import os
import cv2
import easyocr

def process_images(input_folder, output_folder):
    # Create EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each image file in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Read the image
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            # Use EasyOCR to detect text
            result = reader.readtext(image)

            # Draw bounding boxes and write recognized text
            for detection in result:
                top_left = tuple(map(int, detection[0][0]))
                bottom_right = tuple(map(int, detection[0][2]))
                text = detection[1]
                confidence = round(detection[2], 2)

                # Draw red bounding box
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)

                # Write recognized text with confidence
                font_scale = 0.4  # Adjust font size
                font_thickness = 1  # Adjust font thickness
                (text_width, text_height), _ = cv2.getTextSize(f'{text} ({confidence})', cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
                cv2.rectangle(image, (top_left[0], top_left[1] - text_height - 5), (top_left[0] + text_width + 2, top_left[1]), (255, 255, 255), -1)  # Add white background box
                cv2.putText(image, f'{text} ({confidence})', (top_left[0], top_left[1] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 128, 0), font_thickness)  # Dark green color

            # Save the modified image to the output folder
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)
            print(f"Processed {filename} and saved to {output_path}")

# Specify input and output folders
input_folder = "Original Images"
output_folder = "After OCR Images"

# Process images
process_images(input_folder, output_folder)
