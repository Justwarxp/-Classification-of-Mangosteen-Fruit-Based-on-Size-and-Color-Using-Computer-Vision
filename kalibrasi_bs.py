import cv2
import numpy as np
import json
import time


# path untuk json
path_json = "bs.json"


# kamera
cap = cv2.VideoCapture(1)

# mencari total pixel
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
full_pixel = width * height

resize_screen = 50  # %

# kode warna RGB merah upper dan lower
merah1 = [0, 0]
hijau1 = [0, 0]
biru1 = [0, 0]


def nothing(x):
    pass


# Buat jendela untuk slider
cv2.namedWindow('Settings')

# Buat trackbar untuk menyesuaikan nilai batas atas dan bawah untuk warna merah
cv2.createTrackbar('Red', 'Settings', 0, 255, nothing)
cv2.createTrackbar('Green', 'Settings', 0, 255, nothing)
cv2.createTrackbar('Blue', 'Settings', 0, 255, nothing)

cv2.createTrackbar('Red_lower', 'Settings', 0, 255, nothing)
cv2.createTrackbar('Green_lower', 'Settings', 0, 255, nothing)
cv2.createTrackbar('Blue_lower', 'Settings', 0, 255, nothing)


j = input("mulai ?, tekan enter")

while 1:

    ret, frame = cap.read()

    # ret will return a true value if the frame exists otherwise False
    into_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Dapatkan nilai trackbar saat ini
    red_upper = cv2.getTrackbarPos('Red', 'Settings')
    red_lower = cv2.getTrackbarPos('Red_lower', 'Settings')
    green_upper = cv2.getTrackbarPos('Green', 'Settings')
    green_lower = cv2.getTrackbarPos('Green_lower', 'Settings')
    blue_upper = cv2.getTrackbarPos('Blue', 'Settings')
    blue_lower = cv2.getTrackbarPos('Blue_lower', 'Settings')

    # Membuat masker menggunakan fungsi inRange()
    # ini akan menghasilkan gambar di mana warna objek
    # yang jatuh dalam rentang akan menjadi putih dan sisanya akan menjadi hitam

    # Batas untuk warna merah
    limit_a_merah = np.array([red_upper, green_upper, blue_upper])
    limit_b_merah = np.array([red_lower, green_lower, blue_lower])

    # simpan data warna
    merah1 = [red_upper, red_lower]
    hijau1 = [green_upper, green_lower]
    blue1 = [blue_upper, blue_lower]

    # rgb to hsv
    r_mask = cv2.inRange(into_hsv, limit_b_merah, limit_a_merah)
    total_red_pixels = cv2.countNonZero(r_mask)

    # untuk tampilan
    warna = cv2.bitwise_and(frame, frame, mask=r_mask)
    print("Total pixel bs : ", round(
        total_red_pixels/full_pixel * 100, 3), "%")

    # write json merah
    data = {
        "bs": [merah1, hijau1, biru1]
    }

    with open(path_json, 'w') as f:
        json.dump(data, f)

        # Ini akan memberi warna pada masker.
    frame = cv2.resize(frame, (int(width*resize_screen/100),
                       int(height*resize_screen/100)))
    warna = cv2.resize(warna, (int(width*resize_screen/100),
                       int(height*resize_screen/100)))
    cv2.imshow('Original', frame)  # untuk menampilkan frame asli
    cv2.imshow('Color BS', warna)  # untuk menampilkan output objek merah

    if cv2.waitKey(1) == 27:
        break

# lepaskan kamera dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
