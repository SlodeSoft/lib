import datetime
import smtplib
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl


class SEND_MAIL:
    def __init__(self, email, token, root_url):
        self.email = email
        self.token = token
        self.root_url = root_url

    def send(self):
        server = smtplib.SMTP()
        # server.set_debuglevel(1) # Décommenter pour activer le debug
        server.connect('smtp.exemple.com', 25)
        # (220, 'toto ESMTP Postfix') # Réponse du serveur
        server.ehlo()
        # (250, 'toto\nPIPELINING\nSIZE 10240000\nVRFY\nETRN\nSTARTTLS\nENHANCEDSTATUSCODES\n8BITMIME\nDSN') # Réponse du serveur
        # server.starttls()
        # On appelle la fonction STARTTLS
        # (220, '2.0.0 Ready to start TLS') # Réponse du serveur
        # (250, 'toto\nPIPELINING\nSIZE 10240000\nVRFY\nETRN\nSTARTTLS\nENHANCEDSTATUSCODES\n8BITMIME\nDSN') # Réponse du serveur
        fromaddr = 'VIAPASS ADMIN !!! RESET PASSWORD !!! <dcptools@viapass-xpress.com>'
        toaddrs = [self.email]  # On peut mettre autant d'adresses que l'on souhaite
        html = f"<!DOCTYPE html><html lang='en'><head></head><body>" \
               f"<br>VIAPASS Environment ADMIN - RESET PASSWORD :" \
               f"<br><br>Click Here To Reset Your Password :" \
               f"<a href='{self.root_url}/reset_password?userid={self.email}&token={self.token}' >" \
               f"<input type='button' value='Reset Password'></a>" \
               f"<br><br>HEURE = {datetime.datetime.now()}" \
               f"</body></html>"
        sujet = "[RESET YOU PASSWORD FOR VIAPASS Environment ADMIN]"
        msg2 = MIMEMultipart('alternative')
        msg2['Subject'] = sujet
        msg2['From'] = fromaddr
        msg2['To'] = ','.join(toaddrs)
        msg2["Date"] = formatdate(localtime=True)

        # part = MIMEText(html, 'html')
        part = MIMEText(html, 'html')
        msg2.attach(part)
        try:
            server.sendmail(fromaddr, toaddrs, msg2.as_string())
        except smtplib.SMTPException as e:
            print("SMTP ERROR = {}".format(e))
        except ssl.SSLError as e2:
            print("SSL ERROR = {}".format(e2))
        except ssl.SSLSocket as e3:
            print("SSL ERROR = {}".format(e3))
        except ssl.SSL_ERROR_SSL as e4:
            print("SSL ERROR = {}".format(e4))
        # {} # Réponse du serveur
        server.quit()
        # (221, '2.0.0 Bye') # Réponse du serveur
        # MET A JOUR LA VALEUR DU SERVICE DANS LA BDD CDS-FULLBIM
