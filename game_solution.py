'''Papa's Pizza Making Game'''
'''Author: Amelie Coy, 2023'''

#import required modules 
from tkinter import Tk, Label, Button, Entry, Canvas, Frame, Toplevel, ttk, Radiobutton, IntVar, END
from PIL import Image, ImageTk
import random
import time
import math

#dictionary of ingredients required for each level 
ingredientsPerLevel = {1: ['pepperoni'],
                         2: ['pepperoni', 'onions'],
                         3: ['onions', 'bacon', 'pepperoni'],
                         4: ['pepperoni', 'bacon', 'peppers_olives', 'onions'],
                         5: ['bacon', 'pepperoni', 'onions','tomatoes', 'peppers_olives'],
                         6: ['onions', 'mushrooms', 'bacon', 'peppers_olives', 'pepperoni', 'tomatoes']}

def create_window():
    '''Initialises and configures main window'''
    global window
    window = Tk()
    window.title("Game Window")
    window.configure(bg = yellowColour)
    #set window to full screen size
    global screenWidth
    global screenHeight
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    window.geometry(str(screenWidth) + 'x' + str(screenHeight))

def login():
    '''Configures main window with login widgets'''
    #create title widget for window
    global title
    title = Label(window, fg = redColour, bg = yellowColour, text="Login", font=("Calibri", 45))
    title.place(relx =.5, rely = .1, anchor = 'c')
    #create player name entry widgets 
    global userEntry
    userLabel = Label(window, fg = redColour, bg = yellowColour, text = "Please enter player name below:", font = "Calibri")
    userLabel.place(relx =.5, rely = .25, anchor = 'c')
    userEntry = Entry(window, width = 60)
    userEntry.place(relx =.5, rely = .3, anchor = 'c')
    window.bind("<Return>", menu)

def menu(event):
    '''Configures main window with main menu widgets'''
    get_user()
    #configure main menu widgets 
    for widget in window.winfo_children():
        if widget != title:
            widget.destroy()
    title.configure(text = "Papa's Pizza Making Game")
    playButton = Button(window, width = 20, height = 2, text = "Play", command = play, fg = redColour)
    playButton.place(relx =.5, rely = .3, anchor = 'c')
    settingsButton = Button(window, width = 20, height = 2, text = "Settings", fg = redColour, command = settings)
    settingsButton.place(relx =.5, rely = .4, anchor = 'c')
    leaderboardButton = Button(window, width = 20, height = 2, text = "Leaderboard", fg = redColour, command = show_leaderboard)
    leaderboardButton.place(relx =.5, rely = .5, anchor = 'c')
    #stop return button from triggering player name entry
    window.unbind("<Return>")


def get_user():
    '''Once user has logged in, checks if user is already stored and configures customised direction keys accordingly'''
    #get and store entered player name from widget
    try:
        global userPlaying
        userPlaying = userEntry.get()
    except:
        pass
    #remove menu widgets from page
    global level
    for widget in window.winfo_children():
        if widget != title:
            widget.destroy()
    #open score file to find player name 
    flag = 'notInFile'
    try:
        levelsFile = open("Levels File", 'r')
        lines = levelsFile.readlines()
        directionsForUserLine = 0
        for i in range (len(lines)):
            line = lines[i]
            if line != '\n':
                if line.split(': ')[0] == userPlaying:
                    #player already stored - get current level 
                    level = line.split(': ')[1]
                    level = int(level.strip()[1])
                    flag = 'inFile'
                    #identify direction settings for current player are on next line of file 
                    directionsForUserLine = i+1
                elif i == directionsForUserLine:
                    #get current direction key settings for current player
                    check_current_direction(line)                         
    except:
        pass
    
    if flag == 'notInFile':
        #player not already stored 
        levelsFile = open("Levels File", 'a')
        #add player to file with starting level 1, previous time 0
        levelsFile.write(userPlaying + ": (1, 0)\n")
        #write default direction key settings to file underneath player name
        levelsFile.write(" **↑,↓,←,→\n")
        #set current direction key settings to match defaults
        global currentU
        global currentD
        global currentL
        global currentR
        currentU = 'Up'
        currentD = 'Down'
        currentL = 'Left'
        currentR = 'Right'
        levelsFile.close()

