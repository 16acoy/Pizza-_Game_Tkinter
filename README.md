# Papa's Pizza Making Game

Welcome to Papa's Pizza Making Game, a fun interactive game where you create delicious pizzas by selecting ingredients and placing them on the pizza in a time-bound challenge. Each level introduces new ingredients and challenges, testing your speed and accuracy. Enjoy the excitement of making pizzas while racing against time!

**Features:**

Login system to save player progress.
6 challenging levels, each with different ingredient requirements.
A dynamic and interactive gameplay experience using directional keys.
A pause menu with options to quit or enter cheat codes.
Real-time score tracking with a leaderboard system.

The game uses tkinter for GUI and PIL (from the Pillow library) for image handling.

**How to Play**

_Login:_ Start by entering your player name. If you're a returning player, your progress will be loaded automatically.

_Play:_ Start or resume your pizza-making journey.

_Settings:_ Customize your controls (optional).

_Leaderboard:_ View top scores.

_In-Game Controls:_
Use the arrow keys to move the ingredients and place them on the pizza.
You must place the correct ingredients in the right spot to progress to the next level.

_Pause Menu:_
You can pause the game anytime to resume later or quit the level.

_Cheat Code:_ 
Enter cheat codes to gain advantages in the game, such as taking off time from your score.

_Boss Key:_ Provides a "boss key" feature (default 'b') to disguise the game as a work-related window.

**Gameplay**

Each level introduces a set of ingredients you must place on the pizza in the correct order:

Level 1: Pepperoni

Level 2: Pepperoni, Onions

Level 3: Pepperoni, Onions, Bacon

Level 4: Pepperoni, Bacon, Peppers & Olives, Onions

Level 5: Bacon, Pepperoni, Onions, Tomatoes, Peppers & Olives

Level 6: Onions, Mushrooms, Bacon, Peppers & Olives, Pepperoni, Tomatoes

The ingredients are listed on the order receipt for each level.

_Winning a Level:_

Move ingredients using the arrow keys until they are placed at the center of the pizza.
Place all required ingredients to progress to the next level.
The faster you complete the level, the better your score.

_Failing a Level:_

If you place the wrong ingredient or hit the moving pizza cutter, the level will fail, and you'll need to restart.

**Key Features**

User Progress: Player progress is stored in a file, allowing you to resume from where you left off.

Customization: Players can change directional keys for control.

Cheat Codes: Enter cheat codes to reduce time penalties and boost your chances.

**Files and Configuration**

_Images:_ Ensure that all required images for ingredients, pizza base, and other assets are in the correct directory.

_Levels File:_ A text file used to store user progress and scores.
