import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

# Global client socket for maintaining the connection
client_socket = None

# Function to handle request to server using the same connection
def send_request(request):
    global client_socket
    if client_socket is None:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.100.43', 8080))  # Connect to server

    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(4096).decode('utf-8')
    return response  # Return the response

# GUI for Client (Customer)
def client_gui():
    root = tk.Tk()
    root.title("Client Pelanggan")
    root.configure(bg="#f0f0f0")  # Change background color of the main window
    root.geometry("1024x768")  # Set the window size to be larger

    program_icon = Image.open("logo.png")  # Replace 'icon.png' with the actual path of your program icon file
    program_icon_photo = ImageTk.PhotoImage(program_icon)  # Convert to PhotoImage object

    # Set the program icon (icon displayed in the top-left corner of the window)
    root.iconphoto(False, program_icon_photo)  # False means it's the window's main icon

    # **Logo Section**
    # Load PNG logo using Pillow
    logo_image = Image.open("sigma_banner.png")  # Path to your PNG file
    logo_image = logo_image.resize((1024, 200), Image.ANTIALIAS)  # Resize the logo as needed
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Display the logo in the GUI
    logo_label = tk.Label(root, image=logo_photo, bg="#f0f0f0")
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)

    # Main frame to divide the layout (left: menu, right: input/output)
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create a canvas to hold the menu on the left side with a scrollbar
    canvas_frame = tk.Frame(main_frame, bg="#f0f0f0")
    canvas_frame.grid(row=0, column=0, sticky="n")

    # Make left_frame wider by increasing the canvas width
    canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", width=400, height=400)  # Increased width to 300
    canvas.grid(row=0, column=0)

    # Add a scrollbar for the canvas
    scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside the canvas to hold the menu items
    left_frame = tk.Frame(canvas, bg="#f0f0f0")
    canvas.create_window((0, 0), window=left_frame, anchor='nw')

    # Right side for input/output
    right_frame = tk.Frame(main_frame, bg="#f0f0f0")
    right_frame.grid(row=0, column=1, sticky="n", padx=10)

    output_label = tk.Label(right_frame, text="Review Pesanan:", bg="#f0f0f0")
    output_label.pack()

    output_widget = ScrolledText(right_frame, width=50, height=10)
    output_widget.pack()

    # New frame for checkout information
    checkout_info_frame = tk.Frame(right_frame, bg="#f0f0f0")
    checkout_info_frame.pack(fill=tk.X, pady=10)

    # Label and output for checkout info
    checkout_info_label = tk.Label(checkout_info_frame, text="Informasi Checkout:", bg="#f0f0f0")
    checkout_info_label.pack(anchor='w')

    checkout_info_widget = ScrolledText(checkout_info_frame, width=50, height=5)
    checkout_info_widget.pack()

    # Dictionary to store the order counts of each item
    item_order_count = {}        # Tracks the current count set by the user (via "+")
    confirmed_orders = {}        # Tracks the confirmed order when "Add" is clicked
    item_prices = {}             # Store prices of items for total calculation

    # Function to handle checkout and display the server response in checkout info frame
    def checkout_pesanan():
        total_cost = 0
        checkout_info_widget.delete("1.0", tk.END)  # Clear the checkout info before updating

        for item, count in confirmed_orders.items():
            if count > 0:
                request = f"order,{item},{count}"
                response = send_request(request)  # Send request and get response from server

                # Display response in the checkout information frame
                checkout_info_widget.insert(tk.END, response + '\n')  

                # Parsing the response to extract total cost
                try:
                    total_line = response.split("Total: Rp.")[1]
                    total_cost += float(total_line.strip())
                except (IndexError, ValueError):
                    checkout_info_widget.insert(tk.END, "Error parsing total cost.\n")
        
        # Display total cost at the end of the checkout info
        checkout_info_widget.insert(tk.END, f"\nTotal pembayaran: Rp.{total_cost:.2f}")

    # Function to exit
    def keluar():
        send_request('exit')
        root.quit()

    # Function to increase the order count
    def tambah_pesanan(item, label):
        item_order_count[item] += 1
        label.config(text=str(item_order_count[item]))

    # Function to decrease the order count
    def kurangi_pesanan(item, label):
        if item_order_count[item] > 0:
            item_order_count[item] -= 1
            label.config(text=str(item_order_count[item]))

    # Function to confirm the order when "Add" is clicked
    def add_pesanan(item):
        if item_order_count[item] > 0:
            confirmed_orders[item] = item_order_count[item]
            output_widget.insert(tk.END, f"{item}: {item_order_count[item]} porsi ditambahkan ke pesanan\n")
        else:
            output_widget.insert(tk.END, f"{item}: Tidak ada porsi untuk ditambahkan\n")

    # Function to cancel the order and reset count to 0
    def batalkan_pesanan(item, label):
        if item in confirmed_orders:
            confirmed_orders[item] = 0  # Reset confirmed orders to 0
            item_order_count[item] = 0  # Reset item count to 0
            label.config(text="0")  # Update the label to show 0
            output_widget.insert(tk.END, f"{item}: Pesanan dibatalkan, jumlah direset ke 0\n")
        else:
            output_widget.insert(tk.END, f"{item}: Tidak ada pesanan untuk dibatalkan\n")

    # Function to review the orders added and total payment
    def review_pesanan():
        output_widget.delete("1.0", tk.END)  # Clear output widget before showing the review
        output_widget.insert(tk.END, "Daftar Pesanan Anda:\n")
        total_payment = 0  # Initialize total payment
        
        for item, count in confirmed_orders.items():
            if count > 0:
                price = item_prices.get(item, 0)  # Get item price
                total_item_price = price * count  # Calculate total price for this item
                output_widget.insert(tk.END, f"{item}: {count} porsi @ Rp.{price:.2f} -> Total: Rp.{total_item_price:.2f}\n")  # Show item, count, and price
                total_payment += total_item_price  # Calculate total payment

        # Display total payment at the end of the review
        output_widget.insert(tk.END, f"\nTotal Pembayaran: Rp.{total_payment:.2f}\n")  # Show total payment in review

    # Function to fetch and display menu on the left side
    def tampilkan_menu():
        response = send_request('menu')  # Fetch menu from server
        menu_items = response.strip().split("\n")

        # Display menu and create buttons for each item
        for row, item in enumerate(menu_items):
            if item:
                item_name, item_price = item.split(': Rp')
                item_order_count[item_name] = 0  # Initialize order count
                confirmed_orders[item_name] = 0  # Initialize confirmed orders
                item_prices[item_name] = float(item_price)  # Store prices for total calculation

                # Label untuk item
                item_label = tk.Label(left_frame, text=f"{item_name}: Rp.{item_price}", bg="#f0f0f0")
                item_label.grid(row=row + 1, column=0, sticky="w", padx=5, pady=5)

                # Label untuk jumlah pesanan
                jumlah_label = tk.Label(left_frame, text="0", width=3, bg="#f0f0f0")
                jumlah_label.grid(row=row + 1, column=1, padx=5)

                # Tombol Kurang (-)
                kurang_button = tk.Button(left_frame, text="-", command=lambda i=item_name, l=jumlah_label: kurangi_pesanan(i, l))
                kurang_button.grid(row=row + 1, column=2, padx=5)

                # Tombol Tambah (+)
                tambah_button = tk.Button(left_frame, text="+", command=lambda i=item_name, l=jumlah_label: tambah_pesanan(i, l))
                tambah_button.grid(row=row + 1, column=3, padx=5)

                # Tombol Add
                add_button = tk.Button(left_frame, text="Add", command=lambda i=item_name: add_pesanan(i))
                add_button.grid(row=row + 1, column=4, padx=5)

                # Tombol Cancel
                cancel_button = tk.Button(left_frame, text="Cancel", command=lambda i=item_name, l=jumlah_label: batalkan_pesanan(i, l))
                cancel_button.grid(row=row + 1, column=5, padx=5)

        left_frame.update_idletasks()  # Ensure all widgets are placed before configuring scroll region
        canvas.config(scrollregion=canvas.bbox("all"))  # Set scroll region based on widgets' bounding box

    # Automatically fetch the menu when the GUI starts
    tampilkan_menu()

    # Button to checkout the order
    checkout_button = tk.Button(root, text="Checkout", command=checkout_pesanan)
    checkout_button.pack(side=tk.BOTTOM, pady=10)

    # Button to review the orders
    review_button = tk.Button(root, text="Review Pesanan", command=review_pesanan)
    review_button.pack(side=tk.BOTTOM)

    # Button to exit
    exit_button = tk.Button(root, text="Keluar", command=keluar)
    exit_button.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()

client_gui()