def play():
    #begin gameplay at correct level for player     
    start_level(int(level))

def start_level(level):
    '''Configures main window with game level widgets'''
    #remove menu widgets from window 
    for widget in window.winfo_children():
        if widget != title:
            widget.destroy()
    #display current level number 
    title.configure(text = "Level " + str(level))
    #create game canvas in bottom half of screen
    global gameCanvas
    gameCanvas = Canvas(window, width = screenWidth, height = screenHeight/2, bg = yellowColour, highlightthickness=0)
    gameCanvas.place(relx=0.5, rely=1, anchor='s')
    #record start time of gameplay
    global pauseTime
    global startTime
    pauseTime = 0
    startTime = time.time()
    #get ingredients required to complete current level from dictionary, write to list 
    orderIngredients = ''
    for ingredient in ingredientsPerLevel[level]:
        if ingredient == 'peppers_olives':
            ingredient = 'Peppers and Olives\n'
        else:
            ingredient = ingredient[0].upper() + ingredient[1:] + '\n'
        orderIngredients += ingredient

    #place receipt image and ingredient list for level in window
    receiptLabel = Label(window, image = orderReceipt) # height = 150, width = 200)
    receiptLabel.place(relx =.5, rely = .3, anchor = 'c')

    orderIngredientsLabel = Label(window, text = orderIngredients, bg = '#F0F0F0' ) 
    orderIngredientsLabel.place(relx =.455, rely = .22, anchor = 'nw')

    #place pizza image on canvas
    gameCanvas.create_image(1000, 50, anchor= 'nw', image=pizzaBase, tag = "pizza")

    #place ingredient images on canvas - loop through list  
    i = 0
    global ingredientImages
    ingredientImages = []
    for ing in ingredientDict:
        #only show images without the red selection border
        if 'Red' not in ing:
            pic = ingredientDict[ing]
            #calculate position of image on canvas 
            if i < 3:
                y = 120
            else:
                y = 320
            gap = 200
            x = 100 + ((i % 3)*gap)
            #place image and bind to selection function when clicked
            ingredientImages.append(gameCanvas.create_image(x, y, image=pic, activeimage = ingredientDict[ing+'Red']))
            gameCanvas.tag_bind(ingredientImages[i], "<ButtonRelease-1>", select_ingredient)
            i += 1
    #create lines to indicate centre of pizza
    gameCanvas.create_line(1130, 225, 1210, 225)
    gameCanvas.create_line(1170, 185, 1170, 265)

    #configure lists to hold ingredients successfully placed on pizza for this level 
    global placedIngs
    placedIngs = []
    global placedImages
    placedImages = []

    #create and show pause button on window
    pauseButtonButton = Button(window, image = pauseButton, command = pause) 
    pauseButtonButton.place(relx =.94, rely = .1, anchor = 'c')

    #create and show pizza cutter shape 
    gameCanvas.create_oval(800, 0, 850, 50, tag = 'cutter')
    start_cutter_movement()

