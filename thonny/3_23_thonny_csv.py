from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import csv
from csv import writer
import time
from waiting import wait

'''
You don't need to put global on the base indentation level, just initialize the variables here and use global VAR_NAME within the classes/function you need to call them in
'''
global window
global Drinks
global delete
global app

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
def createDrink(info):
    with open('data/drink.csv','a',newline="") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(info)
        f_object.close()
    
    
    
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
                
                loginBtn1 = Button(window, text="Finish", command=lambda: [button.destroy(), App(), loginBtn1.destroy()])
                loginBtn1.grid(row=1, columnspan=2, column=col, pady=10, padx=70, ipadx=50, ipady=40)
            else:
                loginBtn1 = Button(window, text="OK", command=lambda: [button.destroy(), Drink.readthis(ingredientList), loginBtn1.destroy()])
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
# CREATE DRINK 
############################################################
class createDrinks(Frame):
    def __init__(self):
        Frame.__init__(self)
        usrIng = ""
        usrAmt = 0
        
        self.s = ""
        self.inges = []
        self.info = []
        def main():
            button = Label(window, text="What is the name of your drink?")
            button.grid(row=0, columnspan=1, column=0, pady=10, padx=130, ipadx=0, ipady=40)
            loginBtn1 = Button(window, text="", command=lambda: [button.destroy(), self.info.append(returnDrink(entry)), ingredientScreen(),loginBtn1.destroy()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=10, padx=10, ipadx=50, ipady=40)
            
        def returnDrink(en):
            """Gets and prints the content of the entry"""
            content = entry.get()
            return content
            
        def returnIngredient(en):
            """Gets and prints the content of the entry"""
            content = entry.get()
            self.inges.append(content)
        
        def returnOunces(en):
            """Gets and prints the content of the entry"""
            content = entry.get()
            self.inges.append(content)
        
        def ouncesScreen():
            entry.delete(0,END)
            button = Label(window, text="How many ounces of this ingredient should be added?")
            button.grid(row=0, columnspan=1, column=0, pady=10, padx=130, ipadx=0, ipady=40)
            loginBtn1 = Button(window, text="", command=lambda: [button.destroy(), returnOunces(entry), entry.grid_remove(), checkScreen(),loginBtn1.destroy()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=10, padx=10, ipadx=50, ipady=40)

        
        def ingredientScreen():
            entry.delete(0,END)
            button = Label(window, text="What is the name of your ingredient?")
            button.grid(row=0, columnspan=1, column=0, pady=10, padx=130, ipadx=0, ipady=40)
            loginBtn1 = Button(window, text="", command=lambda: [button.destroy(), returnIngredient(entry), ouncesScreen(),loginBtn1.destroy()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=10, padx=10, ipadx=50, ipady=40)
            
        def checkScreen():
            newIng = "{}/{};".format(self.inges[0],self.inges[1])
            self.s += newIng
            self.inges = []
            
            button = Label(window, text="Do you want to add another ingredient?")
            button.grid(row=0, columnspan=1, column=0, pady=10, padx=130, ipadx=0, ipady=40)
            loginBtn1 = Button(window, text="Yes", command=lambda: [button.destroy(), ingredientScreen(), entry.grid(), loginBtn1.destroy(),loginBtn.destroy()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=10, padx=10, ipadx=50, ipady=40)
            
            loginBtn = Button(window, text="No", command=lambda: [button.destroy(), finishedScreen(), loginBtn.destroy(), loginBtn1.destroy(), self.info.append(self.s.rstrip(self.s[-1]))])
            loginBtn.grid(row=2, columnspan=1, column=1, pady=10, padx=10, ipadx=50, ipady=40)
        
        def finishedScreen():
            button = Label(window, text="Drink Finished")
            button.grid(row=0, columnspan=1, column=0, pady=10, padx=130, ipadx=0, ipady=40)
            loginBtn1 = Button(window, text="OK", command=lambda: [button.destroy(), loginBtn1.destroy(), App(), createDrink(self.info)])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=10, padx=10, ipadx=50, ipady=40)
            
        entry = Entry(window, width=50,justify='center')
        entry.grid(row=1, columnspan=1, column=0, pady=10, padx=130, ipadx=0, ipady=40)
        
        
        
        main()
            
        
 





############################################################
# MAIN APP - SELECTION SCREEN FOR CREATING OR MAKING A DRINK
############################################################
class App(Frame):
    def __init__(self):
        Frame.__init__(self)
        
        def mainScreen():
            loginBtn = Button(window, text='Select Drink', command=lambda: [loginBtn.destroy(),loginBtn1.destroy(), selectDrinks()])
            loginBtn.grid(row=1, columnspan=1, pady=10, padx=10, ipadx=50, ipady=40)
        
            loginBtn1 = Button(window, text='Create Drink', command=lambda: [loginBtn.destroy(),loginBtn1.destroy(), createDrinks()])
            loginBtn1.grid(row=1, columnspan=1, column=2, pady=10, padx=10, ipadx=50, ipady=40)
        mainScreen()
        



readCSV()

window.geometry("800x480")
app = App()
window.mainloop()
