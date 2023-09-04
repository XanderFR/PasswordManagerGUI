from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generatePassword():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    passwordLetters = [choice(letters) for _ in range(randint(8, 10))]  # Make a list of 8 to 10 random letters
    passwordSymbols = [choice(symbols) for _ in range(randint(2, 4))]  # Make a list of 2 to 4 random symbols
    passwordNumbers = [choice(numbers) for _ in range(randint(2, 4))]  # Make a list of 2 to 4 random numbers

    passwordList = passwordLetters + passwordSymbols + passwordNumbers  # Combine the character lists
    shuffle(passwordList)  # Shuffle all the characters of passwordList around

    password = "".join(passwordList)  # Combine all the characters of passwordList together with nothing in between them and store the result in "password" variable
    passwordEntry.delete(0, END)  # Deletes any preexisting contents in the passwordEntry field
    passwordEntry.insert(0, password)  # Puts the produced password into the passwordEntry field
    pyperclip.copy(password)  # Save the password to the computer clipboard, like highlighting password and pressing ctrl+c


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    # Retrieve the data from the entry fields
    website = websiteEntry.get()
    email = emailEntry.get()
    password = passwordEntry.get()

    # Prepare password information in JSON format
    newData = {
        website: {
            "Email": email,
            "Password": password
        }
    }

    if len(website) == 0 or len(password) == 0:  # Ensure website and password fields aren't empty
        messagebox.showinfo(title="Oops", message="Please make sure the fields aren't empty.")

    else:  # If all the fields have something in them
        try:
            # Open the data file if it exists
            with open("data.json", "r") as dataFile:
                # Program tries to read the old data
                data = json.load(dataFile)

        except FileNotFoundError:  # If data.json does not exist already
            with open("data.json", "w") as dataFile:  # Create the file
                json.dump(newData, dataFile, indent=4)  # And add data to it

        else:  # Runs if try block above was successful, if data.json does exist already
            # Updating old data with new data
            data.update(newData)

            with open("data.json", "w") as dataFile:
                # Saving updated data
                json.dump(data, dataFile, indent=4)  # Save the updated password JSON information to the data file
        finally:
            websiteEntry.delete(0, END)  # Delete everything in the websiteEntry field
            passwordEntry.delete(0, END)  # Delete everything in the passwordEntry field


# ---------------------------- FIND PASSWORD ------------------------------- #
def findPassword():
    website = websiteEntry.get()  # Take the website from within the websiteEntry field
    try:
        with open("data.json") as dataFile:  # Open the data.json file
            data = json.load(dataFile)  # Store data (dictionary) in "data" variable
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")

    else:
        if website in data:
            email = data[website]["Email"]  # Find the website's name in the dictionary and grab its email value
            password = data[website]["Password"]  # Find the website's name in the dictionary and grab its password value
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")
# ---------------------------- UI SETUP ------------------------------- #
# The general window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=20)

# The "MyPass" Lock Logo
canvas = Canvas(height=200, width=200)
logoImg = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logoImg)  # The placement of the logo image in the canvas
canvas.grid(row=0, column=1)

# The Labels
websiteLabel = Label(text="Website:")
websiteLabel.grid(row=1, column=0)
emailLabel = Label(text="Email / Username:")
emailLabel.grid(row=2, column=0)
passwordLabel = Label(text="Password:")
passwordLabel.grid(row=3, column=0)

# The Entry Fields
websiteEntry = Entry(width=33)
websiteEntry.grid(row=1, column=1)
websiteEntry.focus()  # Puts blinking cursor in the websiteEntry field
emailEntry = Entry(width=52)
emailEntry.grid(row=2, column=1, columnspan=2)
emailEntry.insert(0, "TestEmail@gmail.com")  # At index 0 of the emailEntry field, insert email address
passwordEntry = Entry(width=33)
passwordEntry.grid(row=3, column=1)

# The Buttons
searchButton = Button(text="Search", width=15, command=findPassword)
searchButton.grid(row=1, column=2)
generatePasswordButton = Button(text="Generate Password", command=generatePassword)
generatePasswordButton.grid(row=3, column=2)
addButton = Button(text="Add", width=44, command=save)
addButton.grid(row=4, column=1, columnspan=2)


window.mainloop()
