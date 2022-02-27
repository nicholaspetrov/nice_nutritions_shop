from cgitb import text
import tkinter as tk
from tkinter import CENTER, Canvas, Scrollbar, ttk
import sqlite3
from sqlite3 import Error
from page import Page


class ShoppingOrderPage(Page):
    
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, *args, **kwargs) 
        self.root = root

    def create_insert_window(self):
        
        self.clean_right_frame()
        # Insert button now unclickable until actions done on insert window completed
        self.insert_button['state'] = tk.DISABLED
        
        work_frame = tk.Frame(self.right_frame)#, background='green')
        work_frame.pack(anchor='w', side='top', padx=10)
        
        # For retrieving what was written in entry boxes
        status_var = tk.StringVar()  
        date_sent_var = tk.StringVar()  
        date_delivered_var = tk.StringVar()
        customer_id_var = tk.StringVar()

        def insert():
            self.disabled_insert()
            # Object formed to be passed through self.insert() with sql statement
            shopping_order = (
                status_var.get(),
                date_sent_var.get(),
                date_delivered_var.get(),
                customer_id_var.get()
            )
            sql = 'INSERT INTO shopping_order(status, date_sent, date_delivered, customer_id) VALUES(?, ?, ?, ?)'
            id = self.insert(sql, shopping_order)
            
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
        status_label = tk.Label(work_frame, text='Status: ').pack(side='top')
        status_entry = tk.Entry(work_frame, textvariable=status_var).pack(side='top')
        
        date_sent_label = tk.Label(work_frame, text='Date Sent: ').pack(side='top')
        date_sent_entry = tk.Entry(work_frame, textvariable=date_sent_var).pack(side='top')

        date_delivered_label = tk.Label(work_frame, text='Date Delivered: ').pack(side='top')
        date_delivered_entry = tk.Entry(work_frame, textvariable=date_delivered_var).pack(side='top')

        customer_id_label = tk.Label(work_frame, text='Customer ID: ').pack(side='top')
        customer_id_entry = tk.Entry(work_frame, textvariable=customer_id_var).pack(side='top')
        
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
        
        shopping_order_table = ttk.Treeview(
            result_set_frame, 
            yscrollcommand=scrollbar.set,
            xscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        
        shopping_order_table.pack(fill='both')
        scrollbar.config(command=shopping_order_table.yview)
        scrollbar.config(command=shopping_order_table.xview)
        
        shopping_order_table['columns'] = ('shopping_order_id', 'status', 'date_sent', 'date_delivered', 'customer_id')
        
        shopping_order_table.column("#0", width=0,  stretch=tk.NO)
        shopping_order_table.column("shopping_order_id",anchor='w', width=80)
        shopping_order_table.column("status",anchor='w', width=80)
        shopping_order_table.column("date_sent",anchor='w', width=80)
        shopping_order_table.column("date_delivered",anchor='w', width=80)
        shopping_order_table.column("customer_id",anchor='w', width=80)
        
        shopping_order_table.heading("#0", text='',  anchor=tk.CENTER)
        shopping_order_table.heading("shopping_order_id",text="Shopping Order ID",anchor=tk.CENTER)
        shopping_order_table.heading("status",text="Status",anchor=tk.CENTER)
        shopping_order_table.heading("date_sent",text="Date Sent",anchor=tk.CENTER)
        shopping_order_table.heading("date_delivered",text="Date Delivered",anchor=tk.CENTER)
        shopping_order_table.heading("customer_id",text="Customer ID",anchor=tk.CENTER)
        
        status_var = tk.StringVar()  
        date_sent_var = tk.StringVar()  
        date_delivered_var = tk.StringVar()
        customer_id_var = tk.StringVar()

        def select():
            self.disable_select()
            # Table restarts - Empties table if full
            shopping_order_table.delete(*shopping_order_table.get_children())
            
            status = status_var.get()
            date_sent = date_sent_var.get()
            date_delivered = date_delivered_var.get()
            customer_id = customer_id_var.get()
            
            # Use of wildcards
            # Object (shopping_order) formed to be passed through self.select() with sql statement
            shopping_order = (
                status or '%',
                date_sent or '%',
                date_delivered or '%',
                customer_id or '%'
            )

            sql = 'SELECT * FROM shopping_order WHERE status like ? AND date_sent like ? AND date_delivered like ? AND customer_id like ?'
            rows = self.select(sql, shopping_order)
            
            counter = 0
            # Rows returned from self.select() iterated through and inserted into shopping_order_table made in lines 159-187
            for row in rows:
                shopping_order_table.insert(
                    parent='',
                    index='end',
                    iid=counter,
                    text='',
                    values = row
                )
                counter += 1
            # If no rows are present in table after specific selection was requested
            # Error message appears and selection process repeats
            if len(shopping_order_table.get_children()) == 0:
                pop_up_none = tk.Toplevel()
                r_x = self.root.winfo_x() + self.root.winfo_width()/2
                r_y = self.root.winfo_y() + self.root.winfo_width()/2
                pop_up_none.geometry(f"300x70+{int(r_x)-150}+{int(r_y)-35}") 
                message = tk.Label(pop_up_none, text='ERROR: No records found').pack(side='top')
                button = tk.Button(pop_up_none, text='OK', command=pop_up_none.destroy).pack(side='bottom')
            else:
                shopping_order_table.pack(expand=True)
            
        def delete_clicked():
            pop_up_delete = tk.Toplevel()
            pop_up_delete.title('Delete Record')
            work_frame = tk.Frame(pop_up_delete, padx=10, pady=10)
            work_frame.pack(side='left', fill='both', expand=True)
            self.set_active(pop_up_delete)
            
            item = shopping_order_table.item(shopping_order_table.focus()).get('values')
            confirmation = tk.Label(work_frame, text='Are you sure you want to delete this record:').pack(side='top', pady=5)
            id_label = tk.Label(work_frame, text=f'Id: {item[0]}').pack(side='top', pady=5)
            
            status_label = tk.Label(work_frame, text='Status: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            status_label_value = tk.Label(work_frame, text=item[1]).pack(side='top', pady=5)
            
            date_sent_label = tk.Label(work_frame, text='Date Sent: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            date_sent_label_value = tk.Label(work_frame, text=item[2]).pack(side='top', pady=5)

            date_delivered_label = tk.Label(work_frame, text='Date Delivered: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            date_delivered_label_value = tk.Label(work_frame, text=item[3]).pack(side='top', pady=5)
            
            customer_id_label = tk.Label(work_frame, text='Customer ID: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            customer_id_value = tk.Label(work_frame, text=item[4]).pack(side='top', pady=5)
            
            def cancel_delete():
                pop_up_delete.destroy()
                pop_up_delete.update()
                
            def delete_record():
                shopping_order = (item[0],)
                sql = 'DELETE FROM shopping_order WHERE order_id=?'
                self.delete(sql, shopping_order)
                
                select()
                pop_up_delete.destroy()
            
            cancel_button = tk.Button(work_frame, text='Cancel', width=10, command=cancel_delete).pack(side='bottom')
            ok_button = tk.Button(work_frame, text='Ok', width=10, command=delete_record).pack(side='bottom')
            
            r_x = self.root.winfo_x() + self.root.winfo_width()/2
            r_y = self.root.winfo_y() + self.root.winfo_height()/2
            pop_up_delete.geometry(f"300x400+{int(r_x)-150}+{int(r_y)-200}")
            
            
        def update_clicked():
            # Making update window that has entry fields already filled in with what record the user selected by cursor on table
            status_var_update = tk.StringVar()
            date_sent_var_update = tk.StringVar()  
            date_delivered_var_update = tk.StringVar()
            customer_id_var_update = tk.StringVar()
        
            pop_up_update = tk.Toplevel()
            pop_up_update.title('Update Record')
            work_frame = tk.Frame(pop_up_update, padx=10, pady=10)
            work_frame.pack(side='left', fill='both', expand=True)
            self.set_active(pop_up_update)
            
            # Item = dictionary of keys and tuples, one of which is values and is retrieved below
            item = shopping_order_table.item(shopping_order_table.focus()).get('values')
            
            # Id label uneditable
            id_label = tk.Label(work_frame, text=f'Id: {item[0]}').pack(side='top', pady=5)
            
            # Supplier name retrieved then placed in entry box being editable by user
            # Same done for date_delivered and customer_id
            status_var_update.set(item[1])
            status_label = tk.Label(work_frame, text='Status: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            status_entry = tk.Entry(work_frame, textvariable=status_var_update).pack(side='top', pady=5, fill='both')
            
            date_sent_var_update.set(item[2])
            date_sent_label = tk.Label(work_frame, text='Date Sent: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            date_sent_entry = tk.Entry(work_frame, textvariable=date_sent_var_update).pack(side='top', pady=5, fill='both')

            date_delivered_var_update.set(item[3])
            date_delivered_label = tk.Label(work_frame, text='Date Delivered: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            date_delivered_entry = tk.Entry(work_frame, textvariable=date_delivered_var_update).pack(side='top', pady=5, fill='both')

            customer_id_var_update.set(item[4])
            customer_id_label = tk.Label(work_frame, text='Customer ID: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            customer_id_entry = tk.Entry(work_frame, textvariable=customer_id_var_update).pack(side='top', pady=5, fill='both')
             
            def save_updated_item():
                # Once save button clicked - update process takes place
                shopping_order = (
                    status_var_update.get(),
                    date_sent_var_update.get(),
                    date_delivered_var_update.get(),
                    customer_id_var_update.get(),
                    item[0]
                )
                sql = 'UPDATE shopping_order SET status = ?, date_sent = ?, date_delivered = ?, customer_id = ? WHERE order_id = ?'
                self.update(sql, shopping_order)
                
                select()
                pop_up_update.destroy()
                
            def cancel_update():
                pop_up_update.destroy()
                pop_up_update.update()
                
            cancel_button = tk.Button(work_frame, text='Cancel', width=10, command=cancel_update).pack(side='bottom')
            save_button = tk.Button(work_frame, text='Save', width=10, command=save_updated_item).pack(side='bottom')

            r_x = self.root.winfo_x() + self.root.winfo_width()/2
            r_y = self.root.winfo_y() + self.root.winfo_height()/2
            pop_up_update.geometry(f"300x350+{int(r_x)-150}+{int(r_y)-175}") 
            
            
        delete_button = tk.Button(result_set_frame, text='Delete', width=15, command=delete_clicked)
        delete_button.pack(anchor="e", side="bottom")
        update_button = tk.Button(result_set_frame, text='Update', width=15, command=update_clicked)
        update_button.pack(anchor="e", side="bottom")
              
        status_label = tk.Label(search_criteria_frame, text='Status: ').pack(side='top')
        status_entry = tk.Entry(search_criteria_frame, textvariable=status_var).pack(side='top')
        
        date_sent_label = tk.Label(search_criteria_frame, text='Date Sent: ').pack(side='top')
        date_sent_entry = tk.Entry(search_criteria_frame, textvariable=date_sent_var).pack(side='top')

        date_delivered_label = tk.Label(search_criteria_frame, text='Date Delivered: ').pack(side='top')
        date_delivered_entry = tk.Entry(search_criteria_frame, textvariable=date_delivered_var).pack(side='top')

        customer_id_label = tk.Label(search_criteria_frame, text='Customer ID: ').pack(side='top')
        customer_id_entry = tk.Entry(search_criteria_frame, textvariable=customer_id_var).pack(side='top')
        
        cancel_button = tk.Button(search_criteria_frame, text='Cancel', width=10, command=lambda:[self.clean_right_frame(), self.enabled_insert_select()])
        cancel_button.pack(side = "bottom")
        select_button = tk.Button(search_criteria_frame, text='Select', width=10, command=select)
        select_button.pack(side='bottom')