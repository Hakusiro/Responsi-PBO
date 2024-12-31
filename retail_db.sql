-- Membuat database
CREATE DATABASE IF NOT EXISTS retail_db;
USE retail_db;

-- Membuat tabel produk
CREATE TABLE IF NOT EXISTS produk (
    id_produk INT AUTO_INCREMENT PRIMARY KEY,
    nama_produk VARCHAR(255) NOT NULL,
    harga_produk DECIMAL(10, 2) NOT NULL
);

-- Membuat tabel transaksi
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
