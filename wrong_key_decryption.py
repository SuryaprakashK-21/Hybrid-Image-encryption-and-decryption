import numpy as np
import cv2
from argon2 import PasswordHasher
import hashlib
import os

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

# Decryption pipeline (using wrong key)
def decrypt_with_wrong_key(encrypted_image, wrong_key):
    confused_image = reverse_diffusion(encrypted_image, wrong_key)
    original_image = reverse_fibonacci_transform(confused_image, wrong_key)
    original_image = np.clip(original_image, 0, 255).astype(np.uint8)
    return original_image

# Main function to process multiple images
if __name__ == "__main__":
    image_names = [
        "baboon.jpg", "black.jpg", "brain.jpg", "cameraman.jpg",
        "grey.jpg", "lena.jpg", "peppers.jpg", "ribs.jpg"
    ]

    output_dir = "wrong_key_decryption"
    os.makedirs(output_dir, exist_ok=True)

    for image_name in image_names:
        input_image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

        if input_image is None:
            print(f"Error: Image {image_name} not found.")
            continue

        encrypted_image, correct_key = encrypt_image(input_image)

        # Generate a wrong key (by altering the correct key slightly)
        wrong_key = hashlib.sha256(b"wrong_key").digest()[:16]

        # Decrypt using the wrong key
        decrypted_image_with_wrong_key = decrypt_with_wrong_key(encrypted_image, wrong_key)

        # Save the result
        wrong_key_output_path = os.path.join(output_dir, f"wrong_decrypted_{image_name}")
        cv2.imwrite(wrong_key_output_path, decrypted_image_with_wrong_key)

        print(f"Processed {image_name} with wrong key. Saved result to {wrong_key_output_path}.")
