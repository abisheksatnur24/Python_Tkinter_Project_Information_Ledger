from cgitb import text
from tkinter import *
from turtle import update, width 
from PIL import ImageTk, Image
import sqlite3

#Creating root and configuring it
root = Tk()
root.title('Database Ledger')
root.iconbitmap('C:/Users/abish/OneDrive/Desktop/Code/Information_Ledger/book_icon.ico')
root.geometry("350x600")

#Creating the database and after initial creation just connects to the already made database
db = sqlite3.connect("information_ledger.db")

#Creating cursor for database
cursr = db.cursor()

#Creating table for database if not already created  
'''
Commented out as table has been created already

cursr.execute("""CREATE TABLE information   
    (first_name text,
    last_name text,
    address text,
    city text,
    state text,
    zipcode integer,
    username text,
    password text
    )
""")

'''
#FUNCTIONS FOR BUTTONS BEGIN HERE

#Creating SUBMIT FUNCTION for submit button
def submit():

    #Connect to database & create cursor
    db = sqlite3.connect('information_ledger.db')
    cursr = db.cursor()

    #Insert user data into information table in the information_ledger database
    #Made use of pseudo-variables and python dictionary to place values into the database
    cursr.execute("INSERT INTO information VALUES(:f_name, :l_name, :address, :city, :state, :zipcode, :username, :password)", 
        {
            'f_name' : f_name.get(),
            'l_name' : l_name.get(), 
            'address' : address.get(),
            'city' : city.get(),
            'state' : state.get(),
            'zipcode' : zipcode.get(),
            'username' : username.get(),
            'password' : password.get()
        }
    )


    #clear textboxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)
    username.delete(0, END)
    password.delete(0, END)

    #Commit & Close database
    db.commit()
    db.close()


#Creating QUERY FUNCTION for query button
def query():
    #Connect to database & create cursor
    db = sqlite3.connect('information_ledger.db')
    cursr = db.cursor()

    #Query the DB
    cursr.execute("SELECT *, oid FROM information")
    records = cursr.fetchall()

    #Displays records in terminal 
    print(records)

    #Reads each record and outputs it into the terminal
    print_records = ''
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + "\t" + str(record[8]) + "\n"

    #Displays first_name last_name and oid on window    
    query_label = Label(root, text=print_records)
    query_label.grid(row=10, column=0, columnspan=2)
    

    #Commit & Close database
    db.commit()
    db.close()

#Creating DELETE FUNCTION for DELETE button
def delete():
    #Connect to database & create cursor
    db = sqlite3.connect('information_ledger.db')
    cursr = db.cursor()

    #Delete functionality
    cursr.execute("DELETE from information WHERE oid = " + delete_box.get())

    delete_box.delete(0, END)
    

    #Commit & Close database
    db.commit()
    db.close()

#Creating UPDATE FUNCTION for UPDATE button in EDIT FUNCTION 
def update():
    #Connect to database & create cursor
    db = sqlite3.connect('information_ledger.db')
    cursr = db.cursor()

    #Updating the records
    record_id = delete_box.get()
    cursr.execute("""UPDATE information SET 
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode, 
        username = :username,
        password = :password

        WHERE oid = :oid """, 
        {
            'first' : f_name_editor.get(),
            'last' : l_name_editor.get(),
            'address' : address_editor.get(),
            'city' :  city_editor.get(),
            'state' : state_editor.get(),
            'zipcode' : zipcode_editor.get(),
            'username' : username_editor.get(),
            'password' : password_editor.get(),
            'oid' : record_id
        }
    )

    #Commit & Close database
    db.commit()
    db.close()
    #Closing editor window once button is pressed
    editor.destroy()


