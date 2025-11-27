import json
import os
from datetime import datetime

FILE_DATA = "data.json"  # Nama file untuk menyimpan data pasien
FILE_RIWAYAT = "riwayat.json"  # Nama file untuk menyimpan riwayat pasien

DAFTAR_POLI = ["Umum", "Gigi", "Anak", "THT", "Mata"]  # Daftar poli yang tersedia

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')  # Membersihkan layar terminal

def muat_file(nama_file):
    try:
        with open(nama_file, "r") as file:
            return json.load(file)  # Membaca data dari file JSON
    except:
        return []  # Jika file tidak ditemukan atau error, kembalikan list kosong

def simpan_file(nama_file, data):
    with open(nama_file, "w") as file:
        json.dump(data, file, indent=4)  # Menyimpan data ke file JSON

def buat_nomor_antrian(poli, data):
    kode = poli[0].upper()  # Mengambil huruf pertama dari nama poli
    jumlah = sum(1 for x in data if x["poli"] == poli)  # Menghitung jumlah pasien di poli tersebut
    return f"{kode}-{jumlah + 1:02d}"  # Membuat nomor antrian dengan format KODE-XX

def tambah_pasien():
    bersihkan_layar()
    print("=== Tambah Pasien ===")
    nama = input("Nama Pasien: ")
    umur = input("Umur Pasien: ")

    print("\nPilih Poli:")
    for i, poli in enumerate(DAFTAR_POLI, 1):
        print(f"{i}. {poli}")
    try:
        pilihan = int(input("Masukkan pilihan: "))
        poli = DAFTAR_POLI[pilihan - 1]
    except:
        print("Pilihan tidak valid!")
        input("Tekan ENTER...")
        return

    keluhan = input("Keluhan Pasien: ")

    data = muat_file(FILE_DATA)
    nomor_antrian = buat_nomor_antrian(poli, data)

    pasien = {
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Tanggal dan waktu saat ini
        "nama": nama,
        "umur": umur,
        "poli": poli,
        "keluhan": keluhan,
        "nomor_antrian": nomor_antrian
    }

    data.append(pasien)  # Menambahkan data pasien ke daftar
    simpan_file(FILE_DATA, data)  # Menyimpan data ke file

    print("\nData berhasil ditambahkan!")
    input("Tekan ENTER...")
    bersihkan_layar()

def lihat_data():
    bersihkan_layar()
    print("=== Semua Data Pasien ===")
    data = muat_file(FILE_DATA)
    if not data:
        print("Belum ada data.")
    else:
        for d in data:
            print(f"{d['nomor_antrian']} | {d['nama']} | {d['umur']} | {d['poli']} | {d['keluhan']} | {d['tanggal']}")
    input("\nTekan ENTER...")
    bersihkan_layar()

def perbarui_pasien():
    bersihkan_layar()
    print("=== Update Data Pasien ===")
    data = muat_file(FILE_DATA)
    lihat_data()

    nomor_antrian = input("Masukkan nomor antrian yang ingin diupdate: ")
    for d in data:
        if d["nomor_antrian"] == nomor_antrian:
            d["nama"] = input("Nama baru: ")
            d["umur"] = input("Umur baru: ")
            d["keluhan"] = input("Keluhan baru: ")
            simpan_file(FILE_DATA, data)
            print("Data berhasil diperbarui!")
            input("ENTER...")
            bersihkan_layar()
            return

    print("Nomor antrian tidak ditemukan!")
    input("ENTER...")
    bersihkan_layar()

def hapus_pasien():
    bersihkan_layar()
    print("=== Hapus Data Pasien ===")
    data = muat_file(FILE_DATA)
    lihat_data()

    nomor_antrian = input("Masukkan nomor antrian yang ingin dihapus: ")
    for d in data:
        if d["nomor_antrian"] == nomor_antrian:
            data.remove(d)  # Menghapus data pasien dari daftar
            simpan_file(FILE_DATA, data)  # Menyimpan perubahan ke file
            print("Data berhasil dihapus!")
            input("ENTER...")
            bersihkan_layar()
            return

    print("Nomor tidak ditemukan!")
    input("ENTER...")
    bersihkan_layar()

def panggil_pasien():
    bersihkan_layar()
    print("=== Panggil Pasien Per Poli ===")

    print("\nPilih Poli:")
    for i, poli in enumerate(DAFTAR_POLI, 1):
        print(f"{i}. {poli}")
    try:
        pilihan = int(input("Masukkan pilihan: "))
        poli = DAFTAR_POLI[pilihan - 1]
    except:
        print("Pilihan tidak valid!")
        input("ENTER...")
        return

    data = muat_file(FILE_DATA)
    antrian_poli = [d for d in data if d["poli"] == poli]  # Filter pasien berdasarkan poli

    if not antrian_poli:
        print("Tidak ada pasien dalam antrian poli ini.")
        input("ENTER...")
        bersihkan_layar()
        return

    pasien = antrian_poli[0]  # Mengambil pasien pertama dalam antrian
    print(f"\nMemanggil: {pasien['nomor_antrian']} | {pasien['nama']}")

    riwayat = muat_file(FILE_RIWAYAT)
    riwayat.append(pasien)  # Menambahkan pasien ke riwayat
    simpan_file(FILE_RIWAYAT, riwayat)

    data.remove(pasien)  # Menghapus pasien dari antrian
    simpan_file(FILE_DATA, data)

    input("ENTER...")
    bersihkan_layar()

