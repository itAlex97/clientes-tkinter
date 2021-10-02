import builtins
from sqlite3.dbapi2 import Row
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from typing import Collection

root = Tk()
root.title('CRM')

# Conexion a DB
conn = sqlite3.connect('crm.db')
c = conn.cursor()
c.execute(
    """
    create table if not exists cliente(
        id integer primary key autoincrement,
        nombre text not null,
        telefono text not null,
        empresa text not null
    );
    """
)

# Definición de funciones
def render_client():
    rows = c.execute('select * from cliente').fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', END, row[0], values=(row[1], row[2], row[3]))

def insert(client):
    c.execute(
        """
        insert into cliente (nombre, telefono, empresa) values (?, ?, ?)
        """,
        (client['name'], client['tel'], client['comp'])
    )
    conn.commit()
    render_client()

def new_client():
    def save():
        if not name.get():
            messagebox.showerror('Error', 'Todos los campos son requeridos')
            return
        if not tel.get():
            messagebox.showerror('Error', 'Todos los campos son requeridos')
            return
        if not comp.get():
            messagebox.showerror('Error', 'Todos los campos son requeridos')
            return
        client = {
            'name': name.get(),
            'tel': tel.get(),
            'comp': comp.get()
        }
        insert(client)
        top.destroy()

    top = Toplevel()
    top.title('Nuevo Cliente')

    lname = Label(top, text='Nombre')
    name = Entry(top, width=40)
    lname.grid(row=0, column=0)
    name.grid(row=0, column=1)

    ltel = Label(top, text='Teléfono')
    tel = Entry(top, width=40)
    ltel.grid(row=1, column=0)
    tel.grid(row=1, column=1)

    lcomp = Label(top, text='Empresa')
    comp = Entry(top, width=40)
    lcomp.grid(row=2, column=0)
    comp.grid(row=2, column=1)

    btn_save = Button(top, text='Guardar', command=save)
    btn_save.grid(row=3, column=1)

    top.mainloop()

def del_client():
    id = tree.selection()[0]
    client = c.execute('select * from cliente where id = ?', (id,)).fetchone()
    resp = messagebox.askokcancel('Seguro?', 'Estás seguro de querer eliminar al cliente ' + client[1] + ' de este registro?')
    if resp:
        c.execute('delete from cliente where id = ?', (id,))
        conn.commit()
        render_client()
    else:
        pass

# Creación de componentes
# --------------- Buttons ---------------
btn_add = Button(root, text='Nuevo Cliente', command=new_client)
btn_add.grid(column=0, row=0)

btn_del = Button(root, text='Eliminar Cliente', command=del_client)
btn_del.grid(column=1, row=0)
# --------------- Tree ---------------
tree = ttk.Treeview(root)

tree['columns'] = ('Nombre', 'Telefono', 'Empresa')
tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

tree.heading('Nombre', text='Nombre')
tree.heading('Telefono', text='Teléfono')
tree.heading('Empresa', text='Empresa')
tree.grid(column=0, row=1, columnspan=2)

# --------------- || ---------------
render_client()
root.mainloop()