def start_cutter_movement():
    '''Executes loop for continuous movement of pizza cutter and collision detection'''
    while True:
        if gameCanvas.coords('cutter')[1] > 400:
            #reached right edge of canvas 
            x = -5
        elif gameCanvas.coords('cutter')[1] < 50:
            #reached left edge of canvas 
            x = 5
        time.sleep(0.05)
        gameCanvas.move('cutter', 0, x)
        window.update()
        #check if moving ingredient has collided with pizza cutter - causing automatic fail 
        try:
            if gameCanvas.coords("newImage")[0]+75 < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0]+75 > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1]+75 < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1]+75 > gameCanvas.coords("cutter")[1]:
                autoFail()
            elif gameCanvas.coords("newImage")[0]-75 < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0]-75 > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1]-75 < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1]-75 > gameCanvas.coords("cutter")[1]:
                autoFail()
            elif gameCanvas.coords("newImage")[0] < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0] > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1] < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1] > gameCanvas.coords("cutter")[1]:
                autoFail()
            elif gameCanvas.coords("newImage")[0] < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0] > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1]+75 < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1]+75 > gameCanvas.coords("cutter")[1]:
                autoFail()
            elif gameCanvas.coords("newImage")[0]+75 < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0]+75 > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1] < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1] > gameCanvas.coords("cutter")[1]:
                autoFail()
            elif gameCanvas.coords("newImage")[0]-75 < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0]-75 > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1] < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1] > gameCanvas.coords("cutter")[1]:
                autoFail()
            elif gameCanvas.coords("newImage")[0] < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0] > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1]-75 < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1]-75 > gameCanvas.coords("cutter")[1]:
                autoFail()
            elif gameCanvas.coords("newImage")[0]+75 < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0]+75 > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1]-75 < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1]-75 > gameCanvas.coords("cutter")[1]:
                autoFail()
            elif gameCanvas.coords("newImage")[0]-75 < gameCanvas.coords("cutter")[2] and gameCanvas.coords("newImage")[0]-75 > gameCanvas.coords("cutter")[0] and gameCanvas.coords("newImage")[1]+75 < gameCanvas.coords("cutter")[3] and gameCanvas.coords("newImage")[1]+75 > gameCanvas.coords("cutter")[1]:
                autoFail()
        except:
            pass

def select_ingredient(event):
    '''Identifies which ingredient image was clicked and adds red border'''
    global itemNum
    global itemRef
    global curRef
    #find which ingredient image was clicked
    itemNum = gameCanvas.find_closest(event.x, event.y)[0]
    #find corresponding ingredient index in dictionary and show red border selected image
    itemRef = itemNum - 2
    gameCanvas.itemconfigure(itemNum,image = ingredientDict[ingredientList[itemRef]+'Red'])
    curRef = None
    #configure any previously selected image back to default ingredient image 
    for imageNum in ingredientImages:
        imageRef = imageNum-2
        if imageRef != itemRef:
            gameCanvas.itemconfigure(imageNum, image = ingredientDict[ingredientList[imageRef]])
    #bind key presses to movement of selected image
    window.bind("<Key>", movement_handler)

def movement_handler(event):
    '''Creates a duplicate of selected ingredient, and moves it on keypresses'''
    global curRef
    global itemRef
    #check if an ingredient has already been selected and moved
    if gameCanvas.find_withtag("newImage") == ():
        #no ingredient in process of moving - calculate position of new image
        if itemRef < 3:
            y = 120
        else:
            y = 320
        gap = 200
        x = 100 + ((itemRef % 3)*gap)
        #create duplicate of ingredient image to be moved 
        curRef = gameCanvas.create_image(x, y, image= ingredientDict[ingredientList[itemRef]], tags = ("newImage", itemRef))
    if gameCanvas.find_withtag("newImage") != () and gameCanvas.find_withtag("newImage")[0] != curRef :
        #there is a different ingredient with a duplicate image so delete this old one
        gameCanvas.delete("newImage")
        #calculate position of new image
        if itemRef < 3:
            y = 120
        else:
            y = 320
        gap = 200
        x = 100 + ((itemRef % 3)*gap)
        #create duplicate of new ingredient image to be moved 
        curRef = gameCanvas.create_image(x, y, image= ingredientDict[ingredientList[itemRef]], tags = ("newImage", itemRef))

    #check if key pressed matches one of players' direction keys 
    if event.keysym == currentL:
        #move left if not at edge
        if (gameCanvas.coords("newImage"))[0] != 60:
            gameCanvas.move("newImage", -20, 0)
    if event.keysym == currentR:
        #move right if not at edge
        if (gameCanvas.coords("newImage"))[0] != 1380:
            gameCanvas.move("newImage", 20, 0)
    if event.keysym == currentD:
        #move down if not at edge
        if (gameCanvas.coords("newImage"))[1] != 380:
            gameCanvas.move("newImage", 0, 20)
    if event.keysym == currentU:
        #move up if not at edge
        if (gameCanvas.coords("newImage"))[1] != 80:
            gameCanvas.move("newImage", 0, -20)
    check_for_pass_fail()
        
