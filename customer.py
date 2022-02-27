from cgitb import text
import tkinter as tk
from tkinter import CENTER, Canvas, Scrollbar, ttk
import sqlite3
from sqlite3 import Error
from page import Page


class CustomerPage(Page):
    
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, *args, **kwargs) 
        self.root = root

    def create_insert_window(self):
        
        self.clean_right_frame()
        # Insert button now unclickable until actions done on insert window completed
        self.insert_button['state'] = tk.DISABLED
        
        work_frame = tk.Frame(self.right_frame)
        work_frame.pack(anchor='w', side='top', padx=10)
        
        # For retrieving what was written in entry boxes
        name_var = tk.StringVar()  
        shipping_address_var = tk.StringVar()  
        email_var = tk.StringVar()
        
        def insert():
            self.disabled_insert()
            # Object formed to be passed through self.insert() with sql statement
            customer = (
                name_var.get(),
                shipping_address_var.get(),
                email_var.get()
            )
            sql = 'INSERT INTO customer(name, shipping_address, email) VALUES(?, ?, ?)'
            id = self.insert(sql, customer)
            
            # Confirmation window
            result_window = tk.Toplevel()
            # For having pop-up window in centre of 'mainframe'
            r_x = self.root.winfo_x() + self.root.winfo_width()/2
            r_y = self.root.winfo_y() + self.root.winfo_height()/2
            result_window.geometry(f"300x70+{int(r_x)-150}+{int(r_y)-35}") 
            self.set_active(result_window)
            
            id_label = tk.Label(result_window, text=f'Record succesfully created with id: {id}').pack(side='top')
            button = tk.Button(result_window, text='OK', command=lambda:[result_window.destroy(), work_frame.destroy(), self.enabled_insert_select()])
            button.pack(side='bottom')
        
        # Entry boxes for inputting data for fields
        name_label = tk.Label(work_frame, text='Name: ').pack(side='top')
        name_entry = tk.Entry(work_frame, textvariable=name_var).pack(side='top')
        
        shipping_address_label = tk.Label(work_frame, text='Shipping Address: ').pack(side='top')
        shipping_address_entry = tk.Entry(work_frame, textvariable=shipping_address_var).pack(side='top')

        email_label = tk.Label(work_frame, text='Email: ').pack(side='top')
        email_entry = tk.Entry(work_frame, textvariable=email_var).pack(side='top')
        
        insert_button = tk.Button(work_frame, text='Insert', width=10, command=insert)
        insert_button.pack(side='top')
        
        cancel_button = tk.Button(work_frame, text='Cancel', width=10, command=lambda:[self.clean_right_frame(), self.enabled_insert_select()])
        cancel_button.pack(side='top')
    
    def create_select_window(self):
        self.clean_right_frame()
        self.select_button['state'] = tk.DISABLED
        
        # Result set and search criteria frame established in right frame parent 
        result_set_frame = tk.Frame(self.right_frame)
        result_set_frame.pack(side='right', fill="both", expand=True, padx=10)

        search_criteria_frame = tk.Frame(self.right_frame)
        search_criteria_frame.pack(anchor='n', side='top', padx=10)
         
        scrollbar = Scrollbar(result_set_frame)
        scrollbar.pack(side='right', fill=tk.Y)
        
        scrollbar = Scrollbar(result_set_frame, orient='horizontal')
        scrollbar.pack(side='bottom', fill=tk.X)
        
        customer_table = ttk.Treeview(
            result_set_frame, 
            yscrollcommand=scrollbar.set,
            xscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        
        customer_table.pack(fill='both')
        scrollbar.config(command=customer_table.yview)
        scrollbar.config(command=customer_table.xview)
        
        customer_table['columns'] = ('customer_id', 'name', 'shipping_address', 'email')
        
        customer_table.column("#0", width=0,  stretch=tk.NO)
        customer_table.column("customer_id",anchor='w', width=80)
        customer_table.column("name",anchor='w', width=80)
        customer_table.column("shipping_address",anchor='w', width=80)
        customer_table.column("email",anchor='w', width=80)
        
        customer_table.heading("#0", text='',  anchor=tk.CENTER)
        customer_table.heading("customer_id",text="customer Id",anchor=tk.CENTER)
        customer_table.heading("name",text="Name",anchor=tk.CENTER)
        customer_table.heading("shipping_address",text="Shipping Address",anchor=tk.CENTER)
        customer_table.heading("email",text="Email",anchor=tk.CENTER)
        
        name_var = tk.StringVar()  
        shipping_address_var = tk.StringVar()  
        email_var = tk.StringVar()       

        def select():
            self.disable_select()
            # Table restarts - Empties table if full
            customer_table.delete(*customer_table.get_children())
            
            name = name_var.get()
            shipping_address = shipping_address_var.get()
            email = email_var.get()
            
            # Use of wildcards
            # Object (customer) formed to be passed through self.select() with sql statement
            customer = (
                name or '%',
                shipping_address or '%',
                email or '%'
            )

            sql = 'SELECT * FROM customer WHERE name like ? AND shipping_address like ? AND email like ?'
            rows = self.select(sql, customer)
            
            counter = 0
            # Rows returned from self.select() iterated through and inserted into customer_table made in lines 159-187
            for row in rows:
                customer_table.insert(
                    parent='',
                    index='end',
                    iid=counter,
                    text='',
                    values = row
                )
                counter += 1
            # If no rows are present in table after specific selection was requested
            # Error message appears and selection process repeats
            if len(customer_table.get_children()) == 0:
                pop_up_none = tk.Toplevel()
                r_x = self.root.winfo_x() + self.root.winfo_width()/2
                r_y = self.root.winfo_y() + self.root.winfo_width()/2
                pop_up_none.geometry(f"300x70+{int(r_x)-150}+{int(r_y)-35}") 
                message = tk.Label(pop_up_none, text='ERROR: No records found').pack(side='top')
                button = tk.Button(pop_up_none, text='OK', command=pop_up_none.destroy).pack(side='bottom')
            else:
                customer_table.pack(expand=True)
            
        def delete_clicked():
            pop_up_delete = tk.Toplevel()
            pop_up_delete.title('Delete Record')
            work_frame = tk.Frame(pop_up_delete, padx=10, pady=10)
            work_frame.pack(side='left', fill='both', expand=True)
            self.set_active(pop_up_delete)
            
            item = customer_table.item(customer_table.focus()).get('values')
            confirmation = tk.Label(work_frame, text='Are you sure you want to delete this record?').pack(side='top', pady=5)
            id_label = tk.Label(work_frame, text=f'Id: {item[0]}').pack(side='top', pady=5)
            
            customer_label = tk.Label(work_frame, text='Name: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            customer_label_value = tk.Label(work_frame, text=item[1]).pack(side='top', pady=5)
            
            shipping_address_label = tk.Label(work_frame, text='Shipping Address: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            shipping_address_label_value = tk.Label(work_frame, text=item[2]).pack(side='top', pady=5)
            
            email_label = tk.Label(work_frame, text='Email: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            email_label_value = tk.Label(work_frame, text=item[3]).pack(side='top', pady=5)
            
            def cancel_delete():
                pop_up_delete.destroy()
                pop_up_delete.update()
                
            def delete_record():
                customer = (item[0],)
                sql = 'DELETE FROM customer WHERE customer_id=?'
                self.delete(sql, customer)
                
                select()
                pop_up_delete.destroy()
            
            cancel_button = tk.Button(work_frame, text='Cancel', width=10, command=cancel_delete).pack(side='bottom')
            ok_button = tk.Button(work_frame, text='Ok', width=10, command=delete_record).pack(side='bottom')
            
            r_x = self.root.winfo_x() + self.root.winfo_width()/2
            r_y = self.root.winfo_y() + self.root.winfo_height()/2
            # print(r_x)
            # print(r_y)
            #TODO: fix position of this pop up window...
            pop_up_delete.geometry(f"300x330+{int(r_x)-150}+{int(r_y)-165}")
            
            
        def update_clicked():
            # Making update window that has entry fields already filled in with what record the user selected by cursor on table
            name_var_update = tk.StringVar()
            shipping_address_var_update = tk.StringVar()  
            email_var_update = tk.StringVar()
            
            pop_up_update = tk.Toplevel()
            pop_up_update.title('Update Record')
            work_frame = tk.Frame(pop_up_update, padx=10, pady=10)
            work_frame.pack(side='left', fill='both', expand=True)
            self.set_active(pop_up_update)
            
            # Item = dictionary of keys and tuples, one of which is values and is retrieved below
            item = customer_table.item(customer_table.focus()).get('values')
            
            # Id label uneditable
            id_label = tk.Label(work_frame, text=f'Id: {item[0]}').pack(side='top', pady=5)
            
            # Supplier name retrieved then placed in entry box being editable by user
            # Same done for email and 
            name_var_update.set(item[1])
            name_label = tk.Label(work_frame, text='Name: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            name_entry = tk.Entry(work_frame, textvariable=name_var_update).pack(side='top', pady=5, fill='both')
            
            shipping_address_var_update.set(item[2])
            shipping_address_label = tk.Label(work_frame, text='Shipping Address: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            shipping_address_entry = tk.Entry(work_frame, textvariable=shipping_address_var_update).pack(side='top', pady=5, fill='both')

            email_var_update.set(item[3])
            email_label = tk.Label(work_frame, text='Email: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            email_entry = tk.Entry(work_frame, textvariable=email_var_update).pack(side='top', pady=5, fill='both')
            
            def save_updated_item():
                # Once save button clicked - update process takes place
                customer = (
                    name_var_update.get(),
                    shipping_address_var_update.get(),
                    email_var_update.get(),
                    item[0]
                )
                sql = 'UPDATE customer SET name = ?, shipping_address = ?, email = ? WHERE customer_id = ?'
                self.update(sql, customer)
                
                select()
                pop_up_update.destroy()
                
            def cancel_update():
                pop_up_update.destroy()
                pop_up_update.update()
                
            cancel_button = tk.Button(work_frame, text='Cancel', width=10, command=cancel_update).pack(side='bottom')
            save_button = tk.Button(work_frame, text='Save', width=10, command=save_updated_item).pack(side='bottom')

            r_x = self.root.winfo_x() + self.root.winfo_width()/2
            r_y = self.root.winfo_y() + self.root.winfo_height()/2
            pop_up_update.geometry(f"300x300+{int(r_x)-150}+{int(r_y)-150}") 
            
            
        delete_button = tk.Button(result_set_frame, text='Delete', width=15, command=delete_clicked)
        delete_button.pack(anchor="e", side="bottom")
        update_button = tk.Button(result_set_frame, text='Update', width=15, command=update_clicked)
        update_button.pack(anchor="e", side="bottom")
              
        name_label = tk.Label(search_criteria_frame, text='Name: ').pack(side='top')
        name_entry = tk.Entry(search_criteria_frame, textvariable=name_var).pack(side='top')
        
        shipping_address_label = tk.Label(search_criteria_frame, text='Shipping Address: ').pack(side='top')
        shipping_address_entry = tk.Entry(search_criteria_frame, textvariable=shipping_address_var).pack(side='top')

        email_label = tk.Label(search_criteria_frame, text='Email: ').pack(side='top')
        email_entry = tk.Entry(search_criteria_frame, textvariable=email_var).pack(side='top')

        cancel_button = tk.Button(search_criteria_frame, text='Cancel', width=10, command=lambda:[self.clean_right_frame(), self.enabled_insert_select()])
        cancel_button.pack(side = "bottom")
        select_button = tk.Button(search_criteria_frame, text='Select', width=10, command=select)
        select_button.pack(side='bottom')