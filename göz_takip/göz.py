import cv2
import mediapipe as mp
import webbrowser
import time
import numpy as np

# Göz takibi için kurulum
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
cap = cv2.VideoCapture(0)

# Kamera açılıp açılmadığını kontrol et
if not cap.isOpened():
    print("HATA: Kamera açılamadı! Lütfen kamerayı kontrol edin.")
    print(f"Kamera cihazı: {cap.get(cv2.CAP_PROP_DEVICE_ID)}")
    exit()

# Kamera ayarları
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# YouTube Linki
muzik_url = "https://www.youtube.com/watch?v=Xe97kCPSjYQ&list=RDT4k57yBADXo&index=2"

# Göz özellikleri
uyku_sayaci = 0
EYE_AR_THRESH = 0.30  # Göz açıklık eşiği (daha yüksek = daha az hassas)
CLOSED_FRAMES_THRESHOLD = 30  # Uyku tespit için kapalı frame sayısı (~1 saniye @ 30fps)
frame_sayisi = 0
debug_mode = True  # Debug mesajlarını aç/kapat

def calculate_eye_aspect_ratio(landmarks):
    """Göz oranını (EAR) hesapla"""
    # EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
    p2 = np.array([landmarks[1].x, landmarks[1].y])
    p3 = np.array([landmarks[2].x, landmarks[2].y])
    p4 = np.array([landmarks[3].x, landmarks[3].y])
    p5 = np.array([landmarks[4].x, landmarks[4].y])
    p6 = np.array([landmarks[5].x, landmarks[5].y])
    p1 = np.array([landmarks[0].x, landmarks[0].y])
    
    dist_vertical1 = np.linalg.norm(p2 - p6)
    dist_vertical2 = np.linalg.norm(p3 - p5)
    dist_horizontal = np.linalg.norm(p1 - p4)
    
    ear = (dist_vertical1 + dist_vertical2) / (2 * dist_horizontal + 1e-6)
    return ear

def is_eyes_closed(face_landmarks):
    """Gözlerin kapalı olup olmadığını kontrol et"""
    # Sol göz landmark'ları => MediaPipe'da (362-367)
    LEFT_EYE = [362, 385, 387, 263, 373, 380]
    # Sağ göz landmark'ları => MediaPipe'da (33-38)
    RIGHT_EYE = [33, 160, 158, 133, 153, 144]
    
    try:
        left_eye_landmarks = [face_landmarks.landmark[i] for i in LEFT_EYE]
        right_eye_landmarks = [face_landmarks.landmark[i] for i in RIGHT_EYE]
        
        left_ear = calculate_eye_aspect_ratio(left_eye_landmarks)
        right_ear = calculate_eye_aspect_ratio(right_eye_landmarks)
        
        avg_ear = (left_ear + right_ear) / 2
        
        return avg_ear < EYE_AR_THRESH
    except Exception as e:
        return False

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    frame_sayisi += 1
    
    # Görüntüyü RGB'ye dönüştür
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    
    face_detected = False
    if results.multi_face_landmarks:
        face_detected = True
        for face_landmarks in results.multi_face_landmarks:
            # Gözlerin kapalı olup olmadığını kontrol et
            if is_eyes_closed(face_landmarks):
                uyku_sayaci += 1
            else:
                uyku_sayaci = 0
    else:
        # Yüz algılanamadı, sayacı sıfırla
        uyku_sayaci = 0
    
    # Bilgi göster
    status = "Yüz bulundu" if face_detected else "Yüz bulunamadı"
    cv2.putText(frame, f'Status: {status}', (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f'Kapali: {uyku_sayaci}/{CLOSED_FRAMES_THRESHOLD}', (10, 70),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, 'SPACE: Muzik AC | q: Cikis', (10, 110),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    if debug_mode and frame_sayisi % 10 == 0:  # Her 10. frame'de yazdır
        print(f"Frame: {frame_sayisi} | Status: {status} | Kapali: {uyku_sayaci}/{CLOSED_FRAMES_THRESHOLD}")
    
    # Eğer gözler CLOSED_FRAMES_THRESHOLD frame kapalı kaldıysa:
    if uyku_sayaci > CLOSED_FRAMES_THRESHOLD:
        print("Uyku tespit edildi! Müzik açılıyor...")
        cv2.putText(frame, 'UYKU TESPIT EDILDI!', (50, 150),
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        cv2.imshow('Goz Takip Sistemi', frame)
        cv2.waitKey(500)
        webbrowser.open(muzik_url)
        break

    cv2.imshow('Goz Takip Sistemi', frame)
    
    # Tuş kontrolleri
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # q tuşu: çıkış
        break
    elif key == ord(' '):  # SPACE tuşu: müzik aç
        print("Müzik açılıyor...")
        webbrowser.open(muzik_url)
        break

cap.release()
cv2.destroyAllWindows()