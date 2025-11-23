import numpy as np
import cv2
from argon2 import PasswordHasher
import hashlib

# Key Generation using Argon2
def generate_key(image):
    ph = PasswordHasher()
    image_hash = hashlib.sha256(image.tobytes()).hexdigest()
    key = ph.hash(image_hash).encode()
    return hashlib.sha256(key).digest()[:16]  # 16-byte key

# Confusion phase using Key-dependent Fibonacci Transform
def fibonacci_transform_with_key(image, key):
    rows, cols = image.shape
    seed = sum(byte for byte in key) % 256
    fib = [seed, (seed + 1) % 256]

    for i in range(2, rows * cols):
        fib.append((fib[-1] + fib[-2]) % 256)

    fib = np.array(fib[:rows * cols]).reshape(rows, cols)
    confused_image = (image + fib) % 256
    return confused_image

# Diffusion phase using Logistic Map
def logistic_map_diffusion(confused_image, key, iterations=5):
    rows, cols = confused_image.shape
    key_seed = sum(byte for byte in key)
    x = 0.5 + (key_seed % 100) / 1000
    r = 3.99

    total_pixels = rows * cols
    logistic_map = np.empty(total_pixels, dtype=np.float64)
    logistic_map[0] = x

    for _ in range(iterations):
        for i in range(1, total_pixels):
            logistic_map[i] = r * logistic_map[i - 1] * (1 - logistic_map[i - 1])

    logistic_map_values = ((logistic_map * 256) % 256).astype(np.uint8).reshape(rows, cols)
    encrypted_image = ((confused_image + logistic_map_values) % 256).astype(np.uint8)
    encrypted_image ^= key[0]
    return encrypted_image

# Encryption pipeline
def encrypt_image(image, key):
    confused_image = fibonacci_transform_with_key(image, key)
    encrypted_image = logistic_map_diffusion(confused_image, key)
    return encrypted_image

# Function to calculate NPCR
def calculate_npcr(original_image, encrypted_image):
    diff = (original_image != encrypted_image).astype(np.uint8)
    npcr = np.sum(diff) / diff.size * 100  # Percentage of differing pixels
    return npcr

# Function to calculate UACI
def calculate_uaci(original_image, encrypted_image):
    diff = np.abs(original_image.astype(np.int16) - encrypted_image.astype(np.int16))
    uaci = np.mean(diff / 255.0) * 100  # Average of the intensity differences scaled to percentage
    return uaci

# Main function to process multiple images for key sensitivity analysis
if __name__ == "__main__":
    image_names = [
        "baboon.jpg", "black.jpg", "brain.jpg", "cameraman.jpg",
        "grey.jpg", "lena.jpg", "peppers.jpg", "ribs.jpg"
    ]
    for image_name in image_names:
        input_image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

        if input_image is None:
            print(f"Error: Image {image_name} not found.")
            continue

        # Generate reference encrypted image with original key
        key = generate_key(input_image)
        encrypted_image = encrypt_image(input_image, key)

        # Generate another encrypted image by slightly modifying the key (e.g., changing one byte)
        modified_key = bytearray(key)
        modified_key[0] ^= 0x01  # Modify the first byte to create a different key
        modified_key = bytes(modified_key)

        encrypted_image_modified = encrypt_image(input_image, modified_key)

        # Calculate NPCR and UACI for the original vs the modified encrypted image
        npcr = calculate_npcr(input_image, encrypted_image_modified)
        uaci = calculate_uaci(input_image, encrypted_image_modified)

        # Display the results
        print(f"Key Sensitivity Analysis for {image_name}:")
        print(f"  Original Image vs Modified Encrypted Image:")
        print(f"    NPCR: {npcr:.2f}%")
        print(f"    UACI: {uaci:.2f}%")
        print("-" * 50)
f
