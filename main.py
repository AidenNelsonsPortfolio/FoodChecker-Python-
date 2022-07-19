import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
import pytesseract
import mysql.connector
from PIL import Image, ImageTk

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "****************",
    database = "allergendatabase"
)

mycursor = db.cursor()

root = Tk()
root.wm_title("Allergen Checker")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

app_height = 700
app_width = 1000

milk = tk.StringVar()
treeNuts = tk.StringVar()
gluten = tk.StringVar()
peanuts = tk.StringVar()
soy = tk.StringVar()
shellfish = tk.StringVar()
sesame = tk.StringVar()

root.geometry(f'{app_width}x{app_height}+{int(screen_width/2 - app_width/2)}+{int(screen_height/2- app_height/2)}')


treeNutList = ['walnut', 'tree nut', 'almond', 'pecan', 'pistachio',
               'walnuts', 'tree nuts', 'almonds', 'pecans', 'pistachios']

shellfishList = ['crab', 'lobster', 'fish', 'crustacean', 'oyster']


allergensToFind = []
imageLoaded = False

imageLabel = Label()
warningLabel = Label()

def open_file():
    path = askopenfile(mode='r', filetypes=[('Image Files', ['*jpeg', '*png', '*jpg'])])
    global pathName
    pathName = path.name
    if path is not None:
        global imageLoaded
        imageLoaded = True
        Button(root, text="Find Allergens From Label", command=findAllergens).pack(pady=10)
        temp = Image.open(pathName)
        foodLabel = ImageTk.PhotoImage(temp)

        global imageLabel
        imageLabel = Label(text = "Hello", image = foodLabel)
        imageLabel.pack(pady = 10)
        print("Hello")

        global choose
        choose['text'] = 'File Has Been Uploaded'
        choose['bg'] = 'green'
        choose['state'] = 'disabled'
        pass


def loggedIn():
    global warningLabel
    warningLabel.destroy()

    Label(root, text="Allergen to Scan For", font='Times 35').pack(pady=10)
    ttk.Checkbutton(root, text = "Tree Nuts", variable = treeNuts, onvalue = 'find', offvalue = 'not').pack(padx = 5)
    ttk.Checkbutton(root, text = "Gluten", variable = gluten, onvalue = 'find', offvalue = 'not').pack(padx = 5)
    ttk.Checkbutton(root, text = "Peanuts", variable = peanuts, onvalue = 'find', offvalue = 'not').pack(padx = 5)
    ttk.Checkbutton(root, text = "Soy", variable = soy, onvalue = 'find', offvalue = 'not').pack(padx = 5)
    ttk.Checkbutton(root, text = "Milk", variable=milk, onvalue = 'find', offvalue = 'not').pack(padx = 5)
    ttk.Checkbutton(root, text = "Shellfish", variable = shellfish, onvalue = 'find', offvalue = 'not').pack(padx = 5)
    ttk.Checkbutton(root, text = 'Sesame', variable = sesame, onvalue = 'find', offvalue = 'not').pack(padx = 5)
    choose = tk.Button(root, text = 'Choose Ingredients Label File', font = 'Times 20', command = lambda:(open_file()))
    choose.pack(pady = 10)

def findAllergens():
    if imageLoaded:
        print("Value Extraction Started")

        global imageLabel
        imageLabel.destroy()

        allergensToFind.clear()
        if treeNuts.get() == 'find':
            for nut in treeNutList:
                allergensToFind.append(nut)
        if gluten.get() == 'find':
            allergensToFind.append('wheat')
        if peanuts.get() == 'find':
            allergensToFind.append('peanut')
            allergensToFind.append('peanuts')
        if soy.get() == 'find':
            allergensToFind.append('soy')
        if milk.get() == 'find':
            allergensToFind.append('milk')
            allergensToFind.append('dairy')
        if shellfish.get() == 'find':
            for fish in shellfishList:
                allergensToFind.append(fish)
        if sesame.get() == 'find':
            allergensToFind.append('sesame')
        global pathName
        print(pathName)
        print(allergensToFind)
        img = Image.open(pathName)
        text = pytesseract.image_to_string(img)

        text = text.lower()
        allergensPresent = []
        temp = ""

        for letter in text:
            if letter == "," or letter == " " or letter == ".":
                if temp in allergensToFind or temp[:-1] in allergensToFind:
                    if temp not in allergensPresent:
                        allergensPresent.append(temp)
                        allergenInFood(temp)
                        print("Contains Allergen Selected : WARNING")
                temp = ""
            else:
                temp = temp + letter
        print("done")

    else:
        Label(root, text = "Must Choose A File Before Finding Its Allergy Contents").pack(pady = 10)


