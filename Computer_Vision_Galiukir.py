from ultralytics import YOLO
import cv2
import time
import numpy as np
import serial
import requests
import json


# upload data ke server IOT
url = "https://galiukirmanggis.biz.id/server.php"

############################################################################

# Change this to match your serial port (e.g., '/dev/ttyUSB0' on Linux)
serial_port = 'COM12'
baud_rate = 9600

# kalibrasi
jarak_patokan = 12.5  # jarak kamera ke manggis
ukuran_patokan = 6  # ukuran patokan manggis
# jumlah pixel manggis pada jarak 12,5 cm dari kamera
luas_pixel_jarak_patokan = 116500

# ukuran manggis dalam centimeter
ukuran_kecil = 4  # < 4cm
ukuran_sedang = [5, 7]  # (rentang nilai 4 sampai 8 cm)
ukuran_besar = 7  # > 8cm

# jumlah manggis super1, super2, super3(falcon), super_jumbo, bs, super1_export & super2_export
jumlah_manggis = [0, 0, 0, 0, 0, 0]


# 0 = webcam laptop, 1 = kamera USB
cam = cv2.VideoCapture(1)

# path model
model = YOLO('computer_vision.pt')
data_bs = "bs.json"

batas_deteksi_bs = 30  # 30 persen warna bs pada buah
batas_burik_bs = 15  # persen

################################################################################################################

try:
    ser = serial.Serial(serial_port, baud_rate)
except:
    print("PERIKSA NAMA COM ")

deteksi = "1"

warna_bs = [[0, 0], [0, 0], [0, 0]]
# setting the blue upper limit


try:
    with open(data_bs, 'r') as f:
        data_kode = json.load(f)
        warna_bs = data_kode["bs"]

except:
    print("pastikan sudah kalibrasi warna manggis BS")

limit_atas = np.array(
    [warna_bs[0][0], warna_bs[1][0], warna_bs[2][0]])
# setting the blue lower limit
limit_bawah = np.array(
    [warna_bs[0][1], warna_bs[1][1], warna_bs[2][1]])


# menghitung burik
def compute_texture_roughness(image):
    # Ubah gambar ke grayscale jika belum grayscale
    if len(image.shape) > 2:
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image

    # Hitung kontras menggunakan deviasi standar intensitas piksel
    contrast_score = np.std(image_gray)

    # Normalisasi ke rentang 0-100%
    max_contrast = 255.0  # karena gambar grayscale dengan intensitas 0-255
    roughness_percent = (contrast_score / max_contrast) * 100

    return roughness_percent


def send_command_to_arduino(status):
    """
    Mengirim perintah status ke Arduino melalui serial.
    """
    try:
        ser.write(str(status).encode())
        print("Mengirim perintah ke Arduino")
    except Exception as e:
        print("Gagal mengirim perintah ke Arduino:", e)



def send_data():
    # Mengirim permintaan GET dengan data
    print("Mengirim data .. ")
    data = {
        'apikey': '7b9f15a16d92de22fba7e38e65499652',
        'bs': jumlah_manggis[5],
        'super_export': jumlah_manggis[4],
        'super_jumbo': jumlah_manggis[3],
        'super_3': jumlah_manggis[2],
        'super_2': jumlah_manggis[1],
        'super_1': jumlah_manggis[0]
    }
    try:
        response = requests.get(url, params=data)
    except:
        print("Gagal mengirim data ke server .. ")


def get_data_server():
    global jumlah_manggis
    url_get = "https://galiukirmanggis.biz.id/server_get.php"
    print("update data dari server .. ")
    try:
        jumlah_manggis[0] = int(requests.get(
            url_get + "?id_sensor=SEN20240426110906797").json()["nilai"])
        time.sleep(0.2)
        jumlah_manggis[1] = int(requests.get(
            url_get + "?id_sensor=SEN20240426110925438").json()["nilai"])
        time.sleep(0.2)
        jumlah_manggis[2] = int(requests.get(
            url_get + "?id_sensor=SEN20240426110947449").json()["nilai"])
        time.sleep(0.2)
        jumlah_manggis[3] = int(requests.get(
            url_get + "?id_sensor=SEN20240426110958463").json()["nilai"])
        time.sleep(0.2)
        jumlah_manggis[4] = int(requests.get(
            url_get + "?id_sensor=SEN20240426111010640").json()["nilai"])
        time.sleep(0.2)
        jumlah_manggis[5] = int(requests.get(
            url_get + "?id_sensor=SEN20240426111022655").json()["nilai"])
        time.sleep(0.2)
    except:
        jumlah_manggis = [0, 0, 0, 0, 0, 0]


