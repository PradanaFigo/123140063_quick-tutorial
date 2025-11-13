# Proyek Pyramid (Langkah 4: Debug Toolbar)

Ini adalah langkah keempat dalam tutorial Pyramid. Kita akan menyempurnakan cara kita menginstal dan mengkonfigurasi `pyramid_debugtoolbar` menggunakan "extras" di `setup.py` dan `pyramid.includes` di file `.ini`.

Proyek ini didasarkan pada [Quick Tutorial: Easier Development with debugtoolbar](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/debugtoolbar.html) dari dokumentasi resmi Pyramid.

## Tujuan

Tujuan dari proyek ini adalah untuk beralih ke cara yang lebih bersih dan standar untuk mengelola dependensi pengembangan (seperti `debugtoolbar`) dan mengaktifkannya di konfigurasi `.ini` dengan lebih sederhana.

## Persyaratan

* Python 3.6+
* `pip` dan `venv` (biasanya sudah termasuk dalam Python)

## Instalasi

1.  **Persiapan Proyek (Salin dari Langkah 3):**
    Pertama, salin seluruh proyek `ini` Anda ke folder baru bernama `debugtoolbar`.

    ```bash
    # Pastikan Anda di D:\Figo\projects\quick_tutorial
    cd D:\Figo\projects\quick_tutorial
    
    # Salin 'ini' ke 'debugtoolbar' (ini akan membuat folder 'debugtoolbar')
    Copy-Item -Path ini -Destination debugtoolbar -Recurse
    ```
    Setelah itu, **edit file-file di dalam folder `debugtoolbar`** sesuai tutorial:
    * **`setup.py`**: Pindahkan `pyramid_debugtoolbar` dari `requires` ke `extras_require` baru di bawah kunci `[dev]`.
    * **`development.ini`**: Hapus semua konten lama dan ganti dengan konfigurasi `pyramid.includes` yang baru dan lebih sederhana.
    * **`production.ini`**: Lakukan hal yang sama, tetapi tanpa `pyramid.includes`.

2.  **Buat Ulang dan Aktifkan Virtual Environment (PENTING):**
    `venv` tidak bisa disalin. Anda harus membuatnya ulang di dalam folder `debugtoolbar`.

    ```bash
    # Pindah ke direktori 'debugtoolbar' yang baru
    cd D:\Figo\projects\quick_tutorial\debugtoolbar
    
    # HAPUS venv lama yang rusak (PENTING)
    Remove-Item -Path venv -Recurse -Force
    
    # Buat venv baru yang bersih
    python -m venv venv
    
    # Aktifkan venv (Windows PowerShell)
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instal Proyek dan Dependensi (Cara Baru):**
    Perintah ini akan membaca `setup.py` Anda dan menginstal dependensi "dev" (yaitu `debugtoolbar`) karena Anda menyertakan `".[dev]"`.

    ```bash
    # Pastikan (venv) aktif
    pip install -e ".[dev]"
    ```

## Menjalankan Aplikasi

1.  Pastikan *virtual environment* Anda aktif (prompt diawali dengan `(venv)`) dan Anda berada di direktori `D:\Figo\projects\quick_tutorial\debugtoolbar`.

2.  Jalankan server menggunakan `pserve` (perintahnya sama, tetapi konfigurasinya berbeda):
    ```powershell
    pserve development.ini --reload
    ```

3.  Server akan berjalan di `http://0.0.0.0:6543`.

## Cara Mengakses

Buka browser web Anda dan kunjungi alamat berikut:

[**http://localhost:6543/**](http://localhost:6543/)

Anda akan melihat pesan `Hello World!` dan **logo `</>` (Debug Toolbar)** di sisi kanan layar.

## Tugas Tambahan (Extra Credit)

Tutorial ini menyarankan Anda untuk sengaja membuat error di `tutorial/app.py` (misalnya, mengubah `Response` menjadi `xResponse`). Lakukan ini dan simpan file-nya. Saat Anda me-refresh browser, Anda akan melihat halaman error interaktif yang sangat membantu dari `debugtoolbar`.

## Menghentikan Server

Untuk menghentikan server, kembali ke terminal tempat Anda menjalankan `pserve` dan tekan **Ctrl+C**.