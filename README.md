# Sertifika Hazırlama ve Gönderme Aracı

Bu proje, etkinlik katılımcıları için toplu sertifika hazırlamak ve e-posta yoluyla göndermek amacıyla geliştirilmiş, kullanıcı dostu arayüze sahip bir masaüstü uygulamasıdır.

## Özellikler

*   **Grafik Arayüz (GUI):** Modern ve kullanımı kolay arayüz.
*   **Toplu Sertifika Oluşturma:** CSV dosyasından katılımcı listesini okur ve her biri için kişiselleştirilmiş sertifika oluşturur.
*   **E-posta Gönderimi:** Oluşturulan sertifikaları katılımcıların e-posta adreslerine otomatik olarak gönderir.
*   **Özelleştirilebilir Ayarlar:** Font, yazı rengi, yazı boyutu, e-posta konusu ve mesaj içeriği gibi ayarlar arayüz üzerinden kolayca değiştirilebilir.
*   **Log Takibi:** İşlem durumlarını anlık olarak takip edebileceğiniz log ekranı.

## Kurulum

1.  Projeyi bilgisayarınıza indirin.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

1.  Uygulamayı çalıştırın:
    ```bash
    python app/gui.py
    ```
2.  **Ana İşlemler** sekmesinden:
    *   **Katılımcı Listesi:** `list.csv` formatındaki dosyanızı seçin. (Format: ID, İsim, Email)
    *   **Sertifika Şablonu:** Sertifika tasarımınız olan resim dosyasını (.png, .jpg) seçin.
3.  **Ayarlar** ve **Mail Ayarları** sekmelerinden gerekli yapılandırmaları yapın.
    *   Mail gönderimi için gönderici e-posta ve şifrenizi girin.
4.  **Sertifikaları Hazırla** butonuna basarak sertifikaları oluşturun.
5.  Sertifikalar oluşturulduktan sonra **Mailleri Gönder** butonu aktif olacaktır.

## Dosya Yapısı

*   `app/gui.py`: Uygulamanın grafik arayüzü.
*   `app/app.py`: Arka plan işlemleri (Sertifika oluşturma, Mail gönderme mantığı).
*   `requirements.txt`: Gerekli Python kütüphaneleri.

## Gereksinimler

*   Python 3.x
*   customtkinter
*   Pillow
