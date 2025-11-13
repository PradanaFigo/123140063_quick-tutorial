# Proyek Pyramid (Langkah 3: Konfigurasi .ini)

Ini adalah langkah ketiga dalam tutorial Pyramid, mengubah aplikasi dari file yang dijalankan manual menjadi aplikasi yang dijalankan secara profesional menggunakan `pserve` dan file konfigurasi `.ini`.

Proyek ini didasarkan pada [Quick Tutorial: Application Configuration](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/ini.html) dari dokumentasi resmi Pyramid.

## Tujuan

Tujuan dari proyek ini adalah untuk beralih ke cara standar menjalankan aplikasi Pyramid. Kita akan memisahkan konfigurasi (seperti port) ke dalam file `.ini` dan menggunakan `pserve` untuk melayani aplikasi, termasuk mengaktifkan *debug toolbar*.

## Persyaratan

* Python 3.6+
* `pip` dan `venv` (biasanya sudah termasuk dalam Python)

## Instalasi

1.  **Persiapan Proyek (Salin dari Langkah 2):**
    Pertama, salin seluruh proyek `package` Anda ke folder baru bernama `ini`.

    ```bash
    # Pastikan Anda di D:\Figo\projects\quick_tutorial
    cd D:\Figo\projects\quick_tutorial
    
    # Salin 'package' ke 'ini' (ini akan membuat folder 'ini')
    Copy-Item -Path package -Destination ini -Recurse
    ```
    Setelah itu, **edit file-file di dalam folder `ini`** sesuai tutorial:
    * **`setup.py`**: Tambahkan `pyramid_debugtoolbar` ke `requires` dan tambahkan `entry_points`.
    * **`tutorial/app.py`**: Hapus `if __name__ == '__main__'` dan buat fungsi `main()`.
    * **Buat File Baru**: Buat `development.ini` dan `production.ini` (gunakan konten yang sudah diperbaiki untuk menghindari error).

2.  **Buat Ulang dan Aktifkan Virtual Environment (PENTING):**
    `venv` tidak bisa disalin. Anda harus membuatnya ulang di dalam folder `ini`.

    ```bash
    # Pindah ke direktori 'ini' yang baru
    cd D:\Figo\projects\quick_tutorial\ini
    
    # HAPUS venv lama yang rusak (PENTING)
    Remove-Item -Path venv -Recurse -Force
    
    # Buat venv baru yang bersih
    python -m venv venv
    
    # Aktifkan venv (Windows PowerShell)
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instal Proyek dan Dependensi:**
    Perintah ini akan membaca `setup.py` Anda yang baru, menginstal `pyramid_debugtoolbar`, dan mendaftarkan `entry_points` Anda.

    ```bash
    # Pastikan (venv) aktif
    pip install -e .
    ```

## Menjalankan Aplikasi

1.  Pastikan *virtual environment* Anda aktif (prompt diawali dengan `(venv)`) dan Anda berada di direktori `D:\Figo\projects\quick_tutorial\ini`.

2.  Jalankan server menggunakan `pserve` dan file `.ini` (bukan `python tutorial/app.py`):
    ```powershell
    pserve development.ini --reload
    ```

3.  Server akan berjalan di `http://0.0.0.0:6543`.

## Cara Mengakses

Buka browser web Anda dan kunjungi alamat berikut:

[**http://localhost:6543/**](http://localhost:6543/)

Anda akan melihat pesan `Hello World!` dan **logo `</>` (Debug Toolbar)** di sisi kanan layar.

## Menghentikan Server

Untuk menghentikan server, kembali ke terminal tempat Anda menjalankan `pserve` dan tekan **Ctrl+C**.