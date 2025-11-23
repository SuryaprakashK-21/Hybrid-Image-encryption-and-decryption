import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_scatter(image, direction, title, save_path):
    """
    Generate scatter plots for pixel intensities along a specified direction.
    
    Parameters:
    - image: Grayscale image as a NumPy array.
    - direction: 'horizontal', 'vertical', or 'diagonal'.
    - title: Title of the scatter plot.
    - save_path: File path to save the scatter plot.
    """
    if direction == 'horizontal':
        x = image[:, :-1].flatten()  # Current pixel values
        y = image[:, 1:].flatten()   # Adjacent pixel values
    elif direction == 'vertical':
        x = image[:-1, :].flatten()
        y = image[1:, :].flatten()
    elif direction == 'diagonal':
        x = image[:-1, :-1].flatten()
        y = image[1:, 1:].flatten()
    else:
        raise ValueError("Invalid direction! Choose 'horizontal', 'vertical', or 'diagonal'.")

    # Plot scatter diagram
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, s=1, alpha=0.5, color='blue')
    plt.title(title)
    plt.xlabel("Pixel Value (Current)")
    plt.ylabel("Pixel Value (Adjacent)")
    plt.xlim(0, 255)
    plt.ylim(0, 255)
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()

# Main Function
if __name__ == "__main__":
    # List of original image names
    image_names = [
        "baboon", "black", "brain", "cameraman",
        "grey", "lena", "peppers", "ribs"
    ]

    output_dir = "scatter_plots"
    os.makedirs(output_dir, exist_ok=True)

    for image_name in image_names:
        original_path = f"{image_name}.jpg"
        encrypted_path = f"encrypted_{image_name}.jpg"

        original_image = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
        encrypted_image = cv2.imread(encrypted_path, cv2.IMREAD_GRAYSCALE)

        if original_image is None or encrypted_image is None:
            print(f"Error: Missing files for {image_name}. Skipping...")
            continue

        # Create directories for saving scatter plots
        original_dir = os.path.join(output_dir, "original")
        encrypted_dir = os.path.join(output_dir, "encrypted")
        os.makedirs(original_dir, exist_ok=True)
        os.makedirs(encrypted_dir, exist_ok=True)

        # Generate scatter diagrams for the original image
        plot_scatter(original_image, 'horizontal', f"{image_name} - Original Horizontal Scatter",
                     os.path.join(original_dir, f"{image_name}_horizontal_scatter.png"))
        plot_scatter(original_image, 'vertical', f"{image_name} - Original Vertical Scatter",
                     os.path.join(original_dir, f"{image_name}_vertical_scatter.png"))
        plot_scatter(original_image, 'diagonal', f"{image_name} - Original Diagonal Scatter",
                     os.path.join(original_dir, f"{image_name}_diagonal_scatter.png"))

        # Generate scatter diagrams for the encrypted image
        plot_scatter(encrypted_image, 'horizontal', f"{image_name} - Encrypted Horizontal Scatter",
                     os.path.join(encrypted_dir, f"{image_name}_horizontal_scatter.png"))
        plot_scatter(encrypted_image, 'vertical', f"{image_name} - Encrypted Vertical Scatter",
                     os.path.join(encrypted_dir, f"{image_name}_vertical_scatter.png"))
        plot_scatter(encrypted_image, 'diagonal', f"{image_name} - Encrypted Diagonal Scatter",
                     os.path.join(encrypted_dir, f"{image_name}_diagonal_scatter.png"))

    print(f"Scatter diagrams saved in the '{output_dir}' directory.")