def check_for_pass_fail():
    '''Checks if ingredient should be added to pizza, and whether all correct ingredients for game level are now on pizza'''
    if gameCanvas.coords("newImage") == [1180.0, 220.0]:
        #ingredient has reached centre of pizza - identify which ingredient it is and add to lists
        itemRef = int(gameCanvas.gettags("newImage")[1])
        placedIngs.append(ingredientList[itemRef])
        placedImages.append(Image.open(ingredientList[itemRef] + '.png'))
        #resize ingredient image to fit on pizza and display 
        placedImages[len(placedImages)-1] = placedImages[len(placedImages)-1].resize((300,300))
        placedImages[len(placedImages)-1] = ImageTk.PhotoImage(placedImages[len(placedImages)-1])
        gameCanvas.create_image(1180, 220, image= placedImages[len(placedImages)-1], tags = ("placed", itemRef))
        #delete duplicate image used for movement 
        gameCanvas.delete("newImage")
        #get ingredients required to complete level
        newList = ingredientsPerLevel[level].copy()
        #initialise empty list for comparison
        removed = []
        for ing in placedIngs:
            global failedFlag
            #check if ingredient on pizza is required for the level
            if ing in ingredientsPerLevel[level]:
                try:
                    #remove ingredient from the required list of ingredients, and record that it's been removed
                    newList.remove(ing)
                    removed.append(ing)
                except:
                    pass
                if len(newList) == 0:
                    #passed level as no more ingredients required for level
                    #disable movement of ingredient
                    window.unbind("<Key>")
                    #record time of level completion
                    endTime = time.time()
                    #destroy all gameplay widgets on window
                    for widget in window.winfo_children():
                        if widget != title:
                            widget.destroy()
                    #set title widget to show completion message
                    title.configure(text = 'Congratulations! Level Complete')
                    window.update()
                    time.sleep(2)
                    #calculate time taken and update score file
                    timeScore = endTime - startTime - pauseTime
                    global codeEntered
                    if codeEntered == correctCode:
                        #cheat code takes 10% off your time 
                        timeScore -= (timeScore / 10)
                    update_score(timeScore)

            
            elif ing not in removed:
                #ingredient on pizza should not be on pizza - auto fail
                failedFlag = True
                window.unbind("<Key>") 
                autoFail()

def autoFail():
    '''Ends game level attempt and displays failed message to user, then restarts level'''
    #destroy all gameplay widgets on window
    for widget in window.winfo_children():
        if widget != title:
            widget.destroy()
    #set title widget to show failure message
    title.configure(text = 'Level Failed')
    window.update()
    time.sleep(2)
    #restart level
    start_level(level)

    
def update_score(timeScore):
    '''Writes user's next level and time taken for completed level to score file, begins next level'''
    global level
    #open scores file to get current contents 
    levelsFile = open("Levels File", 'r')
    lines = levelsFile.readlines()
    newLevels = []
    for line in lines:
        #update the score on the line of the current player only
        if line != '\n' and line[0:3] != ' **':
            if line.split(': ')[0] == userPlaying:
                #format the time to 2 digits and 3 decimal places 
                timeScore = round(timeScore, 3)
                if len(str(math.trunc(timeScore))) == 1:
                    timeScore = '0'+str(timeScore)
                #write next level and time taken for current level to file 
                newLine = userPlaying + ": (" + str(level+1) + ", " + str(timeScore) + ")\n"
                newLevels.append(newLine)
            else:
                #keep original line in file if not being updated
                newLevels.append(line)
        elif line[0:3] == ' **':
            newLevels.append(line)
    #write updated file contents back to file 
    levelsFile = open("Levels File", 'w')
    for line in newLevels:
        levelsFile.write(line)
    levelsFile.close()
    #start next level gameplay automatically 
    level += 1
    start_level(level)

