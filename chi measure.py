import cv2
import numpy as np
from scipy.stats import chisquare
from math import log2

# Function to calculate local Shannon entropy
def calculate_entropy(image):
    _, counts = np.unique(image, return_counts=True)
    probabilities = counts / counts.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

# Function to calculate correlation coefficients
def calculate_correlation(image):
    rows, cols = image.shape

    # Horizontal correlation
    horizontal_corr = np.corrcoef(image[:, :-1].flatten(), image[:, 1:].flatten())[0, 1]

    # Vertical correlation
    vertical_corr = np.corrcoef(image[:-1, :].flatten(), image[1:, :].flatten())[0, 1]

    # Diagonal correlation
    diagonal_corr = np.corrcoef(image[:-1, :-1].flatten(), image[1:, 1:].flatten())[0, 1]

    # Handle cases where correlation computation results in NaN or invalid values
    if np.isnan(horizontal_corr) or np.isnan(vertical_corr) or np.isnan(diagonal_corr):
        horizontal_corr, vertical_corr, diagonal_corr = 0, 0, 0

    return horizontal_corr, vertical_corr, diagonal_corr

# Function to calculate χ² value
def calculate_chi_squared(image):
    _, counts = np.unique(image, return_counts=True)
    expected = np.ones_like(counts) * counts.mean()
    chi_square_stat, _ = chisquare(counts, expected)
    return chi_square_stat

# Function to calculate pixel disparity metrics
def calculate_disparity_metrics(original_image, encrypted_image):
    # Ensure both images have the same dimensions
    if original_image.shape != encrypted_image.shape:
        raise ValueError("Original and encrypted images must have the same dimensions.")
    
    # MSE
    mse = np.mean((original_image - encrypted_image) ** 2)
    
    # PSNR
    psnr = 20 * np.log10(255 / np.sqrt(mse)) if mse != 0 else float('inf')
    
    # MAE
    mae = np.mean(np.abs(original_image - encrypted_image))
    
    return mse, psnr, mae

# Main function to process multiple images
if __name__ == "__main__":
    # List of image names
    image_names = [
        "baboon.jpg", "black.jpg", "brain.jpg", "cameraman.jpg",
        "grey.jpg", "lena.jpg", "peppers.jpg", "ribs.jpg"
    ]

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

        # Calculate local Shannon entropy for the cipher image
        entropy = calculate_entropy(encrypted_image)

        # Calculate correlation coefficients for both images
        original_corr = calculate_correlation(original_image)
        encrypted_corr = calculate_correlation(encrypted_image)

        # Calculate χ² value for both images
        original_chi_squared = calculate_chi_squared(original_image)
        encrypted_chi_squared = calculate_chi_squared(encrypted_image)

        # Calculate pixel disparity metrics
        try:
            mse, psnr, mae = calculate_disparity_metrics(original_image, encrypted_image)
        except ValueError as e:
            print(f"Error processing {image_name}: {e}")
            continue

        # Print the results in a readable format
        print(f"Results for {image_name}:")
        print(f"  ------------------------")
        print(f"  Local Shannon Entropy (Cipher Image): {entropy:.4f}")
        print(f"  ------------------------")
        print(f"  Correlation Coefficients:")
        print(f"    - Horizontal Correlation (Original): {original_corr[0]:.4f}")
        print(f"    - Vertical Correlation (Original): {original_corr[1]:.4f}")
        print(f"    - Diagonal Correlation (Original): {original_corr[2]:.4f}")
        print(f"    - Horizontal Correlation (Encrypted): {encrypted_corr[0]:.4f}")
        print(f"    - Vertical Correlation (Encrypted): {encrypted_corr[1]:.4f}")
        print(f"    - Diagonal Correlation (Encrypted): {encrypted_corr[2]:.4f}")
        print(f"  ------------------------")
        print(f"  χ² Value:")
        print(f"    - Original Image: {original_chi_squared:.4f}")
        print(f"    - Encrypted Image: {encrypted_chi_squared:.4f}")
        print(f"  ------------------------")
        print(f"  Pixel Disparity Metrics:")
        print(f"    - MSE (Mean Squared Error): {mse:.4f}")
        print(f"    - PSNR (Peak Signal-to-Noise Ratio): {psnr:.4f} dB")
        print(f"    - MAE (Mean Absolute Error): {mae:.4f}")
        print(f"  ------------------------\n")
