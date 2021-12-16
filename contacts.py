# Import reuired tkinter module

from tkinter import Button, Entry, Label, LabelFrame, Scrollbar, StringVar, Tk, PhotoImage, Toplevel, font

from tkinter import ttk
from tkinter.constants import E, END, W

from database import Database

class Contacts:
    def __init__(self, root):
        self.root = root
        ttk.style = ttk.Style()
        ttk.style.configure("Treeview", font=("helvetica", 10))
        ttk.style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))
        
        
        self.db = Database()

        self.create_gui()
        

    def create_gui(self):
        self.create_left_icon()
        self.create_label_frame()
        self.create_message_area()
        self.create_tree_view()
        self.create_scrollbar()
        self.create_bottom_button()

        self.view_contacts()
        
    

    def create_left_icon(self):
        photo = PhotoImage(file='icons/logo.png')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=0)

    def create_label_frame(self):
        label_frame = LabelFrame(self.root, tex="Create New Contact", bg="sky blue", font="helvetica 10")
        label_frame.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        
        Label(label_frame, text="Name:", bg="green", fg="white").grid(row=1, column=1, sticky=W, pady=2, padx=15)
        self.namefield = Entry(label_frame)
        self.namefield.grid(row=1, column=3, sticky=W, padx=5 , pady=2)

        Label(label_frame, text="Email:", bg="green", fg="white").grid(row=2, column=1, sticky=W, pady=2, padx=15)
        self.emailfield = Entry(label_frame)
        self.emailfield.grid(row=2, column=3, sticky=W, padx=5 , pady=2)

        Label(label_frame, text="Number:", bg="green", fg="white").grid(row=3, column=1, sticky=W, pady=2, padx=15)
        self.numfield = Entry(label_frame)
        self.numfield.grid(row=3, column=3, sticky=W, padx=5 , pady=2)

        Button(label_frame, text="Add Contact", command=self.add_new_contact , bg="blue" , fg="white").grid(row=4, column=3, sticky=E, padx=5, pady=5)

    
    def create_message_area(self):
        self.message = Label(text="", fg="red")
        self.message.grid(row=3, column=1, sticky=W)

    
    def create_tree_view(self):
        self.tree = ttk.Treeview(height=10, columns=("name","email", "number"), style="Treeview")
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading("#0", text="ID", anchor=W)
        self.tree.heading("name", text="Name", anchor=W)
        self.tree.heading("email", text="Email Address", anchor=W)
        self.tree.heading("number", text="Contact Number", anchor=W)

    

    def create_scrollbar(self):
        self.scrollbar = Scrollbar(orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=6, column=3, rowspan=10, sticky='sn')

    
    def create_bottom_button(self):
        Button(text="Delete Selected", command=lambda: self.check_item_selected('REMOVE'), bg="red", fg="white").grid(row=8, column=0, sticky=W, pady=10 , padx=20)
        Button(text="Modify Selected", command=lambda: self.check_item_selected('MODIFY'), bg="purple", fg="white").grid(row=8, column=1, sticky=W, pady=10 , padx=20)

    
    def add_new_contact(self):
        if self.new_contatcs_validated():
            query = "INSERT INTO contacts VALUES (NULL, ?, ?, ?)"
            param = (self.namefield.get(), self.emailfield.get(), self.numfield.get())
            self.db.insert(query, param)
            self.message["text"] = f"New contact {self.namefield.get()} added"


            self.namefield.delete(0, END)
            self.emailfield.delete(0, END)
            self.numfield.delete(0, END)
        else:
            self.message["text"] = "name, email and number can not be blank"
        
        self.view_contacts()
    

    def new_contatcs_validated(self):
        return len(self.namefield.get()) !=0 and len(self.emailfield.get()) != 0 and len(self.numfield.get()) != 0 



    def view_contacts(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        
        query = "SELECT * FROM contacts ORDER BY name DESC"
        contact_entries = self.db.fetch(query)

        for row in contact_entries:
            self.tree.insert('', 0, text=row[0],values=(row[1], row[2], row[3]))

    

    def check_item_selected(self, action_type):
        self.message['text'] = ""
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = "No item selected"
            return 

        if action_type == 'REMOVE':
            self.delete_contacts()
        else:
            self.open_modify_window()

    def delete_contacts(self):
        self.message["text"] = ""
        id = self.tree.item(self.tree.selection())['text']
        query = "DELETE FROM contacts WHERE id=?"
        self.db.remove(query, id)
        self.message["text"] = "Contact deleted successfully"
        self.view_contacts()

    
    def open_modify_window(self):
        id = self.tree.item(self.tree.selection())['text']
        name = self.tree.item(self.tree.selection())['values'][0]
        old_number = self.tree.item(self.tree.selection())['values'][2]
        self.transient = Toplevel()
        self.transient.title('Update Contact')
        
        Label(self.transient, text='Name:').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=0, column=2)
        
        Label(self.transient, text='Old Contact Number:').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_number), state='readonly').grid(row=1, column=2)

        
        Label(self.transient, text='New Phone Number:').grid(
            row=2, column=1)
        new_phone_number_entry_widget = Entry(self.transient)
        new_phone_number_entry_widget.grid(row=2, column=2)


        Button(self.transient, text='Update Contact', command=lambda: self.update_contacts(
            new_phone_number_entry_widget.get(), old_number, id)).grid(row=3, column=2, sticky=E)

        self.transient.mainloop()

    
    def update_contacts(self, new_phone, old_phone, id):
        query = "UPDATE contacts SET phone_number=? WHERE phone_number =? AND id=?"
        params = (new_phone, old_phone, id)
        self.db.update(query, params)
        self.transient.destroy()
        self.message["text"] = "Phone number updated"
        self.view_contacts()



if __name__ == '__main__':
    root = Tk()
    root.title('My Contact List')
    root.geometry("750x450")
    root.resizable(width=False, height=False)
    application = Contacts(root)
    root.mainloop()