def pause():
    '''Initialise and configure new window for pause menu'''
    #create new window for pause menu
    global pausedWindow
    global quitButton
    pausedWindow = Toplevel()
    pausedWindow.grab_set()

    #create and configure pause menu widgets 
    global cheatCodeEntry
    resumeButton = Button(pausedWindow, width = 20, height = 2, text = "Resume", fg = redColour, command = resume) 
    resumeButton.place(relx =.5, rely = .3, anchor = 'c')
    quitButton = Button(pausedWindow, width = 20, height = 2, text = "Quit Level", fg = redColour, command = quit_level)
    quitButton.place(relx =.5, rely = .4, anchor = 'c')
    cheatCodeLabel = Label(pausedWindow, text = "Enter cheat code:", bg = yellowColour, fg = redColour)
    cheatCodeLabel.place(relx =.5, rely = .5, anchor = 'c')
    cheatCodeEntry = Entry(pausedWindow, width = 20)
    cheatCodeEntry.place(relx =.5, rely = .55, anchor = 'c')

    #record time spent in pause mode to subtract from gameplay time
    global pauseTimeStart
    pauseTimeStart = time.time()

    #configure pause window and bind to enter cheat code
    pausedWindow.bind("<Return>", check_cheat_code) 
    pausedWindow.geometry("600x500+360+140")
    pausedWindow.title("Pause Menu")
    pausedWindow.configure(background = yellowColour)
    pausedWindow.wait_window()

def resume():
    '''Destroy pause window and discount pause time from gameplay time to continue level'''
    global pausedWindow
    global pauseTime
    #calculate time spent in pause mode
    pauseTimeEnd = time.time()
    pauseTime += pauseTimeEnd - pauseTimeStart
    #destroy pause menu window
    pausedWindow.grab_release()
    pausedWindow.destroy()
    
def quit_level():
    '''Returns to main menu when level is quit'''
    menu(0)

def check_cheat_code(event):
    '''Compare entered cheat code to valid one, display correct message'''
    global codeEntered
    #retrieve player's cheat code entry from widget
    codeEntered = cheatCodeEntry.get()
    cheatCodeEntry.delete(0, END)
    global cheatCodeMessageLabel
    #check if entered code is valid 
    if codeEntered == correctCode:
            if cheatCodeMessageLabel == None:
                #create and display valid message
                cheatCodeMessageLabel = Label(pausedWindow, text = "Cheat code redeemed", bg = yellowColour, fg = redColour)
                cheatCodeMessageLabel.place(relx =.5, rely = .6, anchor = 'c')
            else:
                #change message text to valid 
                cheatCodeMessageLabel.configure(text = "Cheat code redeemed")
    else:        
            if cheatCodeMessageLabel == None:
                #create and display invalid message
                cheatCodeMessageLabel = Label(pausedWindow, text = "Cheat code invalid", bg = yellowColour, fg = redColour)
                cheatCodeMessageLabel.place(relx =.5, rely = .6, anchor = 'c')
            else:
                #change message text to invalid
                cheatCodeMessageLabel.configure(text = "Cheat code invalid")

def boss_key(event):
    '''Initialise and show boss key window/image'''
    global bossWindow
    #create new fullscreen window with google chrome image and title
    bossWindow = Toplevel()
    bossWindow.grab_set()
    bossWindow.title("Google Chrome")
    bossKeyImageLabel = Label(bossWindow, image = bossKeyImage) 
    bossKeyImageLabel.pack()
    bossWindow.attributes('-fullscreen', True)
    #re-bind b to closing boss image window on next press
    bossWindow.bind("b", close_boss)
    bossWindow.wait_window()

def close_boss(event):
    '''Destroy boss key window/image'''
    global bossWindow
    #destroy boss image window when b clicked
    bossWindow.grab_release()
    bossWindow.destroy()

