from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import csv
import time
global window
global Drinks
global delete
window = Tk()

drinkObjList = []

class newDrink:

    def __init__(self,name,ingredients):
        self.name = name
        self.ingredients = ingredients

    def __str__(self):
        
        return("Drink: "+self.name+" Ingredients: "+self.ingredients)


def readCSV():
    global drinkObjList
    with open('data/drink.csv','r') as f:
        for line in f:
            currentLine = ""
            currentLine += line
            drinkList = []

            drinkList.extend(currentLine.split(","))
            print(drinkList)
            name = drinkList[0]
            ingredients = drinkList[1]

            drinkObj = newDrink(name,ingredients)

            drinkObjList.append(drinkObj)
            print(drinkObjList)
            
def createDrink():
    check = True
    j = 1
    s = ""
    usrName = str(input("What is the name of the drink? "))
    
    while check == True:
        usrIng = input("Enter ingredient {} ").format(j)
        usrAmt = input("Enter the amount in ounces for ingredient {} ").format(j)
        
        newIng = "{}/{};".format(usrIng,usrAmt)
        
        s += newIng
        
        usrCheck = input("Add more ingredients? [Y/N]")
        
        usrCheck = usrCheck.upper()
        
        if usrCheck == "Y":
            j += 1
            check = True
            
        else:
            check = False
            
    outfile = open('data/drink.csv','a',newline="")
    info = "{},{}".format(usrName,s)
    
    
    

class Ing():
    def __init__(self, name, amount):
        self.nam = name
        self.amountOz = amount
    def __str__(self):
        return "Pour " + str(self.amountOz) + " ounce(s) of " + self.nam 

class Drink(Frame):
    def __init__(self, drink):
        
        self._drink = drink
        Frame.__init__(self)
        col = 1

        for inge in drink:
            print(inge)
            button = Label(window, text=inge)
            button.grid(row=0, columnspan=1, column=1, pady=10, padx=130, ipadx=0, ipady=40)
            
            if (col == 1):
                loginBtn1 = Button(window, text="OK", command=lambda: [button.destroy()])
                loginBtn1.grid(row=1, columnspan=2, column=col, pady=10, padx=10, ipadx=50, ipady=40)
            col += 1
            #time.sleep(60)
            
            
        
        #loginBtn1 = Button(window, text='hi', command=None)
        #loginBtn1.grid(row=3, columnspan=3, column=2, pady=10, padx=10, ipadx=50, ipady=40)




class selectDrinks(Frame):
    def __init__(self):
        global delete
        Frame.__init__(self)
        col = 1
        test = 0
        delete = []
        for drink in Drinks:
            print(drink)
            print(test)
            loginBtn1 = Button(window, text=drink[1], command=lambda: [selectDrinks.deleteOptions(), Drink(drink[0])])
            loginBtn1.grid(row=2, columnspan=1, column=col, pady=10, padx=10, ipadx=50, ipady=40)
            delete.append(loginBtn1)
            col += 1
            test += 1
            
    def deleteOptions():
        global delete
        for item in delete:
            item.destroy()
            
        #loginBtn2 = Button(window, text='Rum & Coke', command=lambda: [loginBtn2.destroy(), Drink( "####", "Rum & Coke")])
        #loginBtn2.grid(row=3, columnspan=3, column=2, pady=10, padx=10, ipadx=50, ipady=40)
        
        
class App(Frame):
    def __init__(self):
        Frame.__init__(self)
        loginBtn = Button(window, text='Select Drink', command=lambda: [loginBtn.destroy(),loginBtn1.destroy(), selectDrinks()])
        
        
        loginBtn.grid(row=1, columnspan=1, pady=10, padx=10, ipadx=50, ipady=40)
        loginBtn1 = Button(window, text='Create Drink', command=lambda: [loginBtn.destroy(),loginBtn1.destroy()])
        loginBtn1.grid(row=1, columnspan=1, column=2, pady=10, padx=10, ipadx=50, ipady=40)


readCSV()



'''
ing = []

#hi = Ing("Rum", 1)
RC_ing = [Ing("Rum", 1), Ing("Coke", 5)]
VS_ing = [Ing("Vodka", 1), Ing("Sprite", 5)]

ing.append(RC_ing)
ing.append(VS_ing)

Drinks = []
Drinks.append([RC_ing, ["Rum & Coke"]])
Drinks.append([VS_ing, ["Vodka & Sprite"]])
print(ing[1][0])
print(Drinks[0][1])
print(RC_ing[1])
    
'''
window.geometry("400x300")
app = App()
window.mainloop()
