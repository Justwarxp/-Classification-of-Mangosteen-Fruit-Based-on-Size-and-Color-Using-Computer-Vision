import cv2
import numpy as np

# Baca gambar referensi
image = cv2.imread('6.jpg')

# Ubah gambar menjadi grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Thresholding untuk memisahkan objek dari latar belakang
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Temukan kontur objek
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Asumsikan kontur terbesar adalah objek referensi
reference_contour = max(contours, key=cv2.contourArea)

# Hitung luas piksel dari kontur objek referensi
luas_pixel_jarak_patokan = cv2.contourArea(reference_contour)

print("Luas piksel pada jarak patokan:", luas_pixel_jarak_patokan)