def show_leaderboard():
    '''Read scores file for levels and times, orders by descending level then ascending time, displays on leaderboard'''
    #create new leaderboard window + title
    leaderboardWindow = Toplevel()
    leaderboardWindow.grab_set()
    leaderboardTitle = Label(leaderboardWindow, fg = redColour, bg = yellowColour, text="Leaderboard", font=("Calibri", 35))
    leaderboardTitle.place(relx =.5, rely = .1, anchor = 'c')

    #create treeview widget 
    treeview = ttk.Treeview(leaderboardWindow, column=("c1", "c2", "c3"), show=["headings"])
    #add column headings 
    treeview.heading("# 1", text="Player")
    treeview.heading("# 2", text="Level")
    treeview.heading("# 3", text="Time")
    #configure column styles 
    treeview.column("# 1",anchor='c', stretch=False)
    treeview.column("# 2",anchor='c', stretch=False,  width=50)
    treeview.column("# 3",anchor='c', stretch=False)
    #initialise list of dictionaries for players on each level 
    scoresDicts =  [{},{},{},{},{},{}]

    try:
        #get stored scores from file if it exists 
        levelsFile = open("Levels File", 'r')
        lines = levelsFile.readlines()

        for line in lines:
            if line != '\n' and line[0:3] != ' **':
                #get player name
                user = line.split(': ')[0] 
                level = line.split(': ')[1]

                #get player's level
                level1 = int(level.strip()[1])
                #get player's previous time
                score = level.strip()[4:]

                if level1 == 1 and score == '0)':
                    pass
                #add player, level and time to relevant dictionary based on level
                elif level1 == 1:
                    scoresDicts[0][user] = (level.strip()).strip(')').strip('(')
                elif level1 == 2:
                    scoresDicts[1][user] = (level.strip()).strip(')').strip('(')
                elif level1 == 3:
                    scoresDicts[2][user] = (level.strip()).strip(')').strip('(')
                elif level1 == 4:
                    scoresDicts[3][user] = (level.strip()).strip(')').strip('(')
                elif level1 == 5:
                    scoresDicts[4][user] = (level.strip()).strip(')').strip('(')
                elif level1 == 6:
                    scoresDicts[5][user] = (level.strip()).strip(')').strip('(')
        levelsFile.close()
                        
    except:
        pass

    n = 5
    count = 0
    prev = 0
    while n>=0:
        #sort player scores by time within each level 
        sortedScores = dict(sorted(scoresDicts[n].items(), key=lambda x:float(x[1][3:])))
        for item in sortedScores:
            #insert player score into treeview widget in sorted order
            prev += 1
            treeview.insert('', str(count), 'item' + str(count), values = (item, str(int(sortedScores[item][0])-1), sortedScores[item][3:]))
            count += 1
        n -= 1 

    #configure treeview widget and display leaderboard window
    treeview.place(relx =.5, rely = .45, anchor = 'c')
    leaderboardWindow.geometry("600x500+360+140")
    leaderboardWindow.title("Leaderboard")
    leaderboardWindow.configure(background = yellowColour)
    leaderboardWindow.mainloop()