while True:

    
    time1 = time.time()
    res, frame = cam.read()
    status = 0
    count_frame = 0
     
     # Resize frame untuk memperbesar tampilan
    #frame = cv2.resize(frame, (0, 0), fx=1.1, fy=1.1)


    #Update data dari server
    #get_data_server()

    # Run inference on an image
    results = model(frame)  # results list
    for r in results:
        boxes = (r.boxes.xyxy).tolist()

        for box in boxes:

            prob = 0
            label = ""
            luas_pixel = 0

            try:
                cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(
                    box[2]), int(box[3])), (0, 255, 0), 2)
                luas_pixel = (
                    np.abs((int(box[0]) - int(box[2])) * ((int(box[3]) - int(box[1])))))
                ukuran_buah = round(
                    ukuran_patokan*luas_pixel/luas_pixel_jarak_patokan, 4)
                cv2.putText(frame, "Ukuran Buah : " + str(ukuran_buah) + " cm", (int(
                    box[0]), int(box[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # open cv

                # burik detection
                x1, y1, x2, y2 = int(box[0]), int(
                    box[1]), int(box[2]), int(box[3])
                roi = frame[y1:y2, x1:x2]
                burik = round(compute_texture_roughness(roi), 1)
                cv2.putText(frame, "Burik : " + str(burik) + " %", (int(
                    box[0]+10), int(box[1]) + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                # bs detection
                # mencari total pixel
                height, width, _ = roi.shape
                full_pixel = width * height
                into_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                bs_mask = cv2.inRange(into_hsv, limit_bawah, limit_atas) 

                total_bs_pixels = cv2.countNonZero(bs_mask)

                t_bs = round(total_bs_pixels/full_pixel * 100, 3)
                cv2.putText(frame, "BS : " + str(t_bs) + "%", (int(
                    box[0]) + 240, int(box[1]) + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            except:
                pass

            for a in r.boxes.cls:
                try:
                    label = model.names[int(a)]

                    ukuran_buah = round(
                        ukuran_patokan*luas_pixel/luas_pixel_jarak_patokan, 4)
                    print("model : ", label)
                    cv2.putText(frame, label, (int(box[0]), int(
                        box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    if label == "manggis_hijau":

                        if ukuran_buah <= ukuran_kecil:
                         
                         if burik >= 5 and burik < 10:
                             cv2.putText(frame, "Kategori : Super 1 (Ekspor)", (int(
                                    box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                             if deteksi == "1":
                                    time.sleep(8)
                                    status = 5
                                    jumlah_manggis[4] += 1
                                    time.sleep(8)
                                    send_command_to_arduino(5)
                                    
                            

                        elif ukuran_buah <= ukuran_sedang[1] and ukuran_buah > ukuran_sedang[0]:
                            # print("ukuran sedang manggis_hijau")
                            if burik >= 5 and burik < 10:
                                cv2.putText(frame, "Kategori : Super 1 (Ekspor)", (int(
                                    box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                if deteksi == "1":
                                    time.sleep(8)
                                    status = 5
                                    jumlah_manggis[4] += 1
                                    time.sleep(8)
                                    send_command_to_arduino(5)
                                    

                            elif burik >= 10 and burik <= 15:
                                cv2.putText(frame, "Kategori : Super 2 (Ekspor)", (int(
                                    box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                if deteksi == "1":
                                    time.sleep(8)
                                    status = 5
                                    jumlah_manggis[4] += 1
                                    time.sleep(8)
                                    send_command_to_arduino(5)

                        elif ukuran_buah > ukuran_besar:
                            print("ukuran besar manggis_hijau")
                            # cv2.putText(frame, "Besar", (int(
                            #     box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                            # if deteksi == "1":
                            #     status = 3
                            #     # jumlah_manggis_hijau[2] += 1
                            #     ser.write(str(status).encode())

                        if deteksi == "1":
                            send_data()
                            deteksi = "1"

                    if label == "manggis_ungu":

                        if ukuran_buah <= ukuran_kecil:
                            # print("ukuran kecil manggis_ungu")
                            if burik > 10 and burik < 15:
                                cv2.putText(frame, "Kategori : Super 3 (falcon)", (int(
                                    box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                if deteksi == "1":
                                    time.sleep(8)
                                    status = 3
                                    jumlah_manggis[2] += 1
                                    time.sleep(8)
                                    send_command_to_arduino(3)
                                    
                            elif burik > batas_burik_bs and t_bs > batas_deteksi_bs:  # jika burik diatas 15% dan warna bs diatas 30%
                                cv2.putText(frame, "Kategori : BS ", (int(
                                    box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                if deteksi == "1":
                                    time.sleep(8)
                                    status = 6
                                    time.sleep(8)
                                    jumlah_manggis[5] += 1
                                    send_command_to_arduino(6)
                                    #time.sleep(0.5)

                        elif ukuran_buah <= ukuran_sedang[1] and ukuran_buah > ukuran_sedang[0]:
                            # print("ukuran sedang manggis_ungu")

                            if burik > 10 and burik < 15:
                                cv2.putText(frame, "Kategori : Super 1", (int(
                                    box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                if deteksi == "1":
                                    time.sleep(8)
                                    status = 1
                                    time.sleep(8)
                                    jumlah_manggis[0] += 1
                                    send_command_to_arduino(1)
                                    

                            elif burik > 15:
                                if burik > batas_burik_bs and t_bs > batas_deteksi_bs:  # jika burik diatas 15% dan warna bs diatas 30%
                                    cv2.putText(frame, "Kategori : BS", (int(
                                        box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                    if deteksi == "1":
                                        time.sleep(8)
                                        status = 6
                                        time.sleep(8)
                                        jumlah_manggis[5] += 1
                                        send_command_to_arduino(6)
                                        
                                else:
                                    cv2.putText(frame, "Kategori : Super 2", (int(
                                        box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                    if deteksi == "1":
                                        time.sleep(8)
                                        status = 2
                                        time.sleep(8)
                                        jumlah_manggis[1] += 1
                                        time.sleep(8)
                                        send_command_to_arduino(2)
                                       
                                        

                        elif ukuran_buah > ukuran_besar:
                            # print("ukuran besar manggis_ungu")
                            if burik > 10:
                                if burik > batas_burik_bs and t_bs > batas_deteksi_bs:  # jika burik diatas 15% dan warna bs diatas 30%
                                    cv2.putText(frame, "Kategori : BS", (int(
                                        box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                    if deteksi == "1":
                                        time.sleep(8)
                                        status = 6
                                        time.sleep(8)
                                        jumlah_manggis[5] += 1
                                        send_command_to_arduino(6)
                                        
                                        
                                else:
                                    cv2.putText(frame, "Kategori : Super Jumbo", (int(
                                        box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                    if deteksi == "1":
                                        time.sleep(12)
                                        status = 4
                                        jumlah_manggis[3] += 1
                                        time.sleep(8)
                                        send_command_to_arduino(4)
                                        
                                             

                        if deteksi == "1":
                            send_data()
                        deteksi = "1"


                    if label =="manggis_coklat":

                        if ukuran_buah <= ukuran_kecil:
                            #if burik > 15:

                             #if burik > batas_burik_bs and t_bs > batas_deteksi_bs:
                                cv2.putText(frame, "Kategori : BS ", (int(
                                    box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                if deteksi == "1":
                                    time.sleep(8)
                                    status = 6
                                    jumlah_manggis[5] += 1
                                    time.sleep(8)
                                    send_command_to_arduino(6)
                                    
                                
                        elif ukuran_buah <= ukuran_sedang[1] and ukuran_buah > ukuran_sedang[0]:
                            #if burik >15:

                             #if burik > batas_burik_bs and t_bs > batas_deteksi_bs:
                                cv2.putText(frame, "Kategori : BS", (int(
                                        box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                if deteksi == "1":
                                        time.sleep(8)
                                        status = 6
                                        time.sleep(8)
                                        jumlah_manggis[5] += 1
                                        send_command_to_arduino(6)
                                        

                        elif ukuran_buah > ukuran_besar:
                            #if burik >15:

                             #if burik > batas_burik_bs and t_bs > batas_deteksi_bs:
                                cv2.putText(frame, "Kategori : BS", (int(
                                        box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                                if deteksi == "1":
                                        time.sleep(12)
                                        status = 6
                                        time.sleep(8)
                                        jumlah_manggis[5] += 1
                                        send_command_to_arduino(6)
                                        

                                if deteksi == "1":
                                  send_data()
                        deteksi = "1"


                    if label =="apel_merah":

                       if ukuran_buah <= ukuran_sedang[1] and ukuran_buah > ukuran_sedang[0]:
                           
                           cv2.putText(frame, "Kategori : BS ", (int(
                                    box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                           if deteksi == "1":
                                        status = 6
                                        jumlah_manggis[5] += 1
                                        send_command_to_arduino(6)
                                        time.sleep(0.5)

                           elif ukuran_buah > ukuran_besar:
                            
                            cv2.putText(frame, "Kategori : BS", (int(
                                        box[0]) + 10, int(box[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                            if deteksi == "1":
                                        status = 6
                                        jumlah_manggis[5] += 1
                                        send_command_to_arduino(6)
                                        time.sleep(0.5)


                           if deteksi == "1":
                             send_data()
                           deteksi = "1"

                except:
                    pass

                break

            for b in r.boxes.conf:
                try:
                    prob = round(b.squeeze().tolist(), 2)*100
                    print("confidence : ", prob)
                    cv2.putText(frame, str(prob)+"%", (int(box[0]) + 220, int(
                        box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                    cv2.putText(frame, " PIXEL : " + str(luas_pixel), (int(box[0]-10), int(
                        box[1]) - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 250), 2)
                except:
                    pass

                break

            break
        break

        # Menunggu tombol 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow("frame", frame)

     # Mengirim perintah ke Arduino
    #if deteksi == "1":
        #send_command_to_arduino(status)
        #deteksi = "0"
