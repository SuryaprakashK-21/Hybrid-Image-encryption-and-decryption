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

# Reverse Diffusion
def reverse_diffusion(encrypted_image, key, iterations=5):
    rows, cols = encrypted_image.shape
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
    encrypted_image ^= key[0]
    confused_image = ((encrypted_image.astype(np.int16) - logistic_map_values.astype(np.int16)) % 256).astype(np.uint8)
    return confused_image

# Reverse Fibonacci Transform
def reverse_fibonacci_transform(confused_image, key):
    rows, cols = confused_image.shape
    seed = sum(byte for byte in key) % 256
    fib = [seed, (seed + 1) % 256]

    for i in range(2, rows * cols):
        fib.append((fib[-1] + fib[-2]) % 256)

    fib = np.array(fib[:rows * cols]).reshape(rows, cols)
    original_image = (confused_image - fib) % 256
    return original_image

# Encryption pipeline
def encrypt_image(image):
    key = generate_key(image)
    confused_image = fibonacci_transform_with_key(image, key)
    encrypted_image = logistic_map_diffusion(confused_image, key)
    return encrypted_image, key

# Decryption pipeline
def decrypt_image(encrypted_image, key):
    confused_image = reverse_diffusion(encrypted_image, key)
    original_image = reverse_fibonacci_transform(confused_image, key)
    original_image = np.clip(original_image, 0, 255).astype(np.uint8)
    return original_image

# Function to calculate NPCR
def calculate_npcr(original_image, modified_image):
    diff = (original_image != modified_image).astype(np.uint8)
    npcr = np.sum(diff) / diff.size * 100
    return npcr

# Function to calculate UACI
def calculate_uaci(original_image, modified_image):
    diff = np.abs(original_image.astype(np.int16) - modified_image.astype(np.int16))
    uaci = np.mean(diff / 255.0) * 100
    return uaci

if __name__ == "__main__":
    image_names = [
         "lena.jpg"
    ]

    pixel_positions = [(0, 0), (0, 511), (511, 0), (511, 511), (255, 255), (149, 209)]

    for image_name in image_names:
        input_image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

        if input_image is None:
            print(f"Error: Image {image_name} not found.")
            continue

        rows, cols = input_image.shape
        print(f"\n==================== Results for {image_name} ====================")
        for position in pixel_positions:
            x, y = position
            # Ensure the pixel position is valid
            if 0 <= x < rows and 0 <= y < cols:
                modified_image = input_image.copy()
                modified_image[x, y] = np.clip(modified_image[x, y] + 1, 0, 255)  # Modify a single pixel

                # Encrypt both the original and modified images
                encrypted_original, key_original = encrypt_image(input_image)
                encrypted_modified, key_modified = encrypt_image(modified_image)

                # Compute NPCR and UACI for differential analysis
                npcr = calculate_npcr(encrypted_original, encrypted_modified)
                uaci = calculate_uaci(encrypted_original, encrypted_modified)

                # Output the results for the modified pixel position
                print(f"\nModified Pixel Position: ({x+1}, {y+1})")  # Use 1-based indexing for output
                print(f"  NPCR: {npcr:.2f}%")
                print(f"  UACI: {uaci:.2f}%")
            else:
                print(f"Invalid Pixel Position: ({x+1}, {y+1})")

        # Save the images
        cv2.imwrite(f"encrypted_{image_name}", encrypted_original)
        cv2.imwrite(f"decrypted_{image_name}", decrypt_image(encrypted_original, key_original))

        print(f"Processed {image_name}\n")
