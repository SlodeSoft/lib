from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class wa:
    def __init__(self):
        # Chemin vers le fichier exécutable du navigateur Chrome
        self.PATH = 'C:\\Users\\fab_r\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver_win32\\chromedriver.exe'  # Remplacez par le chemin approprié pour votre système d'exploitation
        # Nom de l'utilisateur ou du groupe WhatsApp auquel vous souhaitez envoyer le message
        self.recipient = 'Charles Tyrwhitt'
        # Message que vous souhaitez envoyer
        self.message = 'TEST !'
        # Options du navigateur
        self.options = Options()
        self.options.add_argument('--user-data-dir=C:\\Users\\fab_r\\AppData\\Local\\Google\\Chrome\\Application\\ProfilWhatsApp')  # Chemin vers votre profil WhatsApp (pour éviter la connexion à chaque exécution)
        self.options.add_argument('--disable-dev-shm-usage')
        #self.options.add_argument('--headless')
        #self.options.add_argument('--no-sandbox')

    def send_message(self):
        # Démarrer le navigateur Chrome
        driver = webdriver.Chrome(service=Service(self.PATH), options=self.options)
        driver.get('https://web.whatsapp.com/')

        # Attendre que l'utilisateur se connecte manuellement en scannant le code QR
        input('Appuyez sur Entrée après avoir scanné le code QR et vous être connecté à WhatsApp...')

        # Recherche du champ de recherche
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(self.recipient)
        time.sleep(2)  # Attendre que la liste des contacts se mette à jour
        search_box.send_keys(Keys.ENTER)

        # Attendre que la conversation se charge
        time.sleep(5)

        # Recherche de la zone de saisie du message
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.click()

        # Saisir le message et l'envoyer
        message_box.send_keys(self.message)
        message_box.send_keys(Keys.ENTER)

        # Attendre quelques secondes pour que le message soit envoyé
        time.sleep(5)

        # Fermer le navigateur
        #driver.quit()

        return "Le message a été envoyé avec succès !"


if __name__ == "__main__":
    a = wa()
    print(a.send_message())
