import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Buat koneksi socket client secara global untuk mempertahankan koneksi yang sama
client_socket = None

# Fungsi untuk menangani request ke server menggunakan koneksi yang sama
def send_request(request, output_widget):
    global client_socket
    if client_socket is None:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))  # Koneksi ke server dapur di port 8080

    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(4096).decode('utf-8')
    output_widget.insert(tk.END, response + '\n')

    if request == 'exit':
        client_socket.close()
        client_socket = None  # Set client_socket ke None saat koneksi ditutup

# GUI untuk Client (Pelanggan)
def client_gui():
    root = tk.Tk()
    root.title("Client Pelanggan")

    # Frame utama untuk membagi layout menjadi 2 bagian (kiri: menu, kanan: input/output)
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Bagian kiri untuk daftar menu
    left_frame = tk.Frame(main_frame, width=200)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Label Menu
    menu_label = tk.Label(left_frame, text="Daftar Menu:")
    menu_label.pack()

    # Bagian kanan untuk input pesanan dan output dari server
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    output_label = tk.Label(right_frame, text="Review Pesanan:")
    output_label.pack()

    output_widget = ScrolledText(right_frame, width=50, height=10)
    output_widget.pack()

    # Dictionary untuk menyimpan jumlah pesanan dari setiap item
    item_order_count = {}

    # Fungsi untuk memperbarui jumlah pesanan dan melakukan checkout
    def checkout_pesanan():
        for item, count in item_order_count.items():
            if count > 0:
                request = f"order,{item},{count}"
                send_request(request, output_widget)

    def keluar():
        send_request('exit', output_widget)
        root.quit()

    # Fungsi untuk menambah jumlah pesanan
    def tambah_pesanan(item, label):
        item_order_count[item] += 1
        label.config(text=str(item_order_count[item]))

    # Fungsi untuk mengurangi jumlah pesanan
    def kurangi_pesanan(item, label):
        if item_order_count[item] > 0:
            item_order_count[item] -= 1
        label.config(text=str(item_order_count[item]))

    # Fungsi untuk menampilkan pesanan yang telah dipilih
    def review_pesanan():
        output_widget.delete("1.0", tk.END)  # Clear output widget before showing the review
        output_widget.insert(tk.END, "Daftar Pesanan Anda:\n")
        for item, count in item_order_count.items():
            if count > 0:
                output_widget.insert(tk.END, f"{item}: {count} porsi\n")

    # Fungsi untuk mendapatkan dan menampilkan menu di kiri
    def tampilkan_menu():
        db_menu = []
        send_request('menu', output_widget)  # Jangan tampilkan hasil di output widget
        response = output_widget.get("1.0", tk.END).strip().split("\n")

        output_widget.delete("1.0", tk.END)  # Clear the output widget

        # Tampilkan menu dan buat tombol tambah/kurangi untuk setiap item
        for item in response:
            if item:
                item_name, item_price = item.split(': Rp')
                item_order_count[item_name] = 0  # Inisialisasi pesanan dengan 0

                item_frame = tk.Frame(left_frame)
                item_frame.pack(fill=tk.X)

                item_label = tk.Label(item_frame, text=f"{item_name}: Rp{item_price}")
                item_label.pack(side=tk.LEFT)

                kurang_button = tk.Button(item_frame, text="-", command=lambda i=item_name, l=None: kurangi_pesanan(i, l))
                kurang_button.pack(side=tk.LEFT)

                jumlah_label = tk.Label(item_frame, text="0", width=3)
                jumlah_label.pack(side=tk.LEFT)

                tambah_button = tk.Button(item_frame, text="+", command=lambda i=item_name, l=jumlah_label: tambah_pesanan(i, l))
                tambah_button.pack(side=tk.LEFT)

    # Otomatis ambil menu dari server saat aplikasi dimulai
    tampilkan_menu()

    # Tombol untuk melakukan checkout
    order_button = tk.Button(right_frame, text="Checkout Pesanan", command=checkout_pesanan)
    order_button.pack()

    # Tombol untuk mereview pesanan yang telah ditambahkan
    review_button = tk.Button(right_frame, text="Review Pesanan", command=review_pesanan)
    review_button.pack()

    exit_button = tk.Button(right_frame, text="Keluar", command=keluar)
    exit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    client_gui()
