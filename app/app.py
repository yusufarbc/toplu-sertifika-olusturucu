import csv
import os
import smtplib
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import Image, ImageDraw, ImageFont

class CertificateManager:
    def __init__(self):
        # Default configurations can be overwritten
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_path = os.path.join(base_dir, "PaytoneOne.ttf")
        self.font_size = 60
        self.font_color = (28, 48, 85)
        self.template_path = os.path.join(base_dir, "template.png")
        self.output_dir = os.path.join(base_dir, "certificates")
        
    def read_csv(self, file_path):
        """Reads the CSV file and returns a list of rows."""
        rows = []
        try:
            with open(file_path, encoding="utf-8") as csvfile:
                csvreader = csv.reader(csvfile, delimiter=",")
                for row in csvreader:
                    if row: # Skip empty lines
                        rows.append(row)
            return rows, None
        except Exception as e:
            return [], str(e)

    def create_certificate(self, name, template_path=None):
        """Creates a certificate image for a given name."""
        if template_path is None:
            template_path = self.template_path
            
        try:
            img = Image.open(template_path)
            draw = ImageDraw.Draw(img)
            
            # Load font
            font = ImageFont.truetype(self.font_path, self.font_size)
            
            # Calculate text position to center it
            # Using textbbox as textsize is deprecated in newer Pillow versions
            bbox = draw.textbbox((0, 0), name, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            img_width, img_height = img.size
            position = ((img_width - text_width) / 2, (img_height - text_height) / 2 - 60)
            
            draw.text(position, name, self.font_color, font=font)
            return img, None
        except Exception as e:
            return None, str(e)

    def save_certificate(self, img, name):
        """Saves the certificate image to disk."""
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
                
            path = os.path.join(self.output_dir, f"{name}.png")
            img.save(path)
            return path, None
        except Exception as e:
            return None, str(e)

    def send_mail(self, credentials, mail_info, attachment_path):
        """Sends a single email with attachment."""
        try:
            username = credentials['username']
            password = credentials['password']
            
            msg = MIMEMultipart()
            msg['Subject'] = mail_info['subject']
            msg['From'] = username
            msg['To'] = mail_info['to']

            msgText = MIMEText(mail_info['message'], 'html')
            msg.attach(msgText)

            with open(attachment_path, 'rb') as fp:
                img = MIMEImage(fp.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(img)

            # Using generic SMTP settings, specialized for Outlook/Office365 in this case but could be parameterized
            with smtplib.SMTP('smtp.office365.com', 587) as smtpObj:
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(username, password)
                smtpObj.sendmail(username, mail_info['to'], msg.as_string())
            
            return True, None
        except Exception as e:
            return False, str(e)
