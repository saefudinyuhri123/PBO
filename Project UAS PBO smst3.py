import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QDateTimeEdit, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QGroupBox, QFormLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
import sqlite3

class ParkirApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(600, 400))
        self.setWindowTitle("Aplikasi Parkir")

        background_label = QLabel(self)
        pixmap = QPixmap("background_image.jpg")
        background_label.setPixmap(pixmap)

        dashboard_group = QGroupBox("Dashboard")
        dashboard_layout = QFormLayout()

        self.label_data = QLabel("Data dari Database: ")
        dashboard_layout.addRow("Data:", self.label_data)

        self.input_plat = QLineEdit()
        dashboard_layout.addRow("Plat Kendaraan:", self.input_plat)

        self.input_jenis = QLineEdit()
        dashboard_layout.addRow("Jenis Kendaraan:", self.input_jenis)

        self.input_jam_masuk = QDateTimeEdit(self)
        self.input_jam_masuk.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        dashboard_layout.addRow("Jam Masuk:", self.input_jam_masuk)

        self.input_jam_keluar = QDateTimeEdit(self)
        self.input_jam_keluar.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        dashboard_layout.addRow("Jam Keluar:", self.input_jam_keluar)

        btn_simpan = QPushButton("Simpan Data")
        btn_simpan.clicked.connect(self.simpan_data)
        dashboard_layout.addRow("", btn_simpan)

        btn_hapus = QPushButton("Hapus Data")
        btn_hapus.clicked.connect(self.hapus_data)
        dashboard_layout.addRow("", btn_hapus)

        dashboard_group.setLayout(dashboard_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(background_label)
        layout.addWidget(dashboard_group)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.label_total_harga = QLabel("Total Harga: 0")
        layout.addWidget(self.label_total_harga)

        self.conn = sqlite3.connect("data_parkir.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_parkir (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plat_kendaraan TEXT,
                jenis_kendaraan TEXT,
                jam_masuk TEXT,
                jam_keluar TEXT,
                harga INTEGER
            )
        ''')

    def simpan_data(self):
        plat_kendaraan = self.input_plat.text()
        jenis_kendaraan = self.input_jenis.text()
        jam_masuk = self.input_jam_masuk.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        jam_keluar = self.input_jam_keluar.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        harga = self.hitung_total_biaya()

        self.cursor.execute("INSERT INTO data_parkir (plat_kendaraan, jenis_kendaraan, jam_masuk, jam_keluar, harga) VALUES (?, ?, ?, ?, ?)",
                            (plat_kendaraan, jenis_kendaraan, jam_masuk, jam_keluar, harga))
        self.conn.commit()

        self.tampilkan_data()
        self.tampilkan_total_harga()

    def hapus_data(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            plat_kendaraan = selected_item.text().split(",")[0].split(":")[1].strip()
            self.cursor.execute("DELETE FROM data_parkir WHERE plat_kendaraan=?", (plat_kendaraan,))
            self.conn.commit()
            self.tampilkan_data()
            self.tampilkan_total_harga()

    def hitung_total_biaya(self):
        return 5000

    def tampilkan_data(self):
        self.cursor.execute("SELECT * FROM data_parkir")
        data = self.cursor.fetchall()

        self.list_widget.clear()

        for row in data:
            item = QListWidgetItem(f"Plat: {row[1]}, Jenis: {row[2]}, Masuk: {row[3]}, Keluar: {row[4]}, Harga: {row[5]}")
            self.list_widget.addItem(item)

    def tampilkan_total_harga(self):
        self.cursor.execute("SELECT SUM(harga) FROM data_parkir")
        total_harga = self.cursor.fetchone()[0]

        self.label_total_harga.setText(f"Total Harga: {total_harga}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkirApp()
    window.show()
    sys.exit(app.exec_())