def settings():
    '''Initialises and configures settings window with existing customised key values'''
    global settingsWindow
    #initialise new window and widgets for settings 
    settingsWindow = Toplevel()
    settingsWindow.grab_set()
    settingsTitle = Label(settingsWindow, fg = redColour, bg = yellowColour, text="Settings", font=("Calibri", 35))
    settingsTitle.place(relx =.5, rely = .1, anchor = 'c')
    subTitle = Label(settingsWindow, fg = redColour, bg = yellowColour, text="Choose direction control keys:", font=("Calibri", 25))
    subTitle.place(relx =.5, rely = .2, anchor = 'c')
    directionLabels = Label(settingsWindow, fg = redColour, bg = yellowColour, text="Up              Down        Left             Right      ", font=("Calibri", 20))
    directionLabels.place(relx =.5, rely = .3, anchor = 'c')

    #create variables that hold value of pressed radiobuttons 
    global upOption
    global downOption
    global leftOption
    global rightOption
    upOption = IntVar()
    downOption = IntVar()
    leftOption = IntVar()
    rightOption = IntVar()

    global userPlaying
    #open scores file to access current player's stored directions 
    levelsFile = open("Levels File", 'r')
    lines = levelsFile.readlines()
    directionsForUserLine = None
    #loop through lines of file
    for i in range (len(lines)):
        line = lines[i]
        print(i)
        print(line)
        if line != '\n':
            if line.split(': ')[0] == userPlaying:
                #player's score details are on this line
                directionsForUserLine = i+1
            elif i == directionsForUserLine:
                print('here')
                #following line will contain their direction key details 
                check_current_direction(line)

    levelsFile.close()

    #create radiobuttons to select new up direction key settings
    upArrowButton = Radiobutton(settingsWindow, text = '↑', value = 0, indicatoron = 0, variable = upOption) 
    upArrowButton.place(relx =.22, rely = .4, anchor = 'c')
    uButton = Radiobutton(settingsWindow, text = 'U', value = 1, indicatoron = 0, variable = upOption) 
    uButton.place(relx =.27, rely = .4, anchor = 'c')
    #enable relevant button based on current setting
    print(currentU)
    if currentU == 'Up':
        upOption.set(0)
    else:
        upOption.set(1) 

    #create radiobuttons to select new down direction key settings
    downArrowButton = Radiobutton(settingsWindow, text = '↓', value = 0, indicatoron = 0, variable = downOption)  
    downArrowButton.place(relx =.37, rely = .4, anchor = 'c')
    dButton = Radiobutton(settingsWindow, text = 'D', value = 1, indicatoron = 0, variable = downOption)  
    dButton.place(relx =.42, rely = .4, anchor = 'c')
    #enable relevant button based on current setting
    if currentD == 'Down':
        downOption.set(0)
    else:
        downOption.set(1)

    #create radiobuttons to select new left direction key settings
    leftArrowButton = Radiobutton(settingsWindow, text = '←', value = 0, indicatoron = 0, variable = leftOption)  
    leftArrowButton.place(relx =.52, rely = .4, anchor = 'c')
    lButton = Radiobutton(settingsWindow, text = 'L', value = 1, indicatoron = 0, variable = leftOption)  
    lButton.place(relx =.57, rely = .4, anchor = 'c')
    #enable relevant button based on current setting
    if currentL == 'Left':
        leftOption.set(0)
    else:
        leftOption.set(1)

    #create radiobuttons to select new right direction key settings
    rightArrowButton = Radiobutton(settingsWindow, text = '→', value = 0, indicatoron = 0, variable = rightOption)  
    rightArrowButton.place(relx =.67, rely = .4, anchor = 'c')
    rButton = Radiobutton(settingsWindow, text = 'R', value = 1, indicatoron = 0, variable = rightOption)  
    rButton.place(relx =.72, rely = .4, anchor = 'c')
    #enable relevant button based on current setting
    if currentR == 'Right':
        rightOption.set(0)
    else:
        rightOption.set(1)

    #create button to save settings and close window
    finishButton = Button(settingsWindow, width = 20, height = 2, text = "Done", command = close_settings, fg = redColour)
    finishButton.place(relx =.5, rely = .5, anchor = 'c')

    #configure and display window
    settingsWindow.geometry("600x500+360+140")
    settingsWindow.title("Leaderboard")
    settingsWindow.configure(background = yellowColour)
    settingsWindow.mainloop()    

def check_current_direction(line):
    '''Convert direction in file to direction for key press check'''
    global currentU
    global currentD
    global currentL
    global currentR
    #line[3] contains the stored direction character read from file, variables hold key event symbol
    print(line[3])
    print(line)
    if line[3] == '↑':
        currentU = 'Up'
    else:
        currentU = 'u'

    if line[5] == '↓':
        currentD = 'Down'
    else:
        currentD = 'd'

    if line[7] == '←':
        currentL = 'Left'
    else:
        currentL = 'l'

    if line[9] == '→':
        currentR = 'Right'
    else:
        currentR = 'r'
            

