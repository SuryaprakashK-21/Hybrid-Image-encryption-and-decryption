import cv2
import numpy as np

# Function to calculate NPCR
def calculate_npcr(original_image, encrypted_image):
    # Ensure both images have the same dimensions
    if original_image.shape != encrypted_image.shape:
        raise ValueError("Original and encrypted images must have the same dimensions.")
    
    # Compute NPCR
    diff = (original_image != encrypted_image).astype(np.uint8)
    npcr = np.sum(diff) / diff.size * 100  # Percentage of differing pixels
    return npcr

# Function to calculate UACI
def calculate_uaci(original_image, encrypted_image):
    # Ensure both images have the same dimensions
    if original_image.shape != encrypted_image.shape:
        raise ValueError("Original and encrypted images must have the same dimensions.")
    
    # Compute UACI
    diff = np.abs(original_image.astype(np.int16) - encrypted_image.astype(np.int16))
    uaci = np.mean(diff / 255.0) * 100  # Average of the intensity differences scaled to percentage
    return uaci

# Main function to process multiple images
if __name__ == "__main__":
    # List of image names
    image_names = [
        "baboon.jpg", "black.jpg", "brain.jpg", "cameraman.jpg",
        "grey.jpg", "lena.jpg", "peppers.jpg", "ribs.jpg"
    ]

    # Iterate through each image
    for image_name in image_names:
        # Generate the encrypted image filename
        encrypted_image_name = f"encrypted_{image_name}"

        # Load original and encrypted images as grayscale
        original_image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
        encrypted_image = cv2.imread(encrypted_image_name, cv2.IMREAD_GRAYSCALE)

        # Check if both images exist
        if original_image is None:
            print(f"Error: Original image {image_name} not found.")
            continue
        if encrypted_image is None:
            print(f"Error: Encrypted image {encrypted_image_name} not found.")
            continue

        # Calculate NPCR and UACI
        try:
            npcr = calculate_npcr(original_image, encrypted_image)
            uaci = calculate_uaci(original_image, encrypted_image)
            # Display the results
            print(f"Results for {image_name}:")
            print(f"  NPCR: {npcr:.2f}%")
            print(f"  UACI: {uaci:.2f}%")
        except ValueError as e:
            print(f"Error processing {image_name}: {e}")
