from cgitb import text
import tkinter as tk
from tkinter import CENTER, Canvas, Scrollbar, ttk
import sqlite3
from sqlite3 import Error
from page import Page


class ProductPage(Page):
    
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, *args, **kwargs) 
        self.root = root

    def create_insert_window(self):
        
        self.clean_right_frame()
        # Insert button now unclickable until actions done on insert window completed
        self.insert_button['state'] = tk.DISABLED
        
        work_frame = tk.Frame(self.right_frame)#, background='green')
        work_frame.pack(anchor='w', side='top', padx=5)
        
        
        # For retrieving what was written in entry boxes
        supplier_id_var = tk.StringVar()  
        product_name_var = tk.StringVar()  
        retail_price_var = tk.StringVar()
        stock_level_var = tk.StringVar()
        product_code_var = tk.StringVar()
        supplier_price_var = tk.StringVar()
        
        def insert():
            self.disabled_insert()
            # Object formed to be passed through self.insert() with sql statement
            product = (
                supplier_id_var.get(),
                product_name_var.get(),
                retail_price_var.get(),
                stock_level_var.get(),
                product_code_var.get(),
                supplier_price_var.get()
            )
            sql = 'INSERT INTO PRODUCT(supplier_id, product_name, retail_price, stock_level, product_code, supplier_price) VALUES(?, ?, ?, ?, ?, ?)'
            id = self.insert(sql, product)
            
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
        supplier_id_label = tk.Label(work_frame, text='Supplier ID: ').pack(side='top')
        supplier_id_entry = tk.Entry(work_frame, textvariable=supplier_id_var).pack(side='top')
        
        product_name_label = tk.Label(work_frame, text='Product Name: ').pack(side='top')
        product_name_entry = tk.Entry(work_frame, textvariable=product_name_var).pack(side='top')

        retail_price_label = tk.Label(work_frame, text='Retail Price: ').pack(side='top')
        retail_price_entry = tk.Entry(work_frame, textvariable=retail_price_var).pack(side='top')

        stock_level_label = tk.Label(work_frame, text='Stock Level: ').pack(side='top')
        stock_level_entry = tk.Entry(work_frame, textvariable=stock_level_var).pack(side='top')
        
        product_code_label = tk.Label(work_frame, text='Product Code: ').pack(side='top')
        product_code_entry = tk.Entry(work_frame, textvariable=product_code_var).pack(side='top')

        supplier_price_label = tk.Label(work_frame, text='Supplier Price: ').pack(side='top')
        supplier_price_entry = tk.Entry(work_frame, textvariable=supplier_price_var).pack(side='top')
        
        
        insert_button = tk.Button(work_frame, text='Insert', width=10, command=insert)
        insert_button.pack(side='top')
        
        cancel_button = tk.Button(work_frame, text='Cancel', width=10, command=lambda:[self.clean_right_frame(), self.enabled_insert_select()])
        cancel_button.pack(side='top')
    
    def create_select_window(self):
        self.clean_right_frame()
        self.select_button['state'] = tk.DISABLED
        
        # Result set and search criteria frame established in right frame parent 
        result_set_frame = tk.Frame(self.right_frame)
        result_set_frame.pack(side='right', fill="both", expand=True, padx=5)

        search_criteria_frame = tk.Frame(self.right_frame)
        search_criteria_frame.pack(anchor='n', side='top', padx=5)
         
        scrollbar = Scrollbar(result_set_frame)
        scrollbar.pack(side='right', fill=tk.Y)
        
        scrollbar = Scrollbar(result_set_frame, orient='horizontal')
        scrollbar.pack(side='bottom', fill=tk.X)
        
        product_table = ttk.Treeview(
            result_set_frame, 
            yscrollcommand=scrollbar.set,
            xscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        
        product_table.pack(fill='both')
        scrollbar.config(command=product_table.yview)
        scrollbar.config(command=product_table.xview)
        
        product_table['columns'] = ('product_id', 'supplier_id', 'product_name', 'retail_price', 'stock_level', 'product_code', 'supplier_price')
        
        product_table.column("#0", width=0,  stretch=tk.NO)
        product_table.column("product_id",anchor='w', width=80)
        product_table.column("supplier_id",anchor='w', width=80)
        product_table.column("product_name",anchor='w', width=80)
        product_table.column("retail_price",anchor='w', width=80)
        product_table.column("stock_level",anchor='w', width=80)
        product_table.column("product_code",anchor='w', width=80)
        product_table.column("supplier_price",anchor='w', width=80)
        
        product_table.heading("#0", text='',  anchor=tk.CENTER)
        product_table.heading("product_id",text="Product Id",anchor=tk.CENTER)
        product_table.heading("supplier_id",text="Supplier Id",anchor=tk.CENTER)
        product_table.heading("product_name",text="Product Name",anchor=tk.CENTER)
        product_table.heading("retail_price",text="Retail Price",anchor=tk.CENTER)
        product_table.heading("stock_level",text="Stock Level",anchor=tk.CENTER)
        product_table.heading("product_code",text="Product Code",anchor=tk.CENTER)
        product_table.heading("supplier_price",text="Supplier Price",anchor=tk.CENTER)
        
        supplier_id_var = tk.StringVar()  
        product_name_var = tk.StringVar()  
        retail_price_var = tk.StringVar()
        stock_level_var = tk.StringVar()
        product_code_var = tk.StringVar()
        supplier_price_var = tk.StringVar()

        def select():
            self.disable_select()
            # Table restarts - Empties table if full
            product_table.delete(*product_table.get_children())
            
            supplier_id = supplier_id_var.get()
            product_name = product_name_var.get()
            retail_price = retail_price_var.get()
            stock_level = stock_level_var.get()
            product_code = product_code_var.get()
            supplier_price = supplier_price_var.get()
            
            # Use of wildcards
            # Object (product) formed to be passed through self.select() with sql statement
            product = (
                supplier_id or '%',
                product_name or '%',
                retail_price or '%',
                stock_level or '%',
                product_code or '%',
                supplier_price or '%'
            )

            sql = 'SELECT * FROM PRODUCT WHERE supplier_id like ? AND product_name like ? AND retail_price like ? AND stock_level like ? AND product_code like ? AND supplier_price like ?'
            rows = self.select(sql, product)
            
            counter = 0
            # Rows returned from self.select() iterated through and inserted into product_table made in lines 159-187
            for row in rows:
                product_table.insert(
                    parent='',
                    index='end',
                    iid=counter,
                    text='',
                    values = row
                )
                counter += 1
            # If no rows are present in table after specific selection was requested
            # Error message appears and selection process repeats
            if len(product_table.get_children()) == 0:
                pop_up_none = tk.Toplevel()
                r_x = self.root.winfo_x() + self.root.winfo_width()/2
                r_y = self.root.winfo_y() + self.root.winfo_width()/2
                pop_up_none.geometry(f"300x70+{int(r_x)-150}+{int(r_y)-35}") 
                message = tk.Label(pop_up_none, text='ERROR: No records found').pack(side='top')
                button = tk.Button(pop_up_none, text='OK', command=pop_up_none.destroy).pack(side='bottom')
            else:
                product_table.pack(expand=True)
            
        def delete_clicked():
            pop_up_delete = tk.Toplevel()
            pop_up_delete.title('Delete Record')
            work_frame = tk.Frame(pop_up_delete, padx=10, pady=10)
            work_frame.pack(side='left', fill='both', expand=True)
            self.set_active(pop_up_delete)
            
            item = product_table.item(product_table.focus()).get('values')
            confirmation = tk.Label(work_frame, text='Are you sure you want to delete this record?').pack(side='top', pady=5)
            id_label = tk.Label(work_frame, text=f'Id: {item[0]}').pack(side='top', pady=5)
            
            supplier_id_label = tk.Label(work_frame, text='Supplier ID: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            supplier_id_label_value = tk.Label(work_frame, text=item[1]).pack(side='top', pady=5)
            
            product_label = tk.Label(work_frame, text='Product Name: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            product_label_value = tk.Label(work_frame, text=item[2]).pack(side='top', pady=5)
            
            retail_price_label = tk.Label(work_frame, text='Retail Price: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            retail_price_label_value = tk.Label(work_frame, text=item[3]).pack(side='top', pady=5)
            
            stock_level_label = tk.Label(work_frame, text='Stock Level: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            stock_level_value = tk.Label(work_frame, text=item[4]).pack(side='top', pady=5)
            
            product_code_label = tk.Label(work_frame, text='Product Code: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            product_code_label_value = tk.Label(work_frame, text=item[5]).pack(side='top', pady=5)
            
            supplier_price_label = tk.Label(work_frame, text='Supplier Price: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            supplier_price_label_value = tk.Label(work_frame, text=item[6]).pack(side='top', pady=5)
            
            def cancel_delete():
                pop_up_delete.destroy()
                pop_up_delete.update()
                
            def delete_record():
                product = (item[0],)
                sql = 'DELETE FROM PRODUCT WHERE product_id=?'
                self.delete(sql, product)
                
                select()
                pop_up_delete.destroy()
            
            cancel_button = tk.Button(work_frame, text='Cancel', width=10, command=cancel_delete).pack(side='bottom')
            ok_button = tk.Button(work_frame, text='Ok', width=10, command=delete_record).pack(side='bottom')
            
            r_x = self.root.winfo_x() + self.root.winfo_width()/2
            r_y = self.root.winfo_y() + self.root.winfo_height()/2
            pop_up_delete.geometry(f"300x510+{int(r_x)-150}+{int(r_y)-255}")
            
            
        def update_clicked():
            # Making update window that has entry fields already filled in with what record the user selected by cursor on table
            supplier_id_var_update = tk.StringVar()
            product_name_var_update = tk.StringVar()  
            retail_price_var_update = tk.StringVar()
            stock_level_var_update = tk.StringVar()
            product_code_var_update = tk.StringVar()
            supplier_price_var_update = tk.StringVar()
            
            pop_up_update = tk.Toplevel()
            pop_up_update.title('Update Record')
            work_frame = tk.Frame(pop_up_update, padx=10, pady=10)
            work_frame.pack(side='left', fill='both', expand=True)
            self.set_active(pop_up_update)
            
            # Item = dictionary of keys and tuples, one of which is values and is retrieved below
            item = product_table.item(product_table.focus()).get('values')
            
            # Id label uneditable
            id_label = tk.Label(work_frame, text=f'Id: {item[0]}').pack(side='top', pady=5)
            
            # Supplier name retrieved then placed in entry box being editable by user
            # Same done for retail_price and stock_level
            supplier_id_var_update.set(item[1])
            supplier_id_label = tk.Label(work_frame, text='Supplier ID: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            supplier_id_entry = tk.Entry(work_frame, textvariable=supplier_id_var_update).pack(side='top', pady=5, fill='both')
            
            product_name_var_update.set(item[2])
            product_label = tk.Label(work_frame, text='Product Name: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            product_entry = tk.Entry(work_frame, textvariable=product_name_var_update).pack(side='top', pady=5, fill='both')

            retail_price_var_update.set(item[3])
            retail_price_label = tk.Label(work_frame, text='Retail Price: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            retail_price_entry = tk.Entry(work_frame, textvariable=retail_price_var_update).pack(side='top', pady=5, fill='both')

            stock_level_var_update.set(item[4])
            stock_level_label = tk.Label(work_frame, text='Stock Level: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            stock_level_entry = tk.Entry(work_frame, textvariable=stock_level_var_update).pack(side='top', pady=5, fill='both')
            
            product_code_var_update.set(item[5])
            product_code_label = tk.Label(work_frame, text='Product Code: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            product_Code_entry = tk.Entry(work_frame, textvariable=product_code_var_update).pack(side='top', pady=5, fill='both')

            supplier_price_var_update.set(item[6])
            supplier_price_label = tk.Label(work_frame, text='Supplier Price: ', font='Helvetica 9 bold').pack(side='top', pady=5)
            supplier_price_entry = tk.Entry(work_frame, textvariable=supplier_price_var_update).pack(side='top', pady=5, fill='both')
            
            def save_updated_item():
                # Once save button clicked - update process takes place
                product = (
                    product_name_var_update.get(),
                    retail_price_var_update.get(),
                    stock_level_var_update.get(),
                    product_code_var_update.get(),
                    supplier_price_var_update.get(),
                    item[0]
                )
                sql = 'UPDATE PRODUCT SET product_name = ?, retail_price = ?, stock_level = ?, product_code = ?, supplier_price = ? WHERE product_id = ?'
                self.update(sql, product)
                
                select()
                pop_up_update.destroy()
                
            def cancel_update():
                pop_up_update.destroy()
                pop_up_update.update()
                
            cancel_button = tk.Button(work_frame, text='Cancel', width=10, command=cancel_update).pack(side='bottom')
            save_button = tk.Button(work_frame, text='Save', width=10, command=save_updated_item).pack(side='bottom')

            r_x = self.root.winfo_x() + self.root.winfo_width()/2
            r_y = self.root.winfo_y() + self.root.winfo_height()/2
            pop_up_update.geometry(f"300x500+{int(r_x)-150}+{int(r_y)-250}") 
            
            
        delete_button = tk.Button(result_set_frame, text='Delete', width=15, command=delete_clicked)
        delete_button.pack(anchor="e", side="bottom")
        update_button = tk.Button(result_set_frame, text='Update', width=15, command=update_clicked)
        update_button.pack(anchor="e", side="bottom")
              
        supplier_id_label = tk.Label(search_criteria_frame, text='Supplier ID: ').pack(side='top')
        supplier_id_entry = tk.Entry(search_criteria_frame, textvariable=supplier_id_var).pack(side='top')
        
        product_label = tk.Label(search_criteria_frame, text='Product Name: ').pack(side='top')
        product_entry = tk.Entry(search_criteria_frame, textvariable=product_name_var).pack(side='top')

        retail_price_label = tk.Label(search_criteria_frame, text='Retail Price: ').pack(side='top')
        retail_price_entry = tk.Entry(search_criteria_frame, textvariable=retail_price_var).pack(side='top')

        stock_level_label = tk.Label(search_criteria_frame, text='Stock Level: ').pack(side='top')
        stock_level_entry = tk.Entry(search_criteria_frame, textvariable=stock_level_var).pack(side='top')
        
        product_code_label = tk.Label(search_criteria_frame, text='Product Code: ').pack(side='top')
        product_code_entry = tk.Entry(search_criteria_frame, textvariable=product_code_var).pack(side='top')

        supplier_price_label = tk.Label(search_criteria_frame, text='Supplier Price: ').pack(side='top')
        supplier_price_entry = tk.Entry(search_criteria_frame, textvariable=supplier_price_var).pack(side='top')

        cancel_button = tk.Button(search_criteria_frame, text='Cancel', width=10, command=lambda:[self.clean_right_frame(), self.enabled_insert_select()])
        cancel_button.pack(side = "bottom")
        select_button = tk.Button(search_criteria_frame, text='Select', width=10, command=select)
        select_button.pack(side='bottom')