def close_settings():

    #get radiobutton values
    uResponse = upOption.get()
    dResponse = downOption.get()
    rResponse = rightOption.get()
    lResponse = leftOption.get()
    
    #destroy settings window
    global settingsWindow
    settingsWindow.grab_release()
    settingsWindow.destroy()

    global level
    i = 0
    lineToUpdate = None
    #open scores file to read and update direction settings
    levelsFile = open("Levels File", 'r')
    lines = levelsFile.readlines()
    newLevels = []
    for i in range (len(lines)):
        #read each line and copy to new version
        line = lines[i]
        newLine = line
        if line != '\n' and line[0:3] != ' **':
            if line.split(': ')[0] == userPlaying:
                #current player's score is on this line so their direction settings are the next line
                lineToUpdate = i+1
        elif i == lineToUpdate:
            #update this file line, and current direction key values, by getting user's direction key choices from radiobutton values
            global currentU
            global currentD
            global currentL
            global currentR
            options = ''
            if uResponse == 0:
                options += '↑,'
                currentU = 'Up'
            elif uResponse == 1:
                options += 'U,'
                currentU = 'u'
            if dResponse == 0:
                options += '↓,'
                currentD = 'Down'
            elif dResponse == 1:
                options += 'D,'
                currentD = 'd'
            if lResponse == 0:
                options += '←,'
                currentL = 'Left'
            elif lResponse == 1:
                options += 'L,'
                currentL = 'l'
            if rResponse == 0:
                options += '→\n'
                currentR = 'Right'
            elif rResponse == 1:
                options += 'R\n'
                currentR = 'r'
            
            newLine = (' **' + options)
        newLevels.append(newLine)
    levelsFile.close()
    #write all lines of new version of file contents to scores file
    levelsFile = open("Levels File", 'w')
    for line in newLevels:
        levelsFile.write(line)
    levelsFile.close()

#initialise global variables used in other modules
global window
global redColour
redColour = "#900000"
global yellowColour
yellowColour = "#FFF0C9"
global level
level = 1
global curRef
curRef = 7
global failedFlag
failedFlag = False
#set valid cheat code
correctCode = "pYth0N"
global cheatCodeMessageLabel
cheatCodeMessageLabel = None
global codeEntered
codeEntered = ''
global currentU
global currentD
global currentL
global currentR
currentU = 'Up'
currentD = 'Down'
currentL = 'Left'
currentR = 'Right'

#call function to create main gameplay window
create_window()

#load and resize all images

#all royalty-free images sourced from https://pngtree.com
global ingredientList
ingredientList = ['mushrooms', 'pepperoni', 'bacon', 'peppers_olives', 'onions', 'tomatoes']
global ingredientDict
#store ingredient images in ingredientDict
ingredientDict = {}
for ingredient in ingredientList:
    ingredientDict[ingredient] = Image.open(ingredient + '.png')
    ingredientDict[ingredient] = ingredientDict[ingredient].resize((150,150))
    ingredientDict[ingredient] = ImageTk.PhotoImage(ingredientDict[ingredient])

    ingredientDict[ingredient+'Red'] = Image.open(ingredient + '_red.png')
    ingredientDict[ingredient+'Red'] = ingredientDict[ingredient+'Red'].resize((150,150))
    ingredientDict[ingredient+'Red'] = ImageTk.PhotoImage(ingredientDict[ingredient+'Red'])

global orderReceipt 
orderReceipt = Image.open('order_receipt.png')
orderReceipt = orderReceipt.resize((150,255))
orderReceipt = ImageTk.PhotoImage(orderReceipt)
global pauseButton 
pauseButton = Image.open('pause_button.png')
pauseButton = pauseButton.resize((100, 100))
pauseButton = ImageTk.PhotoImage(pauseButton)
global pizzaBase 
pizzaBase = Image.open('pizza_base.png')
pizzaBase = pizzaBase.resize((350,350))
pizzaBase = ImageTk.PhotoImage(pizzaBase)
global bossKeyImage
bossKeyImage = Image.open('boss_key.png')
bossKeyImage = bossKeyImage.resize((1440,910))
bossKeyImage = ImageTk.PhotoImage(bossKeyImage)

#bind boss key function 
window.bind("b", boss_key)
#run function to configure window to login screen and set in mainloop
login()
window.mainloop()