# =========================
#     FITUR BARU: SEARCH
# =========================
def cari_pasien():
    bersihkan_layar()
    print("=== Cari Pasien ===")
    print("1. Berdasarkan Nama")
    print("2. Berdasarkan Nomor Antrian")
    print("3. Berdasarkan Poli")

    pilih = input("Masukkan pilihan: ")

    data = muat_file(FILE_DATA)

    if pilih == "1":
        keyword = input("Masukkan nama: ").lower()
        hasil = [d for d in data if keyword in d["nama"].lower()]

    elif pilih == "2":
        keyword = input("Masukkan nomor antrian: ").upper()
        hasil = [d for d in data if d["nomor_antrian"] == keyword]

    elif pilih == "3":
        print("\nPilih Poli:")
        for i, poli in enumerate(DAFTAR_POLI, 1):
            print(f"{i}. {poli}")
        try:
            p = int(input("Masukkan pilihan: "))
            poli = DAFTAR_POLI[p - 1]
        except:
            print("Pilihan tidak valid!")
            input("ENTER...")
            return
        hasil = [d for d in data if d["poli"] == poli]

    else:
        print("Pilihan tidak valid!")
        input("ENTER...")
        bersihkan_layar()
        return

    print("\n=== Hasil Pencarian ===")
    if not hasil:
        print("Tidak ditemukan.")
    else:
        for d in hasil:
            print(f"{d['nomor_antrian']} | {d['nama']} | {d['umur']} | {d['poli']} | {d['keluhan']} | {d['tanggal']}")

    input("ENTER...")
    bersihkan_layar()

# =========================
#     FITUR BARU: SORTING
# =========================
def urutkan_data():
    bersihkan_layar()
    print("=== Urutkan Data Pasien ===")
    print("1. Berdasarkan Nama")
    print("2. Berdasarkan Umur")
    print("3. Berdasarkan Poli")
    print("4. Berdasarkan Tanggal Input")

    pilih = input("Masukkan pilihan: ")

    data = muat_file(FILE_DATA)

    if not data:
        print("Tidak ada data untuk diurutkan.")
        input("ENTER...")
        bersihkan_layar()
        return

    # ==== BUBBLE SORT 
    def bubble_sort(arr, key):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                # ---------------------------------------------------
                # Penentu nilai perbandingan berdasarkan kategori
                # ---------------------------------------------------
                if key == "nama":
                    a = arr[j]["nama"].lower()
                    b = arr[j+1]["nama"].lower()
                elif key == "umur":
                    a = int(arr[j]["umur"])
                    b = int(arr[j+1]["umur"])
                elif key == "poli":
                    a = arr[j]["poli"]
                    b = arr[j+1]["poli"]
                elif key == "tanggal":
                    a = arr[j]["tanggal"]
                    b = arr[j+1]["tanggal"]
                else:
                    return arr

                if a > b:
                    arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap
        return arr

    # ---------------------------------------------------
    # Menentukan kategori sorting
    # ---------------------------------------------------
    if pilih == "1":
        hasil = bubble_sort(data, "nama")
    elif pilih == "2":
        hasil = bubble_sort(data, "umur")
    elif pilih == "3":
        hasil = bubble_sort(data, "poli")
    elif pilih == "4":
        hasil = bubble_sort(data, "tanggal")
    else:
        print("Pilihan tidak valid!")
        input("ENTER...")
        bersihkan_layar()
        return

    print("\n=== Hasil Sorting ===")
    for d in hasil:
        print(f"{d['nomor_antrian']} | {d['nama']} | {d['umur']} | {d['poli']} | {d['keluhan']} | {d['tanggal']}")

    input("ENTER...")
    bersihkan_layar()


def menu():
    while True:
        print("=== Sistem Antrian Rumah Sakit ===")
        print("1. Tambah Pasien")
        print("2. Lihat Data")
        print("3. Update Data")
        print("4. Hapus Data")
        print("5. Panggil (Per Poli)")
        print("6. Cari Pasien")
        print("7. Urutkan Data")
        print("8. Keluar")

        pilihan = input("Masukkan pilihan: ")

        if pilihan == "1":
            tambah_pasien()
        elif pilihan == "2":
            lihat_data()
        elif pilihan == "3":
            perbarui_pasien()
        elif pilihan == "4":
            hapus_pasien()
        elif pilihan == "5":
            panggil_pasien()
        elif pilihan == "6":
            cari_pasien()
        elif pilihan == "7":
            urutkan_data()
        elif pilihan == "8":
            bersihkan_layar()
            break
        else:
            print("Pilihan tidak valid!")
            input("ENTER...")
            bersihkan_layar()

menu()
