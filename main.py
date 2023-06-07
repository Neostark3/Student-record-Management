import io
from tkinter import *
from datetime import date
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import sqlite3 as sq
# pillow needed to be installed to run the program
conn = sq.connect('Database/Reports.db')
c = conn.cursor()

background = "#06283D"
color2 = "#EDEDED"
color3 = "#06283D"
img = []
row = []


# function to exit the window
def closing():
    root.destroy()


# function to print student details on a text page
def print_details():
    roll = reg_entry.get()

    if roll:
        try:
            # Retrieve the student details from the database
            q = "SELECT * FROM students WHERE id = ?"
            values = (roll,)
            c.execute(q, values)
            record = c.fetchone()

            if record:
                filename = "Student_" + roll + ".txt"
                # Open a text file in write mode
                with open(filename, "w") as file:
                    # Write the student details to the file
                    file.write(f"Roll: {record[0]}\n")
                    file.write(f"Name: {record[1]}\n")
                    file.write(f"Gender: {record[2]}\n")
                    file.write(f"Mobile: {record[3]}\n")
                    file.write(f"Website: {record[4]}\n")
                    file.write(f"DOB: {record[5]}\n")
                    file.write(f"Address: {record[6]}\n")
                    file.write(f"Email: {record[7]}\n")
                    file.write(f"Remarks: {record[8]}\n")

                messagebox.showinfo("Success", "Student details printed successfully!")
            else:
                messagebox.showwarning("Warning", "No record found for the given roll number.")
        except sq.Error as e:
            messagebox.showerror("Error", "Failed to retrieve student details: " + str(e))
    else:
        messagebox.showwarning("Warning", "Please enter a valid roll number.")


# function to insert student record to the database
def insert():
    roll = int(Id.get())
    name = name_entry.get()
    gender = "Male" if radio.get() == 1 else "Female"
    mobile = mob_entry.get()
    website = web_entry.get()
    dob = dob_entry.get()
    address = add_entry.get()
    email = mail_entry.get()
    remarks = mark_entry.get()

    # Check if all required fields are provided
    if not roll or not name or not mobile or not dob:
        messagebox.showerror("Error", "Please enter all the required fields.")
        return

    # Check if the roll number is unique
    c.execute("SELECT * FROM students WHERE id=?", (roll,))
    if c.fetchone() is not None:
        messagebox.showerror("Error", "Roll number already exists. Please enter a unique roll number.")
        return

    # Check if a photo is uploaded
    # Prompt to insert photo if not already inserted
    if roll:
        # Prompt the user to select a photo file

        try:
            file = filedialog.askopenfilename()
            fob = open(file, 'rb')
            blob_data = fob.read()

            # Insert the record into the database
            q = "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (roll, name, gender, mobile, website, dob, address, email, remarks, blob_data)
            c.execute(q, values)
            conn.commit()

            messagebox.showinfo("Success", "Record inserted successfully!")
            reset_fields()
        except sq.Error as e:
            messagebox.showerror("Error", "Failed to insert record: " + str(e))

    else:
        messagebox.showwarning("Warning", "Please enter a valid roll number.")


# function to update the student record in the database
def update():
    f_roll = int(Id.get())
    f_name = name_entry.get()
    f_gender = "Male" if radio.get() == 1 else "Female"
    f_mobile = mob_entry.get()
    f_website = web_entry.get()
    f_dob = dob_entry.get()
    f_address = add_entry.get()
    f_email = mail_entry.get()
    f_remarks = mark_entry.get()

    # Check if all required fields are provided
    if not f_roll or not f_name or not f_mobile:
        messagebox.showerror("Error", "Please enter all the required fields.")
        return

    # Check if a photo is uploaded
    # Prompt to insert photo if not already inserted
    file = filedialog.askopenfilename()
    fob = open(file, 'rb')
    blob_data = fob.read()

    # Insert the data into the database
    try:
        update_query = "UPDATE students SET name = ?, gender = ?, mobile = ?, website = ?, dob = ?, address = ?, " \
                       "email = ?, remarks = ?, photo = ? WHERE id = ?"
        update_values = (f_name, f_gender, f_mobile, f_website, f_dob, f_address, f_email, f_remarks, blob_data, f_roll)
        c.execute(update_query, update_values)

        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully.")

    except sq.Error as error:
        messagebox.showerror("Error", f"Failed to update record: {error}")

    query()


