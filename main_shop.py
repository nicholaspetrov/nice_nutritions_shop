'''
Database Tkinter Project dubbed Nicks Nice Nutritions
Nick Petrov
'''

from cgitb import text
from doctest import master
import tkinter as tk
from tkinter import CENTER, Canvas, Scrollbar, ttk
import sqlite3
from sqlite3 import Error
from page import Page
from supplier import SupplierPage
from product import ProductPage
from customer import CustomerPage
from shopping_order import ShoppingOrderPage


# Notebook made with tabs constructed
class MainApplication(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        notebook = ttk.Notebook()

        supplier_frame = SupplierPage(parent=notebook, root=root)
        product_frame = ProductPage(parent=notebook, root=root)
        customer_frame = CustomerPage(parent=notebook, root=root)
        shopping_order_frame = ShoppingOrderPage(parent=notebook, root=root)

        notebook.add(supplier_frame, text='Supplier')
        notebook.add(product_frame, text='Product')
        notebook.add(customer_frame, text='Customer')
        notebook.add(shopping_order_frame, text='Shopping Order')
        notebook.pack(fill='both', expand=True)

if __name__ == "__main__":
    
    # First window displaying things to look out for
    intro = tk.Tk()
    text = '''
    
    Welcome to Nicks Nice Nutritions!
    
    
    A few tips as you use the application:
    
    - In order to update or delete any records, you have to manually 
    click the individual record on the table
    
    - Inputting nothing in all the field entry boxes will result 
    in the entire table being selected

    '''
    label = tk.Label(intro, text=text).pack()
    ok_button = tk.Button(intro, text='Ok', width=10, command=intro.destroy).pack(side='bottom')
    
    intro_width = 400
    intro_height = 240
    ws = intro.winfo_screenwidth() 
    hs = intro.winfo_screenheight() 
    x = (ws/2) - (intro_width/2)
    y = (hs/2) - (intro_height/2)
    intro.geometry('%dx%d+%d+%d' % (intro_width, intro_height, x, y))
    intro.resizable(False, False)
    intro.title('Introduction to Nicks Nice Nutritions')
    intro.mainloop()
    
    # Application window
    root = tk.Tk()
    MainApplication(root).pack()
    width = 800
    height = 600
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 
    x = (ws/2) - (width/2)
    y = (hs/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.title('Nicks Nice Nutritions')
    root.mainloop()