def allergenInFood(s):
    Label(text = f"ALLERGEN SELECTED IS PRESENT IN FOOD \n DO NOT CONSUME \n Allergen Present is {s.upper()}",
          font = 'Times 30', bg = 'red').pack(pady = 10)

def makeNewAcct():
    global newAcct, warningLabel, signIn
    signIn.destroy()
    warningLabel.destroy()
    newAcct.destroy()
    confirmpw = Label(root, text = "Confirm Password Below", font = 'Times 15')
    confirmpw.pack(pady = 10)
    reenterpw = ttk.Entry(root, font = 'Times 15')
    reenterpw.pack(pady = 10)
    enterAllergens = Label(root, text = "Enter All Allergens Below", font = 'Times 15')
    enterAllergens.pack(pady = 10)
    allergens = ttk.Entry(root)
    allergens.pack(pady = 10)
    confButton = ttk.Button(root, text = "Make New Account", command = lambda:(genUserDetails(confirmpw, reenterpw, enterAllergens, allergens, confButton)))
    confButton.pack(pady = 10)

def genUserDetails(l1, e1, l2, e2, b1):
    global username, password
    print(username.get())
    if e1.get() == password.get() and len(e1.get()) > 6:
        print("Good PW")
        mycursor.execute(f"SELECT * FROM User WHERE name = '{username.get()}'")
        if mycursor.rowcount < 1:
            mycursor.fetchall()
            l1.destroy()
            e1.destroy()
            l2.destroy()
            e2.destroy()
            b1.destroy()
            enteruser.destroy()
            enterpw.destroy()
            newAcct.destroy()
            signIn.destroy()
            print("Unique username AND good PW")
            mycursor.execute("INSERT INTO User(name, password, allergens) VALUES (%s,%s,%s)", (username.get(), password.get(), "" ))
            mycursor.fetchall()
            mycursor.execute("SELECT * FROM User")
            password.destroy()
            username.destroy()
            print("complete")
            for row in mycursor:
                print(row)
            mycursor.fetchall()
            loggedIn()
        else:
            warningLabel = Label(root, text = "Username already in use!")
    else:
        warningLabel = Label(root, text = "Must have matching passwords with over 6 characters!", font = 'Times 25', bg = 'red')
        warningLabel.pack(pady = 10)


def tryLogin():
    mycursor.execute(f"SELECT * FROM User WHERE name = '{username.get()}' AND password = '{password.get()}'")
    global warningLabel
    for row in mycursor:
        print(row)
    mycursor.fetchall()
    if mycursor.rowcount < 1:
        print("Bad Login")
        mycursor.execute("SELECT * FROM User")
        mycursor.fetchall()
        for row in mycursor:
            print(row)
        warningLabel.destroy()
        warningLabel = Label(root, text = "Wrong Password Or Username", font = 'Times 30', bg = 'red')
        warningLabel.pack(pady = 10)
    else:
        print("good login")
        mycursor.execute("SELECT * FROM User")
        for row in mycursor:
            print(row)
        mycursor.fecthall()
        enteruser.destroy()
        username.destroy()
        enterpw.destroy()
        password.destroy()
        newAcct.destroy()
        signIn.destroy()
        print("Real User")
        loggedIn()


enteruser = Label(root, text = "Enter Username: ", font = 'Times 15')
enteruser.pack(pady = 10)

username = ttk.Entry(root, font = 'Times 15')
username.pack(pady = 10)

enterpw = Label(root, text = "Enter Password: ", font = 'Times 15')
enterpw.pack(pady = 10)

password = ttk.Entry(root, font = 'Times 15')
password.pack(pady = 10)

signIn = tk.Button(root, text = "Log In", font = 'Times 25', command = lambda:(tryLogin()))
signIn.pack(pady = 10)

newAcct = tk.Button(root, text = "Create New Account", command = lambda:(makeNewAcct()))
newAcct.pack(pady = 10)


root.mainloop()
