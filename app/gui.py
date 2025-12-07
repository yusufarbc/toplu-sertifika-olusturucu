import customtkinter
from tkinter import filedialog, messagebox
import threading
import os
from app import CertificateManager

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sertifika ve Mail Gönderim Aracı")
        self.geometry("900x750")
        
        self.manager = CertificateManager()
        self.csv_rows = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sekme görünümü
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.tab_main = self.tabview.add("Ana İşlemler")
        self.tab_settings = self.tabview.add("Ayarlar")
        self.tab_mail = self.tabview.add("Mail Ayarları")

        self.setup_main_tab()
        self.setup_settings_tab()
        self.setup_mail_tab()

        # Alt kısımdaki log alanı
        self.log_frame = customtkinter.CTkFrame(self)
        self.log_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)
        
        self.log_box = customtkinter.CTkTextbox(self.log_frame, height=150)
        self.log_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.log_box.insert("0.0", "Uygulama hazır.\n")
        self.log_box.configure(state="disabled")

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def setup_main_tab(self):
        self.tab_main.grid_columnconfigure(1, weight=1)

        # Dosya Seçimi - CSV
        self.label_csv = customtkinter.CTkLabel(self.tab_main, text="Katılımcı Listesi (.csv):")
        self.label_csv.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.entry_csv = customtkinter.CTkEntry(self.tab_main, placeholder_text="Dosya seçilmedi")
        self.entry_csv.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.btn_csv = customtkinter.CTkButton(self.tab_main, text="Seç", width=60, command=self.select_csv)
        self.btn_csv.grid(row=0, column=2, padx=10, pady=10)

        # Dosya Seçimi - Şablon
        self.label_template = customtkinter.CTkLabel(self.tab_main, text="Sertifika Şablonu (.png):")
        self.label_template.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.entry_template = customtkinter.CTkEntry(self.tab_main, placeholder_text="Dosya seçilmedi")
        self.entry_template.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry_template.insert(0, os.path.abspath(self.manager.template_path))
        
        self.btn_template = customtkinter.CTkButton(self.tab_main, text="Seç", width=60, command=self.select_template)
        self.btn_template.grid(row=1, column=2, padx=10, pady=10)

        # İşlem Butonları
        self.btn_create = customtkinter.CTkButton(self.tab_main, text="Sertifikaları Hazırla", command=self.start_creation_thread)
        self.btn_create.grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

        self.btn_send = customtkinter.CTkButton(self.tab_main, text="Mailleri Gönder", command=self.start_sending_thread, fg_color="green")
        self.btn_send.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    def setup_settings_tab(self):
        self.tab_settings.grid_columnconfigure(1, weight=1)

        # Çıktı Klasörü
        self.label_output = customtkinter.CTkLabel(self.tab_settings, text="Çıktı Klasörü:")
        self.label_output.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_output = customtkinter.CTkEntry(self.tab_settings)
        self.entry_output.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_output.insert(0, self.manager.output_dir)

        # Font Yolu
        self.label_font = customtkinter.CTkLabel(self.tab_settings, text="Font Dosyası (.ttf):")
        self.label_font.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_font = customtkinter.CTkEntry(self.tab_settings)
        self.entry_font.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry_font.insert(0, self.manager.font_path)

        # Font Boyutu
        self.label_size = customtkinter.CTkLabel(self.tab_settings, text="Font Boyutu:")
        self.label_size.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_size = customtkinter.CTkEntry(self.tab_settings)
        self.entry_size.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.entry_size.insert(0, str(self.manager.font_size))
        
        # Renk (RGB)
        self.label_color = customtkinter.CTkLabel(self.tab_settings, text="Yazı Rengi (R,G,B):")
        self.label_color.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_color = customtkinter.CTkEntry(self.tab_settings)
        self.entry_color.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.entry_color.insert(0, "28, 48, 85")

        self.btn_save_settings = customtkinter.CTkButton(self.tab_settings, text="Ayarları Kaydet", command=self.save_settings)
        self.btn_save_settings.grid(row=4, column=0, columnspan=3, padx=10, pady=20)

    def setup_mail_tab(self):
        self.tab_mail.grid_columnconfigure(1, weight=1)

        # SMTP Sunucusu
        self.label_smtp_server = customtkinter.CTkLabel(self.tab_mail, text="SMTP Sunucusu:")
        self.label_smtp_server.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_smtp_server = customtkinter.CTkEntry(self.tab_mail)
        self.entry_smtp_server.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_smtp_server.insert(0, "smtp.office365.com")

        # Port
        self.label_port = customtkinter.CTkLabel(self.tab_mail, text="Port:")
        self.label_port.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_port = customtkinter.CTkEntry(self.tab_mail)
        self.entry_port.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry_port.insert(0, "587")
        
        # Kullanıcı Adı
        self.label_user = customtkinter.CTkLabel(self.tab_mail, text="E-posta Adresi:")
        self.label_user.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_user = customtkinter.CTkEntry(self.tab_mail)
        self.entry_user.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Şifre
        self.label_pass = customtkinter.CTkLabel(self.tab_mail, text="Şifre:")
        self.label_pass.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_pass = customtkinter.CTkEntry(self.tab_mail, show="*")
        self.entry_pass.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        # Konu
        self.label_subject = customtkinter.CTkLabel(self.tab_mail, text="Konu:")
        self.label_subject.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.entry_subject = customtkinter.CTkEntry(self.tab_mail)
        self.entry_subject.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        self.entry_subject.insert(0, "Sertifikanız Hazır")

        # Mesaj
        self.label_msg = customtkinter.CTkLabel(self.tab_mail, text="Mesaj (HTML):")
        self.label_msg.grid(row=5, column=0, padx=10, pady=10, sticky="ne")
        self.entry_msg = customtkinter.CTkTextbox(self.tab_mail, height=100)
        self.entry_msg.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
        self.entry_msg.insert("0.0", "Etkinliğimize katıldığınız için teşekkür ederiz. Sertifikanız ektedir.")

    def select_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Dosyaları", "*.csv")])
        if file_path:
            self.entry_csv.delete(0, "end")
            self.entry_csv.insert(0, file_path)
            self.load_csv(file_path)

    def select_template(self):
        file_path = filedialog.askopenfilename(filetypes=[("Resim Dosyaları", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.entry_template.delete(0, "end")
            self.entry_template.insert(0, file_path)

    def load_csv(self, path):
        rows, error = self.manager.read_csv(path)
        if error:
            messagebox.showerror("Hata", f"CSV okunamadı: {error}")
            self.log(f"CSV okuma hatası: {error}")
        else:
            self.csv_rows = rows
            self.log(f"CSV başarıyla yüklendi. {len(rows)} kayıt bulundu.")

    def save_settings(self):
        try:
            self.manager.output_dir = self.entry_output.get()
            self.manager.font_path = self.entry_font.get()
            self.manager.font_size = int(self.entry_size.get())
            
            color_str = self.entry_color.get()
            self.manager.font_color = tuple(map(int, color_str.split(',')))
            
            messagebox.showinfo("Başarılı", "Görünüm ayarları güncellendi.")
            self.log("Ayarlar güncellendi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilirken hata: {str(e)}")

    def start_creation_thread(self):
        if not self.csv_rows:
            messagebox.showwarning("Uyarı", "Lütfen önce bir CSV dosyası seçin.")
            return

        self.btn_create.configure(state="disabled")
        threading.Thread(target=self.create_certificates).start()

    def create_certificates(self):
        self.log("----------------------------------------")
        self.log("Sertifika oluşturma işlemi başladı...")
        
        template_path = self.entry_template.get()
        if not os.path.exists(template_path):
            self.log("HATA: Şablon dosyası bulunamadı.")
            self.btn_create.configure(state="normal")
            return

        count = 0
        for row in self.csv_rows:
            # Satır 1: isim, Satır 2 vb. olabilir, orijinal koda göre varsayıyoruz
            if len(row) < 2:
                continue
            
            name = row[1].upper()
            img, error = self.manager.create_certificate(name, template_path)
            if error:
                self.log(f"HATA ({name}): Sertifika oluşturulamadı - {error}")
                continue
            
            path, error = self.manager.save_certificate(img, name)
            if error:
                self.log(f"HATA ({name}): Kaydedilemedi - {error}")
            else:
                self.log(f"BAŞARILI: {name} için sertifika oluşturuldu.")
                count += 1
        
        self.log(f"İşlem tamamlandı. Toplam {count} sertifika oluşturuldu.")
        self.log("----------------------------------------")
        self.btn_create.configure(state="normal")
        
    def start_sending_thread(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        smtp_server = self.entry_smtp_server.get()
        port = self.entry_port.get()

        if not username or not password:
            messagebox.showwarning("Uyarı", "Lütfen mail bilgilerini girin.")
            return
        
        if not smtp_server or not port:
            messagebox.showwarning("Uyarı", "Lütfen SMTP sunucu bilgilerini girin.")
            return

        if not self.csv_rows:
            messagebox.showwarning("Uyarı", "Lütfen önce katılımcı listesini yükleyin.")
            return

        if not messagebox.askyesno("Onay", f"{len(self.csv_rows)} kişiye mail gönderilecek. Emin misiniz?"):
            return

        self.btn_send.configure(state="disabled")
        threading.Thread(target=self.send_mails, args=(username, password, smtp_server, int(port))).start()

    def send_mails(self, username, password, smtp_server, port):
        self.log("----------------------------------------")
        self.log("Mail gönderme işlemi başladı...")
        
        credentials = {'username': username, 'password': password}
        subject = self.entry_subject.get()
        message_body = self.entry_msg.get("0.0", "end")
        
        count = 0
        for row in self.csv_rows:
            # row[1] isim, row[2] email olduğu varsayılıyor
            if len(row) < 3:
                continue
                
            name = row[1].upper()
            email = row[2]
            cert_path = os.path.join(self.manager.output_dir, f"{name}.png")
            
            if not os.path.exists(cert_path):
                self.log(f"ATLANDI ({name}): Sertifika dosyası bulunamadı.")
                continue
                
            mail_info = {
                'subject': subject,
                'message': message_body,
                'to': email
            }
            
            self.log(f"GÖNDERİLİYOR: {email}...")
            # Yeni SMTP parametrelerini buraya ekliyoruz
            success, error = self.manager.send_mail(credentials, mail_info, cert_path, smtp_server, port)
            
            if success:
                self.log(f"BAŞARILI: {email} adresine gönderildi.")
                count += 1
            else:
                self.log(f"HATA: {email} adresine gönderilemedi - {error}")
        
        self.log(f"İşlem tamamlandı. Toplam {count} mail gönderildi.")
        self.log("----------------------------------------")
        self.btn_send.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
