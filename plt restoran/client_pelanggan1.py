import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Global client socket for maintaining the connection
client_socket = None

# Function to handle request to server using the same connection
def send_request(request):
    global client_socket
    if client_socket is None:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #client_socket.connect(('localhost', 8080))  # Connect to server
        client_socket.connect(('192.168.110.214', 8080))  # Connect to server

    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(4096).decode('utf-8')
    return response  # Return the response

# GUI for Client (Customer)
def client_gui():
    root = tk.Tk()
    root.title("Client Pelanggan")

    # Main frame to divide the layout (left: menu, right: input/output)
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Left side for menu
    left_frame = tk.Frame(main_frame, width=200)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Label Menu
    menu_label = tk.Label(left_frame, text="Daftar Menu:")
    menu_label.pack()

    # Right side for input/output
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    output_label = tk.Label(right_frame, text="Review Pesanan:")
    output_label.pack()

    output_widget = ScrolledText(right_frame, width=50, height=10)
    output_widget.pack()

    # New frame for checkout information
    checkout_info_frame = tk.Frame(right_frame)
    checkout_info_frame.pack(fill=tk.X, pady=10)

    # Label and output for checkout info
    checkout_info_label = tk.Label(checkout_info_frame, text="Informasi Checkout:")
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
                    # Contoh respons: "Pesanan untuk 2 Nasi Goreng Spesial diterima. Total: Rp.50000.00"
                    # Pisahkan menggunakan "Total: Rp." sebagai pemisah
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

    # Function to cancel the order
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
        for item in menu_items:
            if item:
                item_name, item_price = item.split(': Rp')
                item_order_count[item_name] = 0  # Initialize order count
                confirmed_orders[item_name] = 0  # Initialize confirmed orders
                item_prices[item_name] = float(item_price)  # Store prices for total calculation

                item_frame = tk.Frame(left_frame)
                item_frame.pack(fill=tk.X)

                item_label = tk.Label(item_frame, text=f"{item_name}: Rp.{item_price}")
                item_label.pack(side=tk.LEFT)

                # Display the count next to the item
                jumlah_label = tk.Label(item_frame, text="0", width=3)
                jumlah_label.pack(side=tk.LEFT)

                # Decrease order count button
                kurang_button = tk.Button(item_frame, text="-", command=lambda i=item_name, l=jumlah_label: kurangi_pesanan(i, l))
                kurang_button.pack(side=tk.LEFT)

                # Increase order count button
                tambah_button = tk.Button(item_frame, text="+", command=lambda i=item_name, l=jumlah_label: tambah_pesanan(i, l))
                tambah_button.pack(side=tk.LEFT)

                # Add button to confirm the order
                add_button = tk.Button(item_frame, text="Add", command=lambda i=item_name: add_pesanan(i))
                add_button.pack(side=tk.LEFT)

                # Add button to cancel the order
                cancel_button = tk.Button(item_frame, text="Cancel", command=lambda i=item_name, l=jumlah_label: batalkan_pesanan(i, l))
                cancel_button.pack(side=tk.LEFT)


    # Automatically fetch the menu when the app starts
    tampilkan_menu()

    # Checkout button
    order_button = tk.Button(right_frame, text="Checkout Pesanan", command=checkout_pesanan)
    order_button.pack()

    # Review button
    review_button = tk.Button(right_frame, text="Review Pesanan", command=review_pesanan)
    review_button.pack()

    # Exit button
    exit_button = tk.Button(right_frame, text="Keluar", command=keluar)
    exit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    client_gui()