# function to delete the student record in the database
def delete_record():
    roll = reg_entry.get()

    if roll:
        try:
            # Delete the record from the database
            q = "DELETE FROM students WHERE id = ?"
            values = (roll,)
            c.execute(q, values)
            conn.commit()

            messagebox.showinfo("Success", "Record deleted successfully!")
            reset_fields()
        except sq.Error as e:
            messagebox.showerror("Error", "Failed to delete record: " + str(e))
    else:
        messagebox.showwarning("Warning", "Please enter a valid roll number.")


# function to search the student record from database to display
def query():
    global img, row
    roll = Search_roll.get()

    # Clear previous data
    reg_entry.delete(0, END)
    name_entry.delete(0, END)
    radio.set(0)
    mob_entry.delete(0, END)
    web_entry.delete(0, END)
    dob_entry.delete(0, END)
    age_entry.delete(0, END)
    add_entry.delete(0, END)
    mail_entry.delete(0, END)
    mark_entry.delete(0, END)
    lbl.configure(image="")

    # Check if roll number is provided
    if not roll:
        messagebox.showerror("Error", "Please enter a roll number.")
        return

    # Execute the query to retrieve the student data
    try:
        q = "SELECT * FROM students WHERE id=?"
        c.execute(q, (roll,))
        row = c.fetchone()
    except sq.Error as error:
        messagebox.showerror("Error", f"Failed to find the record: {error}")

    if row:
        # Set the values in the respective text boxes
        reg_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        radio.set(1 if row[2] == "Male" else 2)
        mob_entry.insert(0, row[3])
        web_entry.insert(0, row[4])
        dob_entry.insert(0, row[5])
        add_entry.insert(0, row[6])
        mail_entry.insert(0, row[7])
        mark_entry.insert(0, row[8])

        dob = dob_entry.get()
        dob_day, dob_month, dob_year = map(int, dob.split("/"))
        current_date = date.today()
        age = current_date.year - dob_year

        # Adjust the age if the current date is before the birth month/day
        if current_date.month < dob_month or (current_date.month == dob_month and current_date.day < dob_day):
            age -= 1
        age_entry.config(state="normal")
        age_entry.delete(0, "end")
        age_entry.insert(0, str(age))

        # Retrieve and display the image if available
        if row[9] is not None:
            #img = ImageTk.PhotoImage(data=row[9])
            #lbl.config(image=img)
            image_data = row[9]
            image = Image.open(io.BytesIO(image_data))

            # Resize the image to fit the desired dimensions
            desired_width = 256  # Set your desired width here
            desired_height = 256  # Set your desired height here
            image = image.resize((desired_width, desired_height), Image.LANCZOS)

            # Convert the resized image to PhotoImage format
            img = ImageTk.PhotoImage(image)

            # Update the image in the lbl widget
            lbl.config(image=img)

        else:
            messagebox.showinfo("Information", "No photo found for the given roll number.")
    else:
        messagebox.showinfo("Information", "No data found for the given roll number.")


# Function to reset all the fields
def reset_fields():
    reg_entry.delete(0, END)
    name_entry.delete(0, END)
    radio.set(0)
    mob_entry.delete(0, END)
    web_entry.delete(0, END)
    dob_entry.delete(0, END)
    age_entry.delete(0, END)
    add_entry.delete(0, END)
    mail_entry.delete(0, END)
    mark_entry.delete(0, END)
    lbl.configure(image="")


# function to calculate age
def calculate_age(dob):
    # Split the DOB into day, month, and year
    dob_day, dob_month, dob_year = map(int, dob.split("/"))

    # Get the current date
    current_date = date.today()

    # Calculate the age
    age = current_date.year - dob_year

    # Adjust the age if the current date is before the birth month/day
    if current_date.month < dob_month or (current_date.month == dob_month and current_date.day < dob_day):
        age -= 1

    return age


root = Tk()
root.title("Reports")
root.geometry("1200x800+200+100")
root.config(bg=background)
root.resizable(False, False)

# top frames
Label(root, text="Created by: Bighnesh Lenka", width=10, height=3, bg="#f0687c", anchor='e').pack(side=TOP, fill=X)
Label(root, text="Student Records", width=10, height=2, bg="#c36464", fg="#fff", font='arial 20 bold').pack(side=TOP,
                                                                                                            fill=X)

# search box

Search_roll = StringVar()
Entry(root, textvariable=Search_roll, width=15, bd=2, font="arial 16").place(x=850, y=74)
imageicon1 = PhotoImage(file="Images/search_icon.png")
Search = Button(root, text="Search", compound=LEFT, image=imageicon1, width=120, height=30, font="arial 13 bold",
                bg="lightblue", command=query)
