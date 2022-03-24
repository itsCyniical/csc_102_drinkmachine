from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import csv
import time
from waiting import wait

'''
You don't need to put global on the base indentation level, just initialize the variables here and use global VAR_NAME within the classes/function you need to call them in
'''
global window
global Drinks
global delete


window = Tk()


###############################################
#LIST OF ALL OBJECTS MADE FROM THE DRINK CLASS#
###############################################
drinkObjList = []

class newDrink:

    def __init__(self,name,ingredients):
        self.name = name
        self.ingredients = ingredients
    
    def name(self):
        return self.name
    
    def ingredients(self):
        return self.ingredients
    
    def __str__(self):
        
        return("Drink: "+self.name+" Ingredients: "+self.ingredients)

###################################################################################################################
#READING THE drink.csv FILE FROM WITHIN THE DATA DIRECTORY. ADD ANY PRE INCLUDED DRINKS DIRECTLY INTO THE CSV FILE#
###################################################################################################################
    
def readCSV():
    global drinkObjList
    with open('data/drink.csv','r') as f:
        for line in f:
            currentLine = ""
            currentLine += line
            drinkList = []

            drinkList.extend(currentLine.split(","))
     #       #print(drinkList)
            name = drinkList[0]
            ingredients = drinkList[1]

            drinkObj = newDrink(name,ingredients)

            drinkObjList.append(drinkObj)
     #       #print(drinkObjList)


##############################
#METHOD FOR USER ADDED DRINKS#
##############################
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
    
    
    
'''
Need to rewrite for csv implementation method
'''


####################################################
# DISPLAYS EACH INGREDIENT FOR SAID DRINK ONE BY ONE
####################################################
class Drink(Frame):
    def __init__(self, drink):
        self._drink = drink
        Frame.__init__(self)
        
        ingredientList = []
        ingredientList.extend(drink.split(";"))
        
        Drink.readthis(ingredientList)
        
    def readthis(ingredientList):
        col = 1
        for ingredient in ingredientList:
            x = ingredient.replace("\n", "")
            formatted = x.split("/")
            
            button = Label(window, text="Pour " + formatted[1] + " ounces of " + formatted[0])
            button.grid(row=0, columnspan=1, column=1, pady=10, padx=130, ipadx=0, ipady=40)
            ingredientList.pop(0)
            
            if (ingredientList == []):
                loginBtn1 = Button(window, text="Finish", command=lambda: [button.destroy(), Label(window, text="Drink Finished").grid(row=0, columnspan=1, column=1, pady=10, padx=130, ipadx=0, ipady=40)])
                loginBtn1.grid(row=1, columnspan=2, column=col, pady=10, padx=70, ipadx=50, ipady=40)
            else:
                loginBtn1 = Button(window, text="OK", command=lambda: [button.destroy(), Drink.readthis(ingredientList)])
                loginBtn1.grid(row=1, columnspan=2, column=col, pady=10, padx=10, ipadx=50, ipady=40)  
            break
    

##########################################################
# READS DRINK LIST AND DISPLAYS EACH ON A SELECTION SCREEN
##########################################################
class selectDrinks(Frame):
    def __init__(self):
        global delete
        Frame.__init__(self)
        col = 1
        row = 2
        delete = []
        for drink in drinkObjList:
            loginBtn1 = Button(window, text=drink.name, command=lambda drink=drink: [selectDrinks.deleteOptions(), Drink(drink.ingredients)])
            loginBtn1.grid(row=row, columnspan=1, column=col, pady=10, padx=10, ipadx=50, ipady=40)
            delete.append(loginBtn1)
            
            if (col % 2 == 0):
                print(col)
                row += 1
                col = 1
            else:
                col +=1
            
    def deleteOptions():
        global delete
        for item in delete:
            item.destroy()

############################################################
# MAIN APP - SELECTION SCREEN FOR CREATING OR MAKING A DRINK
############################################################
class App(Frame):
    def __init__(self):
        Frame.__init__(self)
        loginBtn = Button(window, text='Select Drink', command=lambda: [loginBtn.destroy(),loginBtn1.destroy(), selectDrinks()])
        
        
        loginBtn.grid(row=1, columnspan=1, pady=10, padx=10, ipadx=50, ipady=40)
        loginBtn1 = Button(window, text='Create Drink', command=lambda: [loginBtn.destroy(),loginBtn1.destroy()])
        loginBtn1.grid(row=1, columnspan=1, column=2, pady=10, padx=10, ipadx=50, ipady=40)


readCSV()

window.geometry("400x300")
app = App()
window.mainloop()
