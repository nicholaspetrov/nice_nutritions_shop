from cgitb import text
from doctest import master
import tkinter as tk
from tkinter import CENTER, Canvas, Scrollbar, ttk
import sqlite3
from sqlite3 import Error

class Page(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs, padx=10, pady=10)
        
        # Left and right frames to be replicated in each individual tab (Supplier Page, Customer Page etc.)
        # Left for buttons and right for search criteria and result set frames
        
        self.db_file = 'sugario.db'     
        
        self.left_frame = tk.Frame(self)# background='blue')
        self.left_frame.pack(side='left', fill='both')
        
        self.insert_button = tk.Button(self.left_frame, text="Insert", command=self.create_insert_window, width=10)
        self.insert_button.pack(anchor="w", side="top")
        self.select_button = tk.Button(self.left_frame, text="Select", command=self.create_select_window, width=10)
        self.select_button.pack(anchor="w", side="top")
        
        self.right_frame = tk.Frame(self)# background='pink')
        self.right_frame.pack(side='right', fill='both', expand=True)   
        
        # welcome = tk.Label(self.right_frame, text='Welcome to Nicks Nice Nutritions').pack()
    
    def clean_right_frame(self):
        for child in self.right_frame.winfo_children():
            child.destroy()
        self.enabled_insert_select()
    
    def create_connection(self):
        # Connection to database established
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        return conn
    
    # Insert, select, update, delete methods used universally by all pages
    def insert(self, sql, obj):
        
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql, obj)
        conn.commit()
        id = cur.lastrowid
        print(f'Record successfully inserted, ID = {id}')
        conn.close()
        return id
    
    def select(self, sql, obj):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql, obj)
        rows = cur.fetchall()
        conn.close()
        return rows
        
    def update(self, sql, obj):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql, obj)
        conn.commit()
        id = cur.lastrowid
        print(f'Record {obj[3]} successfully updated')
        conn.close()
        
    def delete(self, sql, obj):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql, obj)
        conn.commit()
        id = cur.lastrowid
        print(f'Record {obj[0]} successfully deleted')
        conn.close()
        
    # Next 3 methods prevent user from clicking insert and select multiple times
    def disable_select(self):
        self.insert_button['state'] = tk.NORMAL
        self.select_button['state'] = tk.DISABLED
    
    def disabled_insert(self):
        self.insert_button['state'] = tk.DISABLED
        self.select_button['state'] = tk.NORMAL
        
    def enabled_insert_select(self):
        self.insert_button['state'] = tk.NORMAL
        self.select_button['state'] = tk.NORMAL
    
    # For putting focus on external pop up windows such as update, delete and insert
    def set_active(self, win):
        win.lift()
        win.focus_force()
        win.grab_set()
        win.grab_release()
    
    # Overriding functions
    def create_insert_window(self):
        pass

    def create_select_window(self):
        pass

    def show(self):
        self.lift()