Search.place(x=1060, y=71)

# Registration stuff

Label(root, text="Student Roll:", font="arial 13", fg=color2, bg=background).place(x=30, y=150)
Label(root, text="Branch:", font="arial 13", fg=color2, bg=background).place(x=450, y=150)
Label(root, text="MCA", font="arial 13", fg=color2, bg=background).place(x=510, y=150)

Id = StringVar()

reg_entry = Entry(root, textvariable=Id, width=15, font="arial 13")
reg_entry.place(x=130, y=150)

# Student details
obj = LabelFrame(root, text="Student's Details", font=20, bd=2, width=900, bg=color2, fg=color3, height=400,
                 relief=GROOVE)
obj.place(x=30, y=200)

Label(obj, text="Full Name:", font="arial 13", bg=color2, fg=color3).place(x=30, y=60)
Label(obj, text="Gender:", font="arial 13", bg=color2, fg=color3).place(x=30, y=120)
Label(obj, text="Mobile no.:", font="arial 13", bg=color2, fg=color3).place(x=30, y=180)
Label(obj, text="Website:", font="arial 13", bg=color2, fg=color3).place(x=30, y=240)
Label(obj, text="Date of birth:", font="arial 13", bg=color2, fg=color3).place(x=500, y=60)
Label(obj, text="Age:", font="arial 13", bg=color2, fg=color3).place(x=500, y=120)
Label(obj, text="Address:", font="arial 13", bg=color2, fg=color3).place(x=500, y=180)
Label(obj, text="Email-id:", font="arial 13", bg=color2, fg=color3).place(x=500, y=240)
Label(obj, text="Remarks:", font="arial 13", bg=color2, fg=color3).place(x=30, y=300)

Name = StringVar()
name_entry = Entry(obj, textvariable=Name, width=35, font="arial 10")
name_entry.place(x=160, y=63)

radio = IntVar()
R1 = Radiobutton(obj, text="Male", variable=radio, value=1, bg=color2, fg=color3)
R1.place(x=160, y=122)

R2 = Radiobutton(obj, text="Female", variable=radio, value=2, bg=color2, fg=color3)
R2.place(x=220, y=122)

Mobile = StringVar()
mob_entry = Entry(obj, textvariable=Mobile, width=20, font="arial 10")
mob_entry.place(x=160, y=183)

Web = StringVar()
web_entry = Entry(obj, textvariable=Web, width=35, font="arial 10")
web_entry.place(x=160, y=243)

Remark = StringVar()
mark_entry = Entry(obj, textvariable=Remark, width=5, font="arial 10")
mark_entry.place(x=160, y=303)

DOB = StringVar()
dob_entry = Entry(obj, textvariable=DOB, width=20, font="arial 10")
dob_entry.place(x=620, y=63)

Age = StringVar()
age_entry = Entry(obj, textvariable=Age, width=5, font="arial 10", state="readonly")
age_entry.place(x=620, y=123)

Address = StringVar()
add_entry = Entry(obj, textvariable=Address, width=35, font="arial 10")
add_entry.place(x=620, y=183)

Mail = StringVar()
mail_entry = Entry(obj, textvariable=Mail, width=35, font="arial 10")
mail_entry.place(x=620, y=243)

f = Frame(root, bg="white", width=256, height=256, relief=GROOVE)
f.place(x=936, y=130)

imageicon3 = PhotoImage(file="Images/upload photo.png")
lbl = Label(f, bg="white", image=imageicon3)
lbl.place(x=0, y=0)

printBTN = Button(root, text="Print", width=19, height=2, font="arial 12 bold", bg="#317d75", command=print_details)
printBTN.place(x=960, y=440)

exitBTN = Button(root, text="Exit", width=19, height=2, font="arial 12 bold", bg="grey", command=closing)
exitBTN.place(x=960, y=510)

insertBTN = Button(root, text="Insert", width=16, height=2, font="arial 12 bold", bg="lightblue", command=insert)
insertBTN.place(x=40, y=660)

updateBTN = Button(root, text="Update", width=16, height=2, font="arial 12 bold", bg="#52c23e", command=update)
updateBTN.place(x=240, y=660)

resetBTN = Button(root, text="Reset", width=16, height=2, font="arial 12 bold", bg="#db3d52", command=reset_fields)
resetBTN.place(x=440, y=660)

deleteBTN = Button(root, text="Delete", width=16, height=2, font="arial 12 bold", bg="#8c151f", command=delete_record)
deleteBTN.place(x=640, y=660)

root.mainloop()
