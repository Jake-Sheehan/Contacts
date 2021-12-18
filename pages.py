import tkinter as tk
from tkinter import ttk
import database


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        # show frame and make it fill screen
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        # Delete frame
        self.pack_forget()


class MainFrame(Page):
    # Initializer
    def __init__(self, *args, **kwargs):
        # Call init of parent class
        Page.__init__(self, *args, **kwargs)

        # Set background color
        self.configure(background='#AAB8B6')

        # Configure columns
        self.grid_columnconfigure(0, weight=2, pad=10)
        self.grid_columnconfigure(1, weight=2, pad=10)
        self.grid_columnconfigure(2, weight=2, pad=10)
        self.grid_columnconfigure(3, weight=1, pad=10)

        # Configure rows
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=10)
        self.grid_rowconfigure(0, pad=5)
        self.grid_rowconfigure(1, pad=5)
        self.grid_rowconfigure(2, pad=5)

        # Get instance of database
        self.db = database.Database()

        # Variables
        self.new_name = tk.StringVar(self, value="Name")
        self.new_phone = tk.StringVar(self, value="Phone Number")
        self.new_email = tk.StringVar(self, value="Email")

        # --- Widgets ---
        # Name entry
        self.name_entry = tk.Entry(self, textvariable=self.new_name)
        self.name_entry.bind("<FocusOut>", self.name_entry_focus_out)
        self.name_entry.bind("<FocusIn>", self.name_entry_focus_in)
        # Phone entry
        self.phone_entry = tk.Entry(self, textvariable=self.new_phone)
        self.phone_entry.bind("<FocusOut>", self.phone_entry_focus_out)
        self.phone_entry.bind("<FocusIn>", self.phone_entry_focus_in)
        # Email entry
        self.email_entry = tk.Entry(self, textvariable=self.new_email)
        self.email_entry.bind("<FocusOut>", self.email_entry_focus_out)
        self.email_entry.bind("<FocusIn>", self.email_entry_focus_in)
        # Add button
        self.add_button = tk.Button(self, text="Add", bg="#DCE1E3",
                                    borderwidth=4, fg="black", command=self.add_button_clicked)
        # Delete button
        self.delete_button = tk.Button(self, text="Delete", bg="#DCE1E3",
                                       borderwidth=4, fg="black", command=self.delete_button_clicked)

        # Contact Treeview
        self.contact_list = ttk.Treeview(self, selectmode="browse")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.contact_list.yview)
        self.contact_list.configure(yscrollcommand=self.scrollbar.set)
        self.contact_list["columns"] = ("0", "1", "2")
        self.contact_list["show"] = "headings"
        self.contact_list.heading("0", text="Name")
        self.contact_list.heading("1", text="Phone")
        self.contact_list.heading("2", text="Email")

        # Display widgets
        self.scrollbar.grid(row=2, column=3, sticky="nse")
        self.name_entry.grid(row=0, column=0, padx=10, sticky="ew")
        self.phone_entry.grid(row=0, column=1, padx=10, sticky="ew")
        self.email_entry.grid(row=0, column=2, padx=10, sticky="ew")
        self.add_button.grid(row=0, column=3, padx=10, sticky="ew")
        self.delete_button.grid(row=1, column=3, padx=10, pady=(0, 25), sticky="ew")
        self.contact_list.grid(row=2, column=0, columnspan=4, sticky="nsew")

        # Show contacts
        self.show_contacts()

    def show_contacts(self):
        # Get all contacts from database
        contacts = list(self.db.collection.find({}))
        # iterate over contacts and add them as labels
        for contact in contacts:
            self.contact_list.insert("", "end", text="L1", values=(contact['name'], contact['phone'], contact['email']))

    # Callbacks

    # if name entry gains focus, remove placeholder
    def name_entry_focus_in(self, event):
        widget = event.widget
        if widget.get() == "Name":
            self.new_name.set("")

    # if phone entry gains focus, remove placeholder
    def phone_entry_focus_in(self, event):
        widget = event.widget
        if widget.get() == "Phone Number":
            self.new_phone.set("")

    # if email entry gains focus, remove placeholder
    def email_entry_focus_in(self, event):
        widget = event.widget
        if widget.get() == "Email":
            self.new_email.set("")

    # if name entry loses focus, restore placeholder
    def name_entry_focus_out(self, event):
        widget = event.widget
        if widget.get() == "":
            self.new_name.set("Name")

    # if phone entry loses focus, restore placeholder
    def phone_entry_focus_out(self, event):
        widget = event.widget
        if widget.get() == "":
            self.new_phone.set("Phone Number")

    # if email entry loses focus, restore placeholder
    def email_entry_focus_out(self, event):
        widget = event.widget
        if widget.get() == "":
            self.new_email.set("Email")

    def add_button_clicked(self):
        # Grab text from entry boxes and create a new dict to enter in database
        name = self.new_name.get()
        phone = self.new_phone.get()
        email = self.new_email.get()
        new_entry = {"name": name, "phone": phone, "email": email}
        # Insert into database
        self.db.insert(new_entry)
        # Insert into treeview
        self.contact_list.insert("", "end", text="L1", values=(name, phone, email))
        # Set variables back to default values
        self.new_name.set("Name")
        self.new_phone.set("Phone Number")
        self.new_email.set("Email")

    def delete_button_clicked(self):
        # Grab selection
        selection = self.contact_list.selection()
        # Grab item
        item = self.contact_list.item(selection[0])
        # Grab contact from item
        contact = item['values']
        # Active contact
        active_contact = {"name": contact[0], "phone": contact[1], "email": contact[2]}
        # Delete the active contact from the database
        self.db.delete(active_contact)
        # Remove selected item from treeview
        self.contact_list.delete(selection[0])
