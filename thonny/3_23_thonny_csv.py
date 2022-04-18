from tkinter import *
import tkinter as tk
import csv
from csv import writer
import time
import customtkinter
import tkinter.font as font
'''
You don't need to put global on the base indentation level, just initialize the variables here and use global VAR_NAME within the classes/function you need to call them in
'''
global window
global Drinks
global delete
global app



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
    drinkObjList = []
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
            
            button = customtkinter.CTkLabel(window, text="Pour " + formatted[1] + " ounces of " + formatted[0], text_font = myFont, anchor= CENTER)
            button.place(relx=0.5, rely=0.18, anchor=CENTER)
            ingredientList.pop(0)
            
            if (ingredientList == []):
                
                loginBtn1 = customtkinter.CTkButton(window, text="Finish", text_font = myFont, command=lambda: [button.destroy(), App(), loginBtn1.destroy()])
                loginBtn1.grid(row=1, columnspan=2, column=col, pady=170, padx=290, ipadx=50, ipady=40)
            else:
                loginBtn1 = customtkinter.CTkButton(window, text="OK", text_font = myFont, command=lambda: [button.destroy(), Drink.readthis(ingredientList), loginBtn1.destroy()])
                loginBtn1.grid(row=1, columnspan=3, column=col, pady=170, padx=290, ipadx=50, ipady=40)  
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
            loginBtn1 = customtkinter.CTkButton(window, text=drink.name, text_font= myDrinkFont, width = 280, command=lambda drink=drink: [selectDrinks.deleteOptions(), Drink(drink.ingredients)])
            loginBtn1.grid(row=row, columnspan=1, column=col, pady=10, padx=10, ipadx=50, ipady=40)
            delete.append(loginBtn1)
            
            if (col % 2 == 0):
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
            button = customtkinter.CTkLabel(window, text="What is the name of your drink?", text_font= myFont)
            button.grid(row=0, columnspan=1, column=0, pady=(10, 0), padx=150, ipadx=0, ipady=50)
            loginBtn1 = customtkinter.CTkButton(window, text="Next", text_font= myFont, command=lambda: [button.destroy(), self.info.append(returnDrink(entry)), ingredientScreen(),loginBtn1.destroy()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=0, padx=0, ipadx=50, ipady=40)
            
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
            button = customtkinter.CTkLabel(window, text="How many ounces of this \n ingredient should be added?", text_font= myFont)
            button.grid(row=0, columnspan=1, column=0, pady=(1, 0), padx=173, ipadx=0, ipady= 38)
            loginBtn1 = customtkinter.CTkButton(window, text="Next", text_font= myFont, command=lambda: [button.destroy(), returnOunces(entry), entry.grid_remove(), checkScreen(),loginBtn1.destroy()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=0, padx=0, ipadx=50, ipady=40)

        
        def ingredientScreen():
            entry.delete(0,END)
            button = customtkinter.CTkLabel(window, text="What is the name of your ingredient?", text_font= myFont)
            button.grid(row=0, columnspan=1, column=0, pady=(10, 0), padx=113, ipadx=0, ipady=50)
            loginBtn1 = customtkinter.CTkButton(window, text="Next", text_font= myFont, command=lambda: [button.destroy(), returnIngredient(entry), ouncesScreen(),loginBtn1.destroy()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=0, padx=0, ipadx=50, ipady=40)
            
        def checkScreen():
            newIng = "{}/{};".format(self.inges[0],self.inges[1])
            self.s += newIng
            self.inges = []
            
            button = customtkinter.CTkLabel(window, text="Do you want to add another ingredient?", text_font= myFont, anchor= CENTER)
            button.grid(row=0, columnspan=3, column=1, pady= 10, padx= 105, ipadx=0, ipady=80)
            loginBtn1 = customtkinter.CTkButton(window, text="Yes", text_font= myFont, command=lambda: [button.destroy(), ingredientScreen(), entry.grid(), loginBtn1.destroy(),loginBtn.destroy()])
            loginBtn1.grid(row=2, columnspan=2, column=1, pady=10, padx=10, ipadx=50, ipady=40)
            
            loginBtn = customtkinter.CTkButton(window, text="No", text_font= myFont, command=lambda: [button.destroy(), finishedScreen(), loginBtn.destroy(), loginBtn1.destroy(), self.info.append(self.s.rstrip(self.s[-1]))])
            loginBtn.grid(row=2, columnspan=1, column=3, pady=10, padx=10, ipadx=50, ipady=40)
        
        def finishedScreen():
            button = customtkinter.CTkLabel(window, text="Drink Finished", text_font= myFont)
            button.grid(row=0, columnspan=1, column=0, pady=10, padx=130, ipadx=0, ipady=40)
            loginBtn1 = customtkinter.CTkButton(window, text="OK", text_font= myFont, command=lambda: [button.destroy(), loginBtn1.destroy(), App(), createDrink(self.info), readCSV()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=10, padx=10, ipadx=50, ipady=40)
            
        entry = Entry(window, width = 30, justify='center', font= myFont)
        entry.grid(row=1, columnspan=1, column=0, pady=(0, 50), padx=0, ipadx=0, ipady=40)
        
        
        
        main()
            
        
 





############################################################
# MAIN APP - SELECTION SCREEN FOR CREATING OR MAKING A DRINK
############################################################
class App(Frame):
    def __init__(self):
        Frame.__init__(self)
        def mainScreen():
            loginBtn = customtkinter.CTkButton(window, text='Select Drink', text_font= myFont ,command=lambda: [loginBtn.destroy(),loginBtn1.destroy(), selectDrinks()])
            loginBtn.grid(row=1, columnspan=1, pady=160, padx=(70, 40), ipadx=50, ipady=40)
        
            loginBtn1 = customtkinter.CTkButton(window, text='Create Drink', text_font= myFont ,command=lambda: [loginBtn.destroy(),loginBtn1.destroy(), createDrinks()])
            loginBtn1.grid(row=1, columnspan=1, column=2, ipadx=50, ipady=40)
        mainScreen()
        



readCSV()
window = customtkinter.CTk()
window.eval('tk::PlaceWindow . center')

myFont = font.Font(window, family='Showcard Gothic', size = 20)
myDrinkFont = font.Font(window, family='Showcard Gothic', size = 20)

window.geometry("800x480")
app = App()
window.mainloop()
