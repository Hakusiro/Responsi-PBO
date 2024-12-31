### Deskripsi Aplikasi
Aplikasi ini adalah sistem manajemen retail berbasis GUI (Graphical User Interface) yang menggunakan **Tkinter** dan **MySQL**. Aplikasi ini memungkinkan pengguna untuk mengelola produk serta mencatat transaksi penjualan produk. Pengguna dapat melakukan operasi CRUD (Create, Read, Update, Delete) untuk produk, serta mencatat transaksi yang terjadi dengan memilih produk dan jumlahnya. 

Aplikasi ini terdiri dari dua tab utama:
1. **Manajemen Produk**: Untuk menambahkan, memperbarui, dan menghapus produk yang ada di database.
2. **Transaksi**: Untuk mencatat transaksi penjualan dengan memilih produk dan jumlah yang dibeli, kemudian menghitung total harga berdasarkan harga produk dan jumlah yang dipilih.

### Cara Menjalankan Aplikasi
1. **Persiapkan Database:**
   - Pastikan **MySQL** sudah terinstal di sistem Anda.
   - Buat database dan tabel sesuai dengan skrip SQL yang disediakan:
     ```sql
     CREATE DATABASE IF NOT EXISTS retail_db;
     USE retail_db;

     CREATE TABLE IF NOT EXISTS produk (
         id_produk INT AUTO_INCREMENT PRIMARY KEY,
         nama_produk VARCHAR(255) NOT NULL,
         harga_produk DECIMAL(10, 2) NOT NULL
     );

     CREATE TABLE IF NOT EXISTS transaksi (
         id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
         id_produk INT NOT NULL,
         jumlah_produk INT NOT NULL,
         total_harga DECIMAL(10, 2) NOT NULL,
         tanggal_transaksi DATE NOT NULL,
         CONSTRAINT fk_produk FOREIGN KEY (id_produk)
             REFERENCES produk (id_produk)
             ON DELETE CASCADE
     );
     ```
2. **Konfigurasi Koneksi Database:**
   - Pastikan koneksi ke database diatur dengan benar di dalam kode Python, dengan mengganti parameter koneksi jika diperlukan, seperti password MySQL pada fungsi `connect_db`.
3. **Jalankan Aplikasi:**
   - Jalankan script Python menggunakan **Python 3.x** yang telah terpasang di sistem Anda.
   - Aplikasi akan membuka jendela GUI menggunakan Tkinter, dan Anda bisa mulai menggunakan aplikasi untuk mengelola produk dan transaksi.

### Struktur Tabel Database
Aplikasi ini menggunakan dua tabel utama dalam database **retail_db**:

1. **Tabel `produk`**: Menyimpan informasi produk yang tersedia di toko.
   - `id_produk`: ID unik untuk setiap produk (Primary Key).
   - `nama_produk`: Nama produk.
   - `harga_produk`: Harga produk.

   **Contoh Struktur Tabel**:
   ```sql
   CREATE TABLE IF NOT EXISTS produk (
       id_produk INT AUTO_INCREMENT PRIMARY KEY,
       nama_produk VARCHAR(255) NOT NULL,
       harga_produk DECIMAL(10, 2) NOT NULL
   );
   ```

2. **Tabel `transaksi`**: Menyimpan informasi transaksi yang terjadi ketika produk dijual.
   - `id_transaksi`: ID unik untuk setiap transaksi (Primary Key).
   - `id_produk`: ID produk yang terlibat dalam transaksi (Foreign Key dari `produk`).
   - `jumlah_produk`: Jumlah produk yang dibeli.
   - `total_harga`: Total harga transaksi, dihitung berdasarkan harga produk dan jumlah yang dibeli.
   - `tanggal_transaksi`: Tanggal transaksi terjadi.

   **Contoh Struktur Tabel**:
   ```sql
   CREATE TABLE IF NOT EXISTS transaksi (
       id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
       id_produk INT NOT NULL,
       jumlah_produk INT NOT NULL,
       total_harga DECIMAL(10, 2) NOT NULL,
       tanggal_transaksi DATE NOT NULL,
       CONSTRAINT fk_produk FOREIGN KEY (id_produk)
           REFERENCES produk (id_produk)
           ON DELETE CASCADE
   );
   ```

### Alur Kerja Aplikasi:
1. **Manajemen Produk**:
   - Menambah produk baru dengan memasukkan nama dan harga produk.
   - Memperbarui informasi produk yang sudah ada berdasarkan ID produk.
   - Menghapus produk berdasarkan ID produk.
   
2. **Transaksi**:
   - Menambahkan transaksi dengan memilih produk dan jumlah yang dibeli. Aplikasi akan menghitung total harga berdasarkan harga produk dan jumlah yang dimasukkan.
   - Menampilkan transaksi yang sudah tercatat, termasuk nama produk, jumlah yang dibeli, total harga, dan tanggal transaksi.
   - Menghapus transaksi berdasarkan ID transaksi.

Dengan antarmuka yang sederhana, aplikasi ini memungkinkan pengguna untuk dengan mudah mengelola data produk dan transaksi dalam bisnis retail.