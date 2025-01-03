import threading
import socket
import mysql.connector
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

# Koneksi ke MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Ganti dengan user database kamu
        password="",  # Ganti dengan password database kamu
        database="sigma_db"
    )

# Fungsi untuk menangani request dari client
def handle_client(client_socket, log_widget):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if request == 'exit':
                client_socket.close()
                break
            
            if not server_running:
                client_socket.send("192.168.110.214".encode('utf-8'))
                client_socket.close()
                break

            if request == 'menu':
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("SELECT nama, harga FROM menu")
                menu = cursor.fetchall()
                db.close()

                response = "\n".join([f"{item[0]}: Rp{item[1]}" for item in menu])
                client_socket.send(response.encode('utf-8'))
            
            elif request.startswith('order'):
                _, nama, quantity = request.split(',')
                quantity = int(quantity)

                db = connect_db()
                cursor = db.cursor()
                cursor.execute("SELECT harga FROM menu WHERE nama = %s", (nama,))
                result = cursor.fetchone()

                if result:
                    harga = result[0]
                    total_harga = harga * quantity

                    cursor.execute("INSERT INTO orders (nama, quantity, total_harga) VALUES (%s, %s, %s)", 
                                   (nama, quantity, total_harga))
                    db.commit()
                    db.close()

                    response = f"Pesanan untuk {quantity} {nama} diterima. Total: Rp.{total_harga:.2f}"
                else:
                    response = "Item tidak ditemukan."
                
                client_socket.send(response.encode('utf-8'))

                # Log pesanan di GUI
                log_widget.insert(tk.END, f"Pesanan diterima: {quantity} {nama}(s), Total: Rp.{total_harga:.2f}\n")

    except Exception as e:
        log_widget.insert(tk.END, f"Error: {e}\n")
        client_socket.close()

# Tambahkan variabel noID global
noID_counter = 1

# Server utama untuk menerima koneksi client
def start_server(log_widget):
    global server_thread, server_socket, server_running, noID_counter
    if server_running:
        log_widget.insert(tk.END, "Server sudah berjalan...\n")
        return
    
    server_running = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.110.214', 8080))
    
    server_socket.listen(5)
    log_widget.insert(tk.END, "Server dapur berjalan di port 8080...\n")

    def accept_clients():
        global noID_counter
        while server_running:
            try:
                client_socket, addr = server_socket.accept()
                # Ambil informasi alamat IP dan port client
                client_ip, client_port = addr
                # Format pesan terhubung dengan noID, IP client, dan port client
                connect_message = f"Terhubung dengan {noID_counter}_{client_ip}_{client_port}"
                log_widget.insert(tk.END, connect_message + "\n")
                
                # Jalankan thread untuk menangani client
                client_handler = threading.Thread(target=handle_client, args=(client_socket, log_widget))
                client_handler.start()
                
                # Increment noID untuk client berikutnya
                noID_counter += 1
            except socket.error:
                break

    server_thread = threading.Thread(target=accept_clients)
    server_thread.start()

# Fungsi untuk menghentikan server
def stop_server(log_widget):
    global server_running, server_socket, server_thread
    if not server_running:
        log_widget.insert(tk.END, "Server sudah berhenti...\n")
        return
    
    server_running = False
    log_widget.insert(tk.END, "Menutup server...\n")
    server_socket.close()  # Tutup socket untuk menghentikan server
    server_thread.join()  # Menunggu server thread berhenti dengan aman
    log_widget.insert(tk.END, "Server berhenti.\n")

# GUI untuk Server (Dapur)
def server_gui():
    global server_thread, server_socket, server_running
    server_thread = None
    server_socket = None
    server_running = False

    root = tk.Tk()
    root.title("Server Dapur")

    program_icon = Image.open("logo.png")  # Replace 'icon.png' with the actual path of your program icon file
    program_icon_photo = ImageTk.PhotoImage(program_icon)  # Convert to PhotoImage object

    # Set the program icon (icon displayed in the top-left corner of the window)
    root.iconphoto(False, program_icon_photo)  # False means it's the window's main icon

    log_label = tk.Label(root, text="Log Pesanan:")
    log_label.pack()

    log_widget = ScrolledText(root, width=50, height=20)
    log_widget.pack()

    start_button = tk.Button(root, text="Mulai Server", command=lambda: start_server(log_widget))
    start_button.pack()

    stop_button = tk.Button(root, text="Hentikan Server", command=lambda: stop_server(log_widget))
    stop_button.pack()

    restart_button = tk.Button(root, text="Restart Server", command=lambda: (stop_server(log_widget), start_server(log_widget)))
    restart_button.pack()

    root.mainloop()

if __name__ == "__main__":
    server_gui()
