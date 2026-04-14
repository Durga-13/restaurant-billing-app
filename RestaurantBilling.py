import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# ✅ MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Mysql@13",
    database="restaurant_db"
)
cursor = conn.cursor()

# ✅ GUI Setup
root = tk.Tk()
root.title("Restaurant Bill Generator")
root.geometry("750x700")

tk.Label(root, text="🍽 Restaurant Billing System", font=("Arial", 18)).pack(pady=10)

# ✅ Reservation Section
tk.Label(root, text="Table ID").pack()
table_id_entry = tk.Entry(root)
table_id_entry.pack()

tk.Label(root, text="Customer Name").pack()
customer_name_entry = tk.Entry(root)
customer_name_entry.pack()

def reserve_table():
    table_id = table_id_entry.get()
    name = customer_name_entry.get()
    if table_id and name:
        try:
            cursor.execute(
                "INSERT INTO reserved_tables (table_id, customer_name, reservation_time) VALUES (%s, %s, %s)",
                (table_id, name, datetime.now())
            )
            conn.commit()
            messagebox.showinfo("Success", f"Table {table_id} reserved for {name}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", str(err))
    else:
        messagebox.showwarning("Input Error", "Please enter table ID and customer name")

tk.Button(root, text="Reserve Table", command=reserve_table).pack(pady=5)

# ✅ Menu Display
tk.Label(root, text="Select Menu Items").pack()
menu_tree = ttk.Treeview(root, columns=("Item", "Category", "Price"), show="headings", height=12)
menu_tree.pack()

for col in ("Item", "Category", "Price"):
    menu_tree.heading(col, text=col)

try:
    cursor.execute("SELECT item_name, category, price FROM menu_items")
    menu_data = cursor.fetchall()
    for item in menu_data:
        menu_tree.insert("", tk.END, values=item)
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", str(err))

# ✅ Bill Section
selected_items = []

def add_to_bill():
    selected = menu_tree.focus()
    if selected:
        item = menu_tree.item(selected)["values"]
        selected_items.append(item)
        bill_list.insert(tk.END, f"{item[0]} - ₹{item[2]}")

tk.Button(root, text="Add to Bill", command=add_to_bill).pack(pady=5)

bill_list = tk.Listbox(root, width=60)
bill_list.pack()

def generate_bill():
    table_id = table_id_entry.get()
    name = customer_name_entry.get()

    # ✅ Auto-insert reservation if not already saved
    if table_id and name:
        try:
            cursor.execute("SELECT * FROM reserved_tables WHERE table_id = %s AND customer_name = %s", (table_id, name))
            existing = cursor.fetchone()
            if not existing:
                cursor.execute(
                    "INSERT INTO reserved_tables (table_id, customer_name, reservation_time) VALUES (%s, %s, %s)",
                    (table_id, name, datetime.now())
                )
                conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Reservation failed: {err}")
    else:
        messagebox.showwarning("Missing Info", "Please enter table ID and customer name")

    # ✅ Generate bill
    total = sum([float(item[2]) for item in selected_items])
    bill_text = "\n".join([f"{item[0]} - ₹{item[2]}" for item in selected_items])
    bill_text += f"\n\nTotal Amount: ₹{total}"
    messagebox.showinfo("🧾 Final Bill", bill_text)

tk.Button(root, text="Generate Bill", command=generate_bill).pack(pady=10)

# ✅ View Reserved Tables
def view_reservations():
    cursor.execute("SELECT * FROM reserved_tables")
    records = cursor.fetchall()
    result = "\n".join([
        f"Table {r[0]} - {r[1]} at {r[2].strftime('%d-%b %I:%M %p')}" for r in records
    ])
    messagebox.showinfo("Reserved Tables", result if result else "No reservations found")

tk.Button(root, text="View Reserved Tables", command=view_reservations).pack(pady=5)

root.mainloop()