#Creating EDIT FUNCTION for EDIT button
def edit():
    #Creating a new editor window
    global editor
    editor = Tk()
    editor.title("Update a Record")
    editor.geometry("400x600")

    #Connect to database & create cursor
    db = sqlite3.connect('information_ledger.db')
    cursr = db.cursor()

    record_id = delete_box.get()
    #Query the DB
    cursr.execute("SELECT * FROM information WHERE oid = " + record_id)
    records = cursr.fetchall()
    #Reads the intended record and prints it into the the entry boxes
    print_records = ''
    '''for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])
        username_editor.insert(0, record[6])
        password_editor.insert(0, record[7])'''

    

    #Commit & Close database
    db.commit()
    db.close()



    #Creating text box labels to aid users
    f_name_label = Label(editor, text="First Name")
    f_name_label.grid(row=0, column=0, padx=20, pady=(10, 0))

    l_name_label = Label(editor, text="Last Name")
    l_name_label.grid(row=1, column=0)

    address_label = Label(editor, text="Address")
    address_label.grid(row=2, column=0)

    city_label = Label(editor, text="City")
    city_label.grid(row=3, column=0)

    state_label = Label(editor, text="State")
    state_label.grid(row=4, column=0)

    zipcode_label = Label(editor, text="Zipcode")
    zipcode_label.grid(row=5, column=0)

    username_label = Label(editor, text="Username")
    username_label.grid(row=6, column=0)

    password_label = Label(editor, text="Password")
    password_label.grid(row=7, column=0)

    #Creating global variables
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor
    global username_editor
    global password_editor

    #Creating text boxes for data update
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady = (10,0))

    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)

    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2,column=1)

    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1)

    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1)

    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1)

    username_editor = Entry(editor, width=30)
    username_editor.grid(row=6, column=1)

    password_editor = Entry(editor, width=30)
    password_editor.grid(row=7, column=1)

    #Creating submit button and placing it on grid
    edit_btn = Button(editor, text="Update record to information ledger", command=update)
    edit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=90 )

    #Reads the intended record and prints it into the the entry boxes
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])
        username_editor.insert(0, record[6])
        password_editor.insert(0, record[7])



#GUI BEGINS FROM HERE 


#Creating text box labels to instruct user what to input in each text box
f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0, padx=20, pady=(10, 0))

l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)

address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)

city_label = Label(root, text="City")
city_label.grid(row=3, column=0)

state_label = Label(root, text="State")
state_label.grid(row=4, column=0)

zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)

username_label = Label(root, text="Username")
username_label.grid(row=6, column=0)

password_label = Label(root, text="Password")
password_label.grid(row=7, column=0)


#Creating text boxes for data entry
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady = (10,0))

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)

address = Entry(root, width=30)
address.grid(row=2,column=1)

city = Entry(root, width=30)
city.grid(row=3, column=1)

state = Entry(root, width=30)
state.grid(row=4, column=1)

zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1)

username = Entry(root, width=30)
username.grid(row=6, column=1)

password = Entry(root, width=30)
password.grid(row=7, column=1)

#Creating submit button and placing it on grid
submit_btn = Button(root, text="Add record to information ledger", command=submit)

submit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

#Creating query button to display database and placing on grid
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=9, column=0, columnspan=2, pady=15, padx=10, ipadx=100)

#Creating delete label, delete box and delete button to remove record from database 
delete_label = Label(root, text="Enter ID: ")
delete_label.grid(row=12, column=0, columnspan=1, pady=(15, 0), padx=10)
delete_box = Entry(root, width=30)
delete_box.grid(row=12, column=1, columnspan=1, pady=(15, 0), padx=10)
delete_btn = Button(root, text="Enter OID and Delete record", command=delete)
delete_btn.grid(row=13, column=0, columnspan=2, pady=5, padx=10, ipadx=64)

#Creating an update button
edit_btn = Button(root, text="Enter OID and Edit record", command=edit)
edit_btn.grid(row=14, column=0, columnspan=2, pady=5, padx=10, ipadx=71)

#Committing changes & closing connection to db; running root 
db.commit()
db.close()
root.mainloop()

#print command to check that everything runs smoothly and till the end
print("hello world")