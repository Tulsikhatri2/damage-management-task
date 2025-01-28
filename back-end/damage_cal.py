import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
import os

def calculate_damage_percentage(fresh_image_path, damaged_image_path):
    # Load images
    fresh_image = cv2.imread('images/cardamage.jpg')

    damaged_image = cv2.imread('images/carfresh.jpg')

    # Check if images are loaded correctly
    if fresh_image is None:
        raise FileNotFoundError(f"Could not load image: {fresh_image_path}")
    if damaged_image is None:
        raise FileNotFoundError(f"Could not load image: {damaged_image_path}")

    # Resize images to the same dimensions (optional, for consistent comparison)
    damaged_image = cv2.resize(damaged_image, (fresh_image.shape[1], fresh_image.shape[0]))

    # Convert images to grayscale
    gray_fresh = cv2.cvtColor(fresh_image, cv2.COLOR_BGR2GRAY)
    gray_damaged = cv2.cvtColor(damaged_image, cv2.COLOR_BGR2GRAY)

    # Compute structural similarity index (SSIM)
    similarity, diff = compare_ssim(gray_fresh, gray_damaged, full=True)
    diff = (diff * 255).astype("uint8")

    # Threshold the difference
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Calculate contours of the differences
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the area of differences
    total_area = gray_fresh.shape[0] * gray_fresh.shape[1]
    damage_area = sum(cv2.contourArea(contour) for contour in contours)

    # Calculate damage percentage
    damage_percentage = (damage_area / total_area) * 100

    # Draw contours on the images for visualization
    fresh_with_contours = fresh_image.copy()
    damaged_with_contours = damaged_image.copy()

    for contour in contours:
        if cv2.contourArea(contour) > 5:  # Ignore very small differences
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(fresh_with_contours, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(damaged_with_contours, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Save result images
    cv2.imwrite("fresh_with_contours.jpg", fresh_with_contours)
    cv2.imwrite("damaged_with_contours.jpg", damaged_with_contours)

    return similarity, damage_percentage, "fresh_with_contours.jpg", "damaged_with_contours.jpg"

if __name__ == "__main__":
    # Paths to input images
    fresh_image_path = "images/fresh_car.jpg"  # Update with your fresh car image path
    damaged_image_path = "images/damaged_car.jpg"  # Update with your damaged car image path

    try:
        # Calculate damage percentage
        similarity, damage_percentage, fresh_result, damaged_result = calculate_damage_percentage(fresh_image_path, damaged_image_path)

        print(f"Similarity: {similarity:.2f}")
        print(f"Damage Percentage: {damage_percentage:.2f}%")
        print(f"Result images saved as: {fresh_result}, {damaged_result}")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
