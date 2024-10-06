import os
import sys
from repo import ClassifierRepo
from services import PredictDigitService
from settings import CLASSIFIER_STORAGE

def predict_digit_from_image(image_path):
    # Load the repository and prediction service
    repo = ClassifierRepo(CLASSIFIER_STORAGE)
    service = PredictDigitService(repo)

    # Call the prediction service with the image file path
    prediction = service.handle(image_path)

    return prediction

def process_images_in_folder(folder_path):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Construct the full path to the image file
        file_path = os.path.join(folder_path, filename)

        # Check if it's an image file
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            print(f"Processing image: {filename}")

            # Predict the digit from the image
            predicted_digit = predict_digit_from_image(file_path)

            # Output the predicted digit
            print(f"The predicted digit for {filename} is: {predicted_digit}")
        else:
            print(f"Skipping non-image file: {filename}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python new_run.py <folder_path>")
    else:
        # Get folder path from the command line argument
        folder_path = sys.argv[1]

        # Check if the provided folder exists
        if not os.path.isdir(folder_path):
            print(f"Error: {folder_path} is not a valid directory.")
        else:
            # Process all images in the folder
            process_images_in_folder(folder_path)
