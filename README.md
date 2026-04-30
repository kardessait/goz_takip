Eye Tracking & Drowsiness Detection System

Bu proje, bilgisayar vizyonu ve makine öğrenmesi tekniklerini kullanarak gerçek zamanlı bir uyku ve yorgunluk tespit sistemi sunar. Sistem, kullanıcının göz hareketlerini analiz ederek yorgunluk belirtileri algıladığında otomatik olarak bir uyarı mekanizması (müzik çalma) başlatır.  
+1


🛠️ Teknik Özellikler
EAR (Eye Aspect Ratio) Analizi: Gözün dikey ve yatay koordinatlarını kullanarak göz açıklık oranını matematiksel olarak hesaplar.  

Yüz İşaretleme (Face Mesh): MediaPipe kütüphanesi ile yüz üzerinde 468+ noktayı gerçek zamanlı takip eder.  

Dinamik Eşik Yönetimi: Belirlenen frame sayısı boyunca (örneğin ~1 saniye) gözlerin kapalı kalması durumunda sistemi tetikler.  

Harici Uygulama Entegrasyonu: Uyku tespiti durumunda webbrowser modülü üzerinden otomatik olarak belirlenen bir YouTube bağlantısını açar.  


🚀 Kullanılan Teknolojiler
Python: Projenin ana dili.  

OpenCV: Kamera yönetimi ve görüntü işleme.  

MediaPipe: Yüksek hassasiyetli yüz ve göz landmark tespiti.  

NumPy: Göz koordinatları arasındaki Öklid mesafesinin hesaplanması.


💻 Nasıl Çalıştırılır?

Bağımlılıkları Yükleyin: ```bash pip install opencv-python mediapipe numpy ```


Sistemi Başlatın: ```python3 göz.py ```

Kısayollar:

SPACE: Manuel olarak müzik testini başlatır.  

q: Uygulamadan güvenli çıkış sağlar.
