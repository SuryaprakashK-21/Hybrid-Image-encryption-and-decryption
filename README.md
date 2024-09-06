# Hybrid Image Encryption and Decryption

## Introduction

This project proposes an advanced and secure image encryption method designed specifically for defense and medical security. The encryption method integrates two main phases: a confusion phase, which scrambles the pixel positions, and a diffusion phase, which alters the intensity of individual pixel values. This hybrid approach ensures a high level of security against various types of attacks.

## Objectives

- **Key Generation**: Generate a robust key using the SHA-3 algorithm for the given image.
- **Pixel Position Scrambling**: Use the Fibonacci-Lucas transform to change pixel positions.
- **Pixel Intensity Modification**: Alter individual pixel intensities using the Tribonacci transform.

## Methodology

### 1. Key Generation (SHA-3)
- The SHA-3 algorithm is employed to generate keys with high randomness and resistance against attacks. It supports variable output lengths, providing flexibility and enhanced security.

### 2. Confusion Phase (Fibonacci-Lucas Transform)
- The pixel positions of the plain image are scrambled using the Fibonacci-Lucas transform, which combines properties of both Fibonacci and Lucas sequences to achieve high randomness and complex key distribution.

### 3. Diffusion Phase (Tribonacci Transform)
- The pixel intensities of the scrambled image are modified using the Tribonacci transform, which further enhances the diffusion properties and adds an extra layer of security.

## Advantages of the Proposed Methodology

1. **SHA-3 Algorithm**:
   - Large key space (up to 1024 bits) suitable for military applications.
   - High resistance due to sponge construction.
   - Variable output lengths for enhanced security.
   - Simple padding scheme for efficient processing.

2. **Fibonacci-Lucas Transform**:
   - Provides high randomness and strong key distribution.
   - Combines the properties of both Fibonacci and Lucas sequences, adding complexity to the encryption process.

## Flow of Work

### **Encryption**
1. **Image Input**: The user provides the plain image for encryption.
2. **Key Generation**: Generate the encryption key using the SHA-3 algorithm.
3. **Confusion Phase**: Apply the Fibonacci-Lucas transform to scramble the pixel positions.
4. **Diffusion Phase**: Use the Tribonacci transform to modify pixel intensities.
5. **Output**: Generate the cipher (encrypted) image.

### **Decryption**
1. **Inverse Diffusion Phase**: Reverse the Tribonacci transform to restore pixel intensities.
2. **Inverse Confusion Phase**: Apply the inverse Fibonacci-Lucas transform to restore pixel positions.
3. **Output**: Obtain the original (decrypted) image.

## Histogram Analysis

The histogram analysis involves examining the distribution of pixel intensity values in both the original and encrypted images. Our proposed method demonstrates excellent performance in achieving a uniform histogram distribution for the encrypted image, indicating high security and resistance against statistical attacks.

## Time Analysis

The encryption algorithm was benchmarked on an Intel i5 11400H processor with 8 GB RAM using Python. The average execution times for various transformations are as follows:

- **Fibonacci-Lucas Transformation**: 0.68 seconds
- **Arnold Transformation**: 2.6047 seconds
- **Fibonacci Transformation**: 2.2097 seconds
- **Poker Shuffle**: 0.79689 seconds

## Requirements

- **Python 3.x**
- **Libraries**: `numpy`, `PIL`, `hashlib`, `matplotlib`

You can install the required libraries using:
```bash
pip install numpy pillow matplotlib
```

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SuryaprakashK-21/Hybrid-Image-Encryption-and-Decryption.git
   cd Hybrid-Image-Encryption-and-Decryption
   ```
2. **Run the script**:
   Use Jupyter Notebook or any Python environment to run the `encryption_decryption.py` script.
3. **Input**: Provide the path to the image for encryption.
4. **Output**: View the encrypted and decrypted images along with their histograms.

## Future Enhancements

- **Quantum-resistant Algorithms**: Explore quantum-resistant encryption methods to further strengthen security.
- **Multi-Layer Encryption**: Implement multiple layers of encryption to enhance robustness against combined attack vectors.
- **Real-Time Encryption**: Optimize the algorithm for real-time applications in medical imaging and defense.

## Contact

For any questions or collaboration opportunities, please reach out to [suryaprakash212004@gmail.com](mailto:suryaprakash212004@gmail.com).
