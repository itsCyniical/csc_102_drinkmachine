from tkinter import *
import tkinter as tk
import csv
from csv import writer
import time
from time import sleep
import customtkinter
import tkinter.font as font
import RPi.GPIO as GPIO

#establish global variables
global SHomeButton 
global window
global Drinks
global delete
global app
global drinkDelete

confirm = 0



selectDrinkXButton = 15

leds = [4,27,5,26,6,25,12,24,13,23,16,22,17,21,18,20]

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds,GPIO.OUT)

##################################################
# ARRAY OF ALL OBJECTS MADE FROM THE DRINK CLASS #
##################################################

drinkObjList = []

###############
# Drink Class #
###############

class newDrink:
    #inits drink variables name and ingredients
    def __init__(self,name,ingredients):
        self.name = name
        self.ingredients = ingredients
    #return name
    def name(self):
        return self.name
    #return ingredients
    def ingredients(self):
        return self.ingredients
    #str method
    def __str__(self):
        return("Drink: "+self.name+" Ingredients: "+self.ingredients)

#####################################################################################################################
# READING THE drink.csv FILE FROM WITHIN THE DATA DIRECTORY. ADD ANY PRE INCLUDED DRINKS DIRECTLY INTO THE CSV FILE #
#####################################################################################################################
    
def readCSV():
    global drinkObjList
    drinkObjList = []
    with open('data/drink.csv','r') as f:
        for line in f:
            currentLine = ""
            currentLine += line
            drinkList = []

            drinkList.extend(currentLine.split(","))
            name = drinkList[0]
            ingredients = drinkList[1]

            drinkObj = newDrink(name,ingredients)
            drinkObjList.append(drinkObj)

################################
# METHOD FOR USER ADDED DRINKS #
################################
            
def createDrink(info):
    with open('data/drink.csv','a',newline="") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(info)
        f_object.close()
    

