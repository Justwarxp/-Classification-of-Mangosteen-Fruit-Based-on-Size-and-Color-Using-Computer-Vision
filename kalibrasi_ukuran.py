import cv2
import numpy as np

# Kalibrasi
jarak_patokan = 12.5  # jarak kamera ke manggis dalam cm
ukuran_patokan = 60  # ukuran patokan manggis dalam mm (6 cm = 60 mm)
# jumlah pixel manggis pada jarak 12,5 cm dari kamera
luas_pixel_jarak_patokan = 116500

# ukuran manggis dalam milimeter
ukuran_kecil = 40  # < 40mm
ukuran_sedang = [50, 60]  # (rentang nilai 50 sampai 60 mm)
ukuran_besar = 80  # > 80mm

# Pastikan ukuran frame tetap konsisten
frame_width = 640
frame_height = 480

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

ret, frame = cap.read()

if ret:
    # Tidak mengubah ukuran frame secara dinamis
    cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
    luas_pixel = np.abs((int(box[0]) - int(box[2])) * (int(box[3]) - int(box[1])))
    ukuran_buah = round(ukuran_patokan * luas_pixel / luas_pixel_jarak_patokan, 4)
    cv2.putText(frame, "Ukuran Buah : " + str(ukuran_buah) + " mm", (int(box[0]), int(box[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
