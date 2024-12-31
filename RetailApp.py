import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

# Koneksi ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Sesuaikan password
        database="retail_db"
    )

# Fungsi CRUD Produk
def add_product(name, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produk (nama_produk, harga_produk) VALUES (%s, %s)", (name, price))
    conn.commit()
    conn.close()

def get_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk")
    products = cursor.fetchall()
    conn.close()
    return products

def update_product(product_id, name, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE produk SET nama_produk=%s, harga_produk=%s WHERE id_produk=%s", (name, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produk WHERE id_produk=%s", (product_id,))
    conn.commit()
    conn.close()

# Fungsi Transaksi
def add_transaction(product_id, quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT harga_produk FROM produk WHERE id_produk=%s", (product_id,))
    price = cursor.fetchone()[0]
    total_price = price * quantity
    today = date.today()
    cursor.execute(
        "INSERT INTO transaksi (id_produk, jumlah_produk, total_harga, tanggal_transaksi) VALUES (%s, %s, %s, %s)",
        (product_id, quantity, total_price, today)
    )
    conn.commit()
    conn.close()
    return total_price

def get_transactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transaksi.id_transaksi, produk.nama_produk, transaksi.jumlah_produk, transaksi.total_harga, transaksi.tanggal_transaksi
        FROM transaksi
        JOIN produk ON transaksi.id_produk = produk.id_produk
    """)
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def delete_transaction(transaksi_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transaksi WHERE id_transaksi=%s", (transaksi_id,))
    conn.commit()
    conn.close()

# GUI Utama
class RetailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Management App")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Tab Control
        tab_control = ttk.Notebook(root)

        self.product_tab = ttk.Frame(tab_control)
        self.transaction_tab = ttk.Frame(tab_control)

        tab_control.add(self.product_tab, text="Manajemen Produk")
        tab_control.add(self.transaction_tab, text="Transaksi")

        tab_control.pack(expand=1, fill="both")
        
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#e0f7fa")  # Warna latar belakang tab
        style.configure("Custom.TButton", background="#00838f", foreground="black")
        style.configure("Custom.TLabel", background="#e0f7fa", foreground="#004d40")

        # Inisialisasi dropdown sebelum load_products dipanggil
        self.product_dropdown = None

        self.setup_transaction_tab()
        self.setup_product_tab()

    def setup_product_tab(self):
        self.product_tab.columnconfigure(1, weight=1)
        self.product_tab.rowconfigure(4, weight=1)

        # Widgets for Product Tab
        ttk.Label(self.product_tab, text="ID Produk:", style="Custom.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.product_id = ttk.Entry(self.product_tab)
        self.product_id.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self.product_tab, text="Nama Produk:", style="Custom.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.product_name = ttk.Entry(self.product_tab)
        self.product_name.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self.product_tab, text="Harga Produk:", style="Custom.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.product_price = ttk.Entry(self.product_tab)
        self.product_price.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(self.product_tab, text="Tambah Produk", style="Custom.TButton", command=self.add_product).grid(row=3, column=0, pady=10)
        ttk.Button(self.product_tab, text="Update Produk", style="Custom.TButton", command=self.update_product).grid(row=3, column=1, pady=10)
        ttk.Button(self.product_tab, text="Hapus Produk", style="Custom.TButton", command=self.delete_product).grid(row=3, column=2, pady=10)

        self.product_table = ttk.Treeview(self.product_tab, columns=("ID", "Nama", "Harga"), show="headings")
        self.product_table.heading("ID", text="ID")
        self.product_table.heading("Nama", text="Nama Produk")
        self.product_table.heading("Harga", text="Harga Produk")
        self.product_table.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.load_products()

    def setup_transaction_tab(self):
        self.transaction_tab.columnconfigure(1, weight=1)
        self.transaction_tab.rowconfigure(3, weight=1)
        # Widgets for Transaction Tab
        ttk.Label(self.transaction_tab, text="ID Transaksi:", style="Custom.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.transaksi_id = ttk.Entry(self.transaction_tab)
        self.transaksi_id.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.transaction_tab, text="Produk:", style="Custom.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.product_dropdown = ttk.Combobox(self.transaction_tab)  # Inisialisasi dropdown
        self.product_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self.transaction_tab, text="Jumlah:", style="Custom.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.product_quantity = ttk.Entry(self.transaction_tab)
        self.product_quantity.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(self.transaction_tab, text="Tambah Transaksi", style="Custom.TButton", command=self.add_transaction).grid(row=3, column=0, pady=10)
        ttk.Button(self.transaction_tab, text="Hapus Transaksi", style="Custom.TButton", command=self.delete_transaction).grid(row=3, column=2, pady=10)

        self.transaction_table = ttk.Treeview(self.transaction_tab, columns=("ID", "Produk", "Jumlah", "Total", "Tanggal"), show="headings")
        self.transaction_table.heading("ID", text="ID")
        self.transaction_table.heading("Produk", text="Produk")
        self.transaction_table.heading("Jumlah", text="Jumlah")
        self.transaction_table.heading("Total", text="Total Harga")
        self.transaction_table.heading("Tanggal", text="Tanggal")
        self.transaction_table.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.load_transactions()

    def add_product(self):
        name = self.product_name.get()
        price = self.product_price.get()
        if name and price:
            try:
                add_product(name, float(price))
                messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Salah", "Harap isi semua kolom.")

    def update_product(self):
        product_id = self.product_id.get()
        name = self.product_name.get()
        price = self.product_price.get()
        if product_id and name and price:
            try:
                update_product(int(product_id), name, float(price))
                messagebox.showinfo("Sukses", "Produk berhasil diperbarui!")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Salah", "Harap isi semua kolom.")

    def delete_product(self):
        product_id = self.product_id.get()
        if product_id:
            try:
                delete_product(int(product_id))
                messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Salah", "Harap masukkan ID produk.")

    def load_products(self):
        for row in self.product_table.get_children():
            self.product_table.delete(row)
        products = get_products()
        for product in products:
            self.product_table.insert("", "end", values=product)
        self.product_dropdown['values'] = [f"{p[1]} (ID: {p[0]})" for p in products]

    def add_transaction(self):
        product = self.product_dropdown.get()
        quantity = self.product_quantity.get()
        
        if not product:
            messagebox.showwarning("Input Salah", "Harap pilih produk terlebih dahulu.")
            return

        if not quantity:
            messagebox.showwarning("Input Salah", "Harap isi jumlah produk.")
            return

        # Validate if quantity is a positive integer
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Jumlah produk harus lebih besar dari 0.")
        except ValueError as e:
            messagebox.showwarning("Input Salah", f"Jumlah produk tidak valid: {e}")
            return

        try:
            # Extract product ID from the dropdown
            product_id = int(product.split("ID: ")[1].replace(")", ""))
            
            # Add transaction
            total_price = add_transaction(product_id, quantity)
            messagebox.showinfo("Sukses", f"Transaksi berhasil! Total Harga: {total_price}")
            self.load_transactions()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")


    def load_transactions(self):
        for row in self.transaction_table.get_children():
            self.transaction_table.delete(row)
        transactions = get_transactions()
        for transaction in transactions:
            self.transaction_table.insert("", "end", values=transaction)
    
    def delete_transaction(self):
        transaksi_id = self.transaksi_id.get()
        if transaksi_id:
            try:
                delete_transaction(int(transaksi_id))
                messagebox.showinfo("Sukses", "Transaksi berhasil dihapus!")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Salah", "Harap masukkan ID Transaksi.")

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = RetailApp(root)
    root.mainloop()