def deleteDrink(drink):
    lines = []
    with open('data/drink.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == drink:
                    lines.remove(row)

    with open('data/drink.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
        writeFile.close()
    


######################################################
# DISPLAYS EACH INGREDIENT FOR SAID DRINK ONE BY ONE #
######################################################

class Drink(Frame):
    def __init__(self, drink):
        self._drink = drink
        Frame.__init__(self)
        
        #creates ingredient array containing every ingredient which is seperated by a ; and formatted as ingredient/numOunces
        ingredientList = []
        ingredientList.extend(drink.split(";"))
        
        #calls the readthis fuction which is a recursive array that deletes the beginning of the array and recalls the function
        #to display the next ingredient on screen, stops when nothing is in the array
        Drink.readthis(ingredientList)
    def readthis(ingredientList):
        global leds
        global SHomeButton
        #places home button
        SHomeButton = customtkinter.CTkButton(window, height = 50, width = 50, text_color = "white", text_font= myDrinkFont, text='Home', command=lambda: [button.destroy(), loginBtn1.destroy(), App(), SHomeButton.place_forget()])
        SHomeButton.place(x=695, y=5)
        
        #GPIO to false before each iteration
        GPIO.output(leds,False)
        col = 1
            
        for ingredient in ingredientList:
            x = ingredient.replace("\n", "")
            formatted = x.split("/")
            
            #######################################
            # Calculating values for GPIO display #
            #######################################
            
            n = float(formatted[1])
            i = 0
            ingDisplay = int(round(n*2))
              
            button = customtkinter.CTkLabel(window, text="Pour " + formatted[1] + " ounces of " + formatted[0], text_color = "white", text_font = myFont, anchor= CENTER)
            button.place(relx=0.5, rely=0.18, anchor=CENTER)
            
            ingredientList.pop(0)
            
            #######################
            # GPIO IMPLEMENTATION #
            #######################
            
            #if nothing is in the array display a button that is labeled finished and when clicked deletes all buttons
            #on the page and returns to home screen
            if (ingredientList == []):
                while (i < ingDisplay):
                    GPIO.output(leds[i], True)
                    i += 1
                    sleep(0.1)
                loginBtn1 = customtkinter.CTkButton(window, text="Finish", text_color = "white", text_font = myFont, command=lambda: [button.destroy(), App(), loginBtn1.destroy(), SHomeButton.place_forget()])
                loginBtn1.grid(row=1, columnspan=2, column=col, pady=170, padx=290, ipadx=50, ipady=40)
            else:
            #OK button that recalls function to move onto the next ingredient
                while (i < ingDisplay):
                    GPIO.output(leds[i], True)
                    i += 1
                    sleep(0.1)
                loginBtn1 = customtkinter.CTkButton(window, text="OK", text_color = "white", text_font = myFont, command=lambda: [SHomeButton.place_forget(), button.destroy(), Drink.readthis(ingredientList), loginBtn1.destroy()])
                loginBtn1.grid(row=1, columnspan=3, column=col, pady=170, padx=290, ipadx=50, ipady=40)   
            break

#scroll postion allows program to see how much the scroll is moving
global scrollposition
scrollposition = 0
class VerticalScrolledFrame(Frame):
    """
            modified but base code from
# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

    """
    def __init__(self, parent, bg,*args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        global main_frame
        global delete
        global canvas
        global sec
        global scrollposition
        delete = []
        
        #heirarchy of custom tkinter objects/widgets(allows for widgets to be gridded in a canvas and scrolled vertically)
        main_frame = Frame(self, bg = "gray10")
        main_frame.pack(fill=BOTH,expand=1)
        delete.append(main_frame)
        
        sec = Frame(main_frame, bg = "gray10")
        sec.pack(fill=BOTH,side=BOTTOM)
        delete.append(sec)
        
        # create a canvas object and a vertical scrollbar for scrolling it
        canvas = Canvas(main_frame, bd=0, highlightthickness=0,bg=bg)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE, pady = (60, 0))
        
        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        delete.append(canvas)
        self.canvasheight = 2000
        
        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas,height=self.canvasheight,bg=bg)
        interior_id = canvas.create_window((0,0),window= interior, anchor="nw")
        delete.append(interior)
    
    
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        self.offset_y = 0
        self.prevy = 0
        self.scrollposition = 1

        def on_press(event):
            self.offset_y = event.y_root
            if self.scrollposition < 1:
                self.scrollposition = 1
            if self.scrollposition > self.canvasheight:
                self.scrollposition = self.canvasheight
            canvas.yview_moveto(self.scrollposition / self.canvasheight)
        
        #################################
        # Pi Touchscreen implementation #
        #################################
        
        def on_touch_scroll(event):
            nowy = event.y_root
            sectionmoved = 40     #speed of scroll
            if nowy > self.prevy:
                event.delta = -sectionmoved
            elif nowy < self.prevy:
                event.delta = sectionmoved
            else:
                event.delta = 0
            self.prevy= nowy

            self.scrollposition += event.delta
            if self.scrollposition < 0:
                self.scrollposition = 0
                
            
            scrollposition = self.scrollposition
            canvas.yview_moveto(self.scrollposition/ self.canvasheight)

        self.bind("<Enter>", lambda _: self.bind_all('<Button-1>', on_press), '+')
        self.bind("<Leave>", lambda _: self.unbind_all('<Button-1>'), '+')
        self.bind("<Enter>", lambda _: self.bind_all('<B1-Motion>', on_touch_scroll), '+')
        self.bind("<Leave>", lambda _: self.unbind_all('<B1-Motion>'), '+')
        
        #deletes all items in the frames
        def deleteOptions():
            global delete
            for item in delete:
                print(item)
                item.destroy()
                
############################################################
# READS DRINK LIST AND DISPLAYS EACH ON A SELECTION SCREEN #
############################################################

class selectDrinks(Frame):
    def __init__(self):
        #set global variables so other functions can access variables used within selectDrinks easily
        global xButtons
        global selectButtons
        global delete
        global selectDrinkXButton
        global frame
        global SHomeButton
        Frame.__init__(self)
        
        #creates a scrollable frame from VerticalScrolledFrame so we can grid buttons into it
        frame = VerticalScrolledFrame(window, "gray10")
        frame.pack(side="top", fill="both", expand=True)
   
        
        #######################
        # GUI BUTTON CREATION #
        #######################
        
        #sets the columns that the buttons will be appended to
        col = 1
        row = 2
        #array to add buttons to, allows for the easy removal of all buttons in the frame
        delete = []
        #dictionary variables
        d = {}
        x = 1
        
        ##creates arrays for the (X buttons) and (drink selector buttons) to be added to
        xButtons = []
        selectButtons = []
        for drink in drinkObjList:
            #the d[] allows the creation of variables with unique names each time, allowing to append each button with a different name
            d["selectButton{0}".format(x)] = customtkinter.CTkButton(frame.interior, text=drink.name, text_color = "white", text_font= myDrinkFont, width = 280)
            d["selectButton{0}".format(x)].grid(row=row, columnspan=1, column=col, pady=10, padx=10, ipadx=50, ipady=40)
            #binds the selectButton to on_releaseDrinks
            d["selectButton{0}".format(x)].bind("<Enter>", lambda _: [self.bind_all('<ButtonRelease>', lambda event, drink=drink: selectDrinks.on_releaseDrinks(event, drink)), '+'])
            d["selectButton{0}".format(x)].bind("<Leave>", lambda _: self.unbind_all('<ButtonRelease>'), '+')
            
            d["xButton{0}".format(x)] = customtkinter.CTkButton(frame.interior, text="X", text_color = "white", text_font= myDrinkFont, width = 40, height = 40,  bg_color="#608BD5", fg_color="red", hover_color = "dark red",command=lambda drink=drink:[deleteDrink(drink.name),readCSV()])
            #binds the xButton to on_releaseDrinks
            d["xButton{0}".format(x)].bind("<Enter>", lambda _: [self.bind_all('<ButtonRelease>', lambda event, drink=drink: selectDrinks.on_releaseX(event, drink)), '+'])
            d["xButton{0}".format(x)].bind("<Leave>", lambda _: self.unbind_all('<ButtonRelease>'), '+')
            
            #appends both buttons to the delete array for easy removal later
            delete.append(d["selectButton{0}".format(x)])
            delete.append(d["xButton{0}".format(x)])
            
            #appends both buttons to their relative arrays
            xButtons.append(drink.name)
            selectButtons.append(drink.ingredients)

            frame.interior.unbind("<ButtonRelease>")
            
            #logic for the positioning of buttons (keeps buttons in 2 columns)
            if (col % 2 == 0):
                d["xButton{0}".format(x)].place(x=743, y=selectDrinkXButton)
                selectDrinkXButton += 130
                row += 1
                col = 1
            else:
                d["xButton{0}".format(x)].place(x=343, y=selectDrinkXButton)
                col +=1
            x += 1
        
        #binds motion in this screen to set (confirm to 0) mentioned later in progam but makes sure scroll is set to 0 in this screen
        window.bind("<Enter>", lambda _: [window.bind('<Motion>', lambda event: selectDrinks.confirmup(event)), '+'])
        #place home button
        SHomeButton = customtkinter.CTkButton(window, height = 50, width = 50, text_color = "white", text_font= myDrinkFont, text='Home', command=lambda: [selectDrinks.deleteOptions(), frame.destroy(), main_frame.destroy(), canvas.destroy(), sec.destroy(), App(), SHomeButton.place_forget()])
        SHomeButton.place(x=695, y=5)
        
    def confirmup(event):
        global confirm
        confirm = 0
        
    def onMotion(event, widget):
        global confirm
        confirm += 1
        #
                
    def on_releaseX(event, drink):
        #bring in variables from other functions
        global xButtons
        global canvas
        global main_frame
        global confirm
        global SHomeButton
        #checks what widget user clicked on
        widget_under_cursor = event.widget.winfo_containing(event.x_root, event.y_root)
        #when B1 is clicked and in motion, records the movement change in onMotion() function
        window.bind("<Enter>", lambda _: [window.bind('<B1-Motion>', lambda event: selectDrinks.onMotion(event, widget_under_cursor)), '+'])
        
        #if the widget that user is on currently is not equal to the widget user was on when clicked, goes to else
        if widget_under_cursor == event.widget:
            #if the scroll moved by more than 10, as recorded in onMotion(), ends function
            if confirm > 10:
                window.unbind_all("<ButtonRelease>")
                window.unbind_all("<Button-1>")
                return
            SHomeButton.place_forget()
            
            #gets the place in storage and sets it to a str
            caller = event.widget
            cleanup = str(caller)
            
            #deletes first 30 characters to get rid of unwanted data
            for i in range(30):
                cleanup = cleanup[1:]
            
            #deletes all characters that arent numbers
            for i in range(len(cleanup)):
                disallowed_characters = "._!abcdefghijklmnopqrstuvwxyz"
                for character in disallowed_characters:
                    cleanup = cleanup.replace(character, "")
            #this is the number in order to how it was created during the init
            fixToLastNum = cleanup
            #since the (X buttons) are the second object created in the loop, divide by 2, this returns the number of the
            #(select button) that was created along with the correlating (X button)
            done = int(fixToLastNum) / 2
            #sets var name to the name of the drink in the position done
            name = xButtons[int(done)-1]
            deleteDrink(name)
            #deletes all objects and frames created in the selectButton() process
            selectDrinks.deleteOptions()
            canvas.delete('all')                
            readCSV()
            frame.destroy()
            main_frame.destroy()
            canvas.destroy()
            sec.destroy()
            window.unbind_all("<ButtonRelease>")
            window.unbind_all("<Button-1>")
            #sends to sendThru (Manages the redisplay of drink buttons after one is deleted)
            selectDrinks.sendThru(selectDrinkXButton)
        else:
            window.unbind_all("<ButtonRelease>")
            window.unbind_all("<Button-1>")
            
    def on_releaseDrinks(event, drink):
        #bring in variables from other functions
        global selectButtons
        global canvas
        global main_frame
        global confirm
        global SHomeButton
        #checks what widget user clicked on
        widget_under_cursor = event.widget.winfo_containing(event.x_root, event.y_root)
        #when B1 is clicked and in motion, records the movement change in onMotion() function
        window.bind("<Enter>", lambda _: [window.bind('<B1-Motion>', lambda event: selectDrinks.onMotion(event, widget_under_cursor)), '+'])
        
        #if the widget that user is on currently is not equal to the widget user was on when clicked, goes to else
        if widget_under_cursor == event.widget:
            #if the scroll moved by more than 10, as recorded in onMotion(), ends function
            if confirm > 10:
                window.unbind_all("<ButtonRelease>")
                window.unbind_all("<Button-1>")
                return
            SHomeButton.place_forget()
            
            #gets the place in storage and sets it to a str
            caller = event.widget
            cleanup = str(caller)
            
            #deletes first 30 characters to get rid of unwanted data
            for i in range(30):
                cleanup = cleanup[1:]
            
            #deletes all characters that arent numbers
            for i in range(len(cleanup)):
                disallowed_characters = "._!abcdefghijklmnopqrstuvwxyz"
                for character in disallowed_characters:
                    cleanup = cleanup.replace(character, "")
            if (cleanup == ""):
                cleanup = str(1)
            else: 
                cleanup = cleanup
            #this is the number in order to how it was created during the init, adds one to account for it being an odd number
            fixToLastNum = int(cleanup) + 1
            #since the (X buttons) are the second object created in the loop, divide by 2, this returns the number of the
            #(select button) that was created along with the correlating (X button)
            done = int(fixToLastNum) / 2
            #sets var ingredients to the ingredients of the drink in the position done
            ingredients = selectButtons[int(done)-1]
            #deletes all objects and frames created in the selectButton() process
            selectDrinks.deleteOptions()
            canvas.delete('all')
            frame.destroy()
            main_frame.destroy()
            canvas.destroy()
            sec.destroy()
            #calls the Drink() method
            Drink(ingredients)
            window.unbind_all("<ButtonRelease>")
            window.unbind_all("<Button-1>")
        else:
            window.unbind_all("<ButtonRelease>")
            window.unbind_all("<Button-1>")
        

        
    #send returnValue to Xbuttonto15
    def sendThru(returnValue):
        answer=returnValue
        selectDrinks.Xbuttonto15(answer)
    
    #sets global selectDrinkXButton to 15, this corrects the y value when calling selectDrinks() again
    def Xbuttonto15(answer):
        global selectDrinkXButton
        selectDrinkXButton = 15
        selectDrinks()
    
    #deletes all items in the frame
    def deleteOptions():
        global delete
        for item in delete:
            #print(item)
            item.destroy()
          
            
#######################
# CREATE DRINK METHOD # 
#######################

class createDrinks(Frame):
    def __init__(self):
        Frame.__init__(self)
        usrIng = ""
        usrAmt = 0
        
        self.s = ""
        self.inges = []
        self.info = []
        
        #creates buttons and labels for this frame, when "Next" button is pressed it sends the input to returnDrink(), and deletes widgets created in the process
        def main(): 
            button = customtkinter.CTkLabel(window, text="What is the name of your drink?", text_color = "white", text_font= myFont)
            button.grid(row=0, columnspan=1, column=0, pady=(10, 0), padx=150, ipadx=0, ipady=50)
            loginBtn1 = customtkinter.CTkButton(window, text="Next", text_color = "white", text_font= myFont, command=lambda: [button.destroy(), self.info.append(returnDrink(entry)), ingredientScreen(),loginBtn1.destroy(), HomeButton.place_forget()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=0, padx=0, ipadx=50, ipady=40)
            HomeButton = customtkinter.CTkButton(window, height = 50, width = 50, text_color = "white", text_font= myDrinkFont, text='Home', command=lambda: [button.destroy(), loginBtn1.destroy(), HomeButton.place_forget(), entry.grid_remove(), App()])
            HomeButton.place(x=695, y=5)
            

        #returns drink name
        def returnDrink(en):
            """Gets and prints the content of the entry"""
            content = entry.get()
            return content
        #returns drink ingredients
        def returnIngredient(en):
            """Gets and prints the content of the entry"""
            content = entry.get()
            self.inges.append(content)
        #returns ounces of ingredients
        def returnOunces(en):
            """Gets and prints the content of the entry"""
            content = entry.get()
            self.inges.append(content)
        
        #creates buttons and labels for this frame, when "Next" button is pressed it sends the input to returnOunces(), and deletes widgets created in the process
        def ouncesScreen():
            entry.delete(0,END)
            button = customtkinter.CTkLabel(window, text="How many ounces of this \n ingredient should be added?", text_color = "white", text_font= myFont)
            button.grid(row=0, columnspan=1, column=0, pady=(1, 0), padx=173, ipadx=0, ipady= 38)
            loginBtn1 = customtkinter.CTkButton(window, text="Next", text_color = "white", text_font= myFont, command=lambda: [button.destroy(), returnOunces(entry), entry.grid_remove(), checkScreen(),loginBtn1.destroy(), HomeButton.place_forget()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=0, padx=0, ipadx=50, ipady=40)
            HomeButton = customtkinter.CTkButton(window, height = 50, width = 50, text_color = "white", text_font= myDrinkFont, text='Home', command=lambda: [button.destroy(), loginBtn1.destroy(), HomeButton.place_forget(), entry.grid_remove(), App()])
            HomeButton.place(x=695, y=5)
            

        #creates buttons and labels for this frame, when "Next" button is pressed it sends the input to returnIngredient(), and deletes widgets created in the process
        def ingredientScreen():
            entry.delete(0,END)
            button = customtkinter.CTkLabel(window, text="What is the name of your ingredient?", text_color = "white", text_font= myFont)
            button.grid(row=0, columnspan=1, column=0, pady=(10, 0), padx=113, ipadx=0, ipady=50)
            loginBtn1 = customtkinter.CTkButton(window, text="Next", text_color = "white", text_font= myFont, command=lambda: [button.destroy(), returnIngredient(entry), ouncesScreen(),loginBtn1.destroy(), HomeButton.place_forget()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=0, padx=0, ipadx=50, ipady=40)
            HomeButton = customtkinter.CTkButton(window, height = 50, width = 50, text_color = "white", text_font= myDrinkFont, text='Home', command=lambda: [button.destroy(), loginBtn1.destroy(), HomeButton.place_forget(), entry.grid_remove(), App()])
            HomeButton.place(x=695, y=5)
        
        #asks user if they want to create new ingredient, if yes send back to ingredientScreen(), if no send to finishedScreen(), both delete all widgets created in the process
        def checkScreen():
            newIng = "{}/{};".format(self.inges[0],self.inges[1])
            self.s += newIng
            self.inges = []
            
            button = customtkinter.CTkLabel(window, text="Do you want to add another ingredient?", text_color = "white", text_font= myFont, anchor= CENTER)
            button.grid(row=0, columnspan=3, column=1, pady= 10, padx= 105, ipadx=0, ipady=80)
            loginBtn1 = customtkinter.CTkButton(window, text="Yes", text_color = "white", text_font= myFont, command=lambda: [button.destroy(), ingredientScreen(), entry.grid(), loginBtn1.destroy(),loginBtn.destroy(), HomeButton.place_forget()])
            loginBtn1.grid(row=2, columnspan=2, column=1, pady=10, padx=10, ipadx=50, ipady=40)
            
            loginBtn = customtkinter.CTkButton(window, text="No",text_color = "white", text_font= myFont, command=lambda: [button.destroy(), finishedScreen(), loginBtn.destroy(), loginBtn1.destroy(), self.info.append(self.s.rstrip(self.s[-1])), HomeButton.place_forget()])
            loginBtn.grid(row=2, columnspan=1, column=3, pady=10, padx=10, ipadx=50, ipady=40)
            HomeButton = customtkinter.CTkButton(window, height = 50, width = 50,text_color = "white", text_font= myDrinkFont, text='Home', command=lambda: [button.destroy(), loginBtn1.destroy(), loginBtn.destroy(), HomeButton.place_forget(), entry.grid_remove(), App()])
            HomeButton.place(x=695, y=5)
        
        #Makes sure users want to add the drink with an "OK" screen, if they press OK, createDrink() is called and the info is added to the CSV file
        def finishedScreen():
            button = customtkinter.CTkLabel(window, text="Drink Finished",text_color = "white", text_font= myFont)
            button.grid(row=0, columnspan=1, column=0, pady=10, padx=280, ipadx=0, ipady=40)
            loginBtn1 = customtkinter.CTkButton(window, text="OK", text_color = "white", text_font= myFont, command=lambda: [button.destroy(), loginBtn1.destroy(), App(), createDrink(self.info), readCSV(), HomeButton.place_forget()])
            loginBtn1.grid(row=2, columnspan=1, column=0, pady=10, padx=10, ipadx=50, ipady=40)
            HomeButton = customtkinter.CTkButton(window, height = 50, width = 50,text_color = "white", text_font= myDrinkFont, text='Home', command=lambda: [button.destroy(), loginBtn1.destroy(), HomeButton.place_forget(), entry.grid_remove(), App()])
            HomeButton.place(x=695, y=5)
        
        #entry is created and used throughout each screen
        entry = Entry(window, width = 30, justify='center', font= myFont)
        entry.grid(row=1, columnspan=1, column=0, pady=(0, 50), padx=0, ipadx=0, ipady=40) 
        main()
            
        
 





##############################################################
# MAIN APP - SELECTION SCREEN FOR CREATING OR MAKING A DRINK #
##############################################################
class App(Frame):
    def __init__(self):
        Frame.__init__(self)
        global selectDrinkXButton
        global frame
        #sets y variable for selectDrink() function
        selectDrinkXButton = 15
        def mainScreen():
            global leds
            #sets GPIO to false if user ever returns to the home screen
            GPIO.output(leds,False)
            #unbinds all event commands in the window
            window.unbind_all("<ButtonRelease>")
            window.unbind_all("<Button-1>")
            window.unbind_all("<B1-Motion>")
            window.unbind_all("<Enter>")
            window.unbind_all("<Leave>")
            #if pressed selectDrink() is called
            loginBtn = customtkinter.CTkButton(window, text='Select Drink', text_color = "white", text_font= myFont ,command=lambda: [loginBtn.destroy(),loginBtn1.destroy(), selectDrinks()])
            loginBtn.grid(row=1, columnspan=1, pady=160, padx=(70, 40), ipadx=50, ipady=40)
            #if pressed createDrinks() is called
            loginBtn1 = customtkinter.CTkButton(window, text='Create Drink', text_color = "white", text_font= myFont ,command=lambda: [loginBtn.destroy(),loginBtn1.destroy(), createDrinks()])
            loginBtn1.grid(row=1, columnspan=1, column=2, ipadx=50, ipady=40)
        mainScreen()
    
readCSV()

#sets attributes of the window
window = customtkinter.CTk()
window.eval('tk::PlaceWindow . center')
window.configure(background = ("gray10", "white"))

#sets fonts
myFont = font.Font(window, family='Showcard Gothic', size = 20)
myDrinkFont = font.Font(window, family='Showcard Gothic', size = 14)

#sets size of window
window.geometry("800x480")
#calls App()
app = App()
window.mainloop()

