# Forest Exploration

Forest Exploration is a Python terminal game, which runs on the Code Institute mock terminal on Heroku. It is a text-based game in which the player explores a randomly generated forest, accumulates points and searches for an amulet. The player wins by using the amulet and can then save their score and stats to the game leaderboard.
This product was made to provide a fun gaming experience that people can access online. It was designed such that multiple people can play and compare their scores on the game leaderboard.

![Responsive Mockup](/readme_images//responsive.webp)

## How To Play

A tutorial and 'help' list of all valid moves are provided in-game. The user should utilise the available commands to travel around the map, collecting items and defeating enemies. The ultimate goal is to accumulate points and end the game by using an item named 'amulet', which is found somewhere on the board. Points are accumulated by defeating enemies and healing sick animals.

## Generation Features

**Random Item Generation**

- The game randomly generates items, animals and enemies for each new area.
- The `generate_items` function in `resources/item.py` and `generate_entities` function in `resources/entity.py` handle the generation of items and entities respectively. These are then utilised by the `Area` class in `resources/area.py`.
- This bolsters the UX by ensuring a different experience every time the user plays.

**Area Description Generation**

- The game randomly generates descriptions for each new area entered from a list of phrases.
- This helps the user orient themselves on the map as they may remember the area descripton. It also fosters game immersion by adding to the fantasy of the game.

## Game Introduction Features

**Tutorial Choice**

- The program starts with a console prompt to the user to answer whether it is their first time playing. 
If so, a tutorial is printed. This ensures the user knows the goal of the game and is able to play properly.
- The console then prompts the user to press any key to continue. This ensures that only the tutorial is on screen
at this time and ensures a postive UX by not overloading the user with information.
- The tutorial can also be printed at any time throughout the game if the user enters the command 'tutorial'.

<details>
<summary> Tutorial Choice Screenshot </summary>

![Tutorial Choice Screenshot](/readme_images/tutorial_choice_screenshot.webp)

</details>

<hr>

**Board Choice**

- After the tutorial choice prompt, the user is prompted to enter a board size they wish to play on.
- The user is presented with three abstracted choices: small, medium or large. They ensures the chosen board size
is always one of three tested choices and the board size is never too large or too small.
- The user's input is validated and the game does not move on until the user enters a valid option.

<details>
<summary> Board Choice Screenshot </summary>

![Board Choice Screenshot](/readme_images/board_choice_screenshot.webp)

</details>
<hr>

**Introduction Information**

- Following the tutorial and board choices, the game starts with introduction information being printed to the user. The first area description is printed
along with an extra line giving the context of the forest location of the game.
- This starts the user off with some information to respond to rather than leaving them to find the look 
command themselves.

<details>
<summary> Introduction Information Screenshot </summary>

![Introduction Information Screenshot](/readme_images/introduction_screenshot.webp)

</details>

## Command Features

The command features are inputs the user can enter throughout the game to interact with items, entities and the environment.

**Help Command**

- The user can input the 'help' command to print a list of all valid commands used in the game.
- A message reminding the user of the 'help' command prints above every prompt for new input in the game.
- This ensures the user can always find the command they need without scrolling up on the console or checking the README,
creating a better UX.

<details>
<summary> Help Command Screenshot </summary>

![Help Command](/readme_images/help_command_screenshot.webp)

</details>
<hr>

**Inventory Command**

- The user can input the 'inventory' command to print their inventory to the console.
- This allows them to utilise the 'use' and 'describe' commands effectively, as they do not need to keep track of what items they have picked up, used or dropped.

<details>
<summary> Inventory Command Screenshot </summary>

![Inventory Command](/readme_images/inventory_command_screenshot.webp)

</details>
<hr>

**Status Command**

- The user can input the 'status' command to print the user's health and score to the console.
- This allows the user to make more informed choices during the game, and improves the UX by ensuring users do not have to keep track of their health and score themselves.
- The user can also input 'status of (entity)' to find the status of an entity in the area. This makes enemy battles more interesting, as players can utilise strategy in which enemy they target first and with which item, improving the UX.
- If an invalid 'status of' command is entered, the console prints a message to explain this. Only 'status of' commands referencing entities in the current area are considered valid, as to maintain the fantasy of occupying only one location at a time.

<details>
<summary> Status Command Screenshot </summary>

![Status Command](/readme_images/status_command_screenshot.webp)

</details>
<details>
<summary> Status Of Command Screenshot </summary>

![Status Of Command](/readme_images/status_of_command_screenshot.webp)

</details>
<details>
<summary> Status Of (Invalid) Command Screenshot </summary>

![Invalid Status Command](/readme_images/status_invalid_screenshot.webp)

</details>
<hr>

**Look Command**

- The user can input the 'look' command to print the current area's description in detail. This includes a brief description of the environment, what entities are present (enemies, animals) and what items are present.
- Though the area's description is printed automatically when an area is entered, the 'look' command allows the user to remind themselves of the current state of the area after entering other commands that may have affected any present entities or items.

<details>
<summary> Look Command Screenshot </summary>

![Look Command](/readme_images/look_command_screenshot.webp)

</details>
<hr>

**Punch Command**

- The user can input the 'punch (entity)' command to perform a weak attack on an animal or enemy and lower their health.
- The ensures that even when the user has no items, they are not powerless against enemies. Since using an item affects the item's durability, it can also be a strategic choice when enemies are on low health, making the game more strategy based and creating a better UX.

<details>
<summary> Punch Command Screenshot </summary>

![Punch Command](/readme_images/punch_command_screenshot.webp)

</details>
<details>
<summary> Punch (Invalid) Command Screenshot </summary>

![Punch Command](/readme_images/punch_invalid_screenshot.webp)

</details>
<hr>

**Flee Command**

- The user can input the 'flee' command when in battle to attempt movement to a nearby area.
- This ensures that users who encounter multiple powerful enemies can continue playing the game without dying.
- The 'flee' command moves the player in a random direction, and has a chance of failing. This provides an incentive to stay and fight enemies, making the user experience all aspects of the game and creating a better UX.

<details>
<summary> Flee Command Screenshot </summary>

![Flee Command](/readme_images/flee_successful_screenshot.webp)

</details>
<details>
<summary> Flee (Unsuccessful) Command Screenshot </summary>

![Flee Unsuccessful Command](/readme_images/flee_unsuccessful_screenshot.webp)

</details>
<details>
<summary> Flee (Invalid) Command Screenshot </summary>

![Flee Invalid Command](/readme_images/flee_invalid_screenshot.webp)

</details>
<hr>

**Map Command**

- The user can input the 'map' command to print the map at any time.
- The map is made up of emojis so that it is easily readable.
- This allows the user to easily orient themselves, ensuring they do not have to keep track of player location themselves, and therefore fostering a better UX.

<details>
<summary> Map Command Screenshot </summary>

![Map Command](/readme_images/map_command_screenshot.webp)

</details>
<hr>

**Key Command**

- The user can input the 'key' command to print a key explaining the emojis that make up the map.
- Though the map emojis were chosen to be easily understable, the 'key' command ensures that no user will be confused by the map, improving UX.

<details>
<summary> Key Command Screenshot </summary>

![Key Command](/readme_images/key_command_screenshot.webp)

</details>
<hr>

**Describe Command**

- The user can input the 'describe' command to receive a brief description of any item in their inventory.
- This allows users to plan when they will use items as they have some foreknowledge of the items' features, improving UX.
- If the user attempts to print a description of an item not in their inventory, a message advising them this item is not in the inventory will be printed. This ensures users do not gain knowledge of items they have not yet encountered.

<details>
<summary> Describe Command Screenshot </summary>

![Describe Command](/readme_images/describe_command_screenshot.webp)

</details>
<details>
<summary> Describe (Invalid) Command Screenshot </summary>

![Describe Invalid Command](/readme_images/describe_invalid_screenshot.webp)

</details>
<hr>

**Use Command**

- The user can input the 'use' command to utilise an item in their inventory.
- This allows the user to utilise a variety of items.
- The user can also input 'use (item) on (entity)' to use the item on another creature. This allows weapons to be used on enemies and animals to be healed.
- Attemping to use a weapon without specifing an entity to be targeted will result in an advice message being printed that the user must enter an entity to target. This ensure that commands like 'use sword' do not assume the player as the target and ensures the user does not accidentally attack themselves.

<details>
<summary> Use Command Screenshot </summary>

![Use Command](/readme_images/use_single_command_screenshot.webp)

</details>
<details>
<summary> Use (Invalid) Command Screenshot </summary>

![Use Command](/readme_images/use_single_invalid_screenshot.webp)

</details>
<details>
<summary> Use On Command Screenshot </summary>

![Use Command](/readme_images/use_command_screenshot.webp)

</details>
<details>
<summary> Use On (Invalid) Command Screenshot </summary>

![Use Command](/readme_images/use_invalid_screenshot.webp)

</details>
<hr>

**Take Command**

- The user can input the 'take (item)' command to pick up items from the ground.
- This allows items to be generated on the ground around the map, allowing players a chance to find items before fighting any enemies.

<details>
<summary> Take Command Screenshot </summary>

![Take Command](/readme_images/take_command_screenshot.webp)

</details>
<details>
<summary> Take (Invalid) Command Screenshot </summary>

![Take Invalid Command](/readme_images/take_invalid_screenshot.webp)

</details>
<hr>

**Drop Command**

- The user can input the 'drop (item)' command to drop items. They may choose to do this if their inventory is becoming crowded with duplicate items.
- This command could have future utilisation if a carrying capacity was introduced.

<details>
<summary> Drop Command Screenshot </summary>

![Drop Command](/readme_images/drop_command_screenshot.webp)

</details>
<details>
<summary> Drop (Invalid) Command Screenshot </summary>

![Drop Invalid Command](/readme_images/drop_invalid_screenshot.webp)

</details>
<hr>

**Search Command**

- The user can input the 'search (entity)' command to search dead enemies for items.
- This provides a reward for completing the task of killing enemies, motiving the player to kill more enemies and continue the gameplay loop, ultimately providing a better UX.
- Searching an enemy more than once will not result in any additional items. This is to retain the difficulty balance of the game and maintain the fantasy of real objects that have been collected and are no longer present on the enemy.

<details>
<summary> Search Command Screenshot </summary>

![Search Command](/readme_images/search_command_screenshot.webp)

</details>
<details>
<summary> Search (Invalid) Command Screenshot </summary>

![Search Invalid Command](/readme_images/search_invalid_screenshot.webp)

</details>
<hr>

**Go Command**

- The user can input the 'go (direction)' command to travel around the map.
- Attempting to move outside the map results in an advisory message that the player cannot move in this direction, ensuring no errors occur in the code.
- Attempting to use the 'go' command with any direction other than 'north', 'east', 'south' or 'west' results in an advisory message being printed which suggests these options. This ensures that anyone using the 'go' command incorrectly is notified of the correct way to use the command, improving the UX.

<details>
<summary> Go Command Screenshot </summary>

![Go Command](/readme_images/go_command_screenshot.webp)

</details>
<details>
<summary> Go (Unsuccessful) Command Screenshot </summary>

![Go Unsuccessful Command](/readme_images/go_unsuccessful_screenshot.webp)

</details>
<details>
<summary> Go (Invalid) Command Screenshot </summary>

![Go Invalid Command](/readme_images/go_invalid_screenshot.webp)

</details>
<hr>

**Quit Command**

- The user can input the 'quit' command to exit the game at any time.
- A brief goodbye message is printed so that the user receives feedback of their action and knows the game has quit correctly.

<details>
<summary> Quit Command Screenshot </summary>

![Quit Command](/readme_images/quit_command_screenshot.webp)

</details>


## Leaderboard Features

**Save Game to Leaderboard**

- The user has the option to save their game to the leaderboard at the end of the game. This allows different users to compare their scores and adds a fun social element to the game that improves UX.
- The user must enter a name so that they can identify their details on the leaderboard. If the name is over 9 characters, the user is printed an advisory message to enter a name of 9 characters or less and the question is reprinted.

<details>
<summary> Save Game Screenshot </summary>

![Save Game](/readme_images/save_game_screenshot.webp)

</details>
<hr>

**Print Leaderboard**

- The leaderboard is printed at the end of every game. This allows users to see others scores and see how their own scores compare.

<details>
<summary> Print Leaderboard Screenshot </summary>

![Print Leaderboard](/readme_images/leaderboard_screenshot.webp)

</details>


## Features Yet to be Implemented

Forest Exploration is a finished and functional online text adventure. However, certain features could be implemented to improve the product in the future.

1. **Items that affect score:**
    - The game currently includes two ways the player can increase their score: killing enemies and healing sick animals.
    - One feature that could improve and the game and UX is another item type that increases the score directly. This would make finding items on the ground and on enemies more interesting.
2. **Enemy variations:**
    - All enemies in the game essentially function the same. They are instances of the Enemy class, with differing names and effect names but the same functionality.
    - The game would have more variety and provide a better UX if each enemy had different functionality.
    - This could be implemented by adding new enemies as children of the Enemy class.
3. **Item carrying capacity:**
    - The user starts the game with two items in their inventory and can find items in areas and on enemies throughout the game. 
    - Though the user is unlikely to accumulate a large amount of items, particularly on the small and medium board sizes, this can potentially happen and the user has to scroll to view all of their items. It may also be hard for the player to keep track of all their items.
    - A better UX could be provided if an item carrying capacity was introduced, so the player can only carry so many items at a time. The Item class could also have a weight attribute and the carrying capacity would be limited by the sum of the all the items' weights. This would add an additional strategy element to gameplay.
    - An alternative solution to the same problem would be implementing a more compact manner of printing the inventory to the user.
4. **Graphical UI:**
    - The game was created from the start to be a text-based adventure. However, it could be adapted to a simple UI with relatively little work. The console could remain for the player to enter their commands, but with the player's inventory and the board map viewable at all times on the page. 
    - Though this would change the nature of the product somewhat, it could potentially improve UX by allowing the user to better understand the location of their player and their items without clogging up the console with the 'map' and 'inventory' commands.

## Data Models

The product utilises various data models. All items are instances of either the `HealthItem` or `Amulet` classes found in `resources/item.py`, both children of the abstract `Item` class. The use of an abstract parent class allows all items to share certain attributes and methods, such as a name and durability. The models are easily scalable, as any additional item types could be added with `Item` as their parent.

All entities (animals, enemies, and the player) are instances of the `Entity` and `Enemy` classes found in `resources/entity.py` and the `Player` class found in `resources/Player.py` respectively. This allows all entities to share common attributes and methods such as the `apply_affect` method. This also allows for scability as new entity types could be added with the `Entity` class as their parent.

## Manual Testing 

|  Feature |  Testing action | Outcome |
|---|---|---|
|Board Choice|Attempt to enter erroneous inputs.|Console prints message advising user to enter 'small', 'medium' or 'large', then repeats question.|
Use Command|Attempt to use an item that does not exist.|An advisory message is printed that the item does not exist.|
|Status Command|Attempt to find the status of an enemy in the area.|The enemy's health is printed to the console.|
|Status Command|Attempt to find the status of an enemy that does not exist in that area.|An advisory message is printed that the enemy does not exist in that area.|
Go Command|Attempt to move outside of map.|Initial testing produced [bug three](#bug_three). After resolving, an advisory message is printed to the user that they cannot move in this direction. |
Save Game to Leaderboard|Attempt to enter invalid name.|Console prints message advising user to enter name of 9 characters or less, then repeats question.|
Save Game to Leaderboard|Attempt to save a game after playing.|The game details are added to the leaderboard and displayed on all future games.
<br>

## Validator Testing 

#### Python
- No syntax issues or PEP8 style issues returned using <a target="_blank" href="https://docs.astral.sh/ruff/">Ruff linter</a>.

## Bugs

|  Bug Number |  Problem | Outcome |
|---|---|---|
|1 |New items found in the game have unexpectedly low durability.| Solved
|2 |Searching enemies always returning no items.| Solved
|3 |List indexing error when attempting to move off map.| Solved
|4 |Modules not importing correctly.| Solved

<br>

**1.**
- When testing the game in its development, I found some items I was acquiring were breaking quicker than I had intended them to. 
- For example, the 'sword' item was meant to have a durability of 5 uses, but was breaking after 1 use.
- I had implemented the item generation by creating a tuple of `HealthItem` objects that the `generate_items` function would iterate through.
- The generator was only creating references to the original tuple objects, which meant that once an item's durability had broken down, all subsequent items acquired of the same item type would retain the same durability. This meant that once the sword's durability had been worn down to 0 the first time, it broke at the first time its durability was checked on subsequent acquirings.
- I resolved the issue by changing the nature of item generation. The tuple in question (`HealthItem.ITEMS` in `resources/item.py`) is now a two-dimensional tuple that holds the arguments for a possible `HealthItem`. A new `HealthItem` object is instantiated every time the `generate_items` function in `resources/item.py` selects it for generation.

**2.**
- In the game, players can search dead enemies using the 'search' command - this sometimes returns items. Testing during development found that searching enemies was never returning items.
- The public `search` method of the `Enemy` class in `resources/entity.py` returns the enemy's 'loot' (items) so that they can be added to the player's inventory. It then sets the private `_searched` attribute to `True`. The enemy cannot be searched twice, as the the `search` method checks if `_searched` is `False` before returning the items. If it is `True`, it simply returns an empty list.
- The `search` method was always evaluating `_searched` to `True` and therefore never returning the enemy's items. This was due to a typing error in the public `apply_affect` method of the parent `Entity` class. The `apply_affect` method was accidentally setting `_searched` to a non-empty string. Since non-empty strings evalute to `True`, this meant that any `Entity` object for which the `apply_affect` method had been called had a `True` `_searched` attribute.
- The typing error in `affect_health` was corrected, resolving the issue.

<a name="bug_three"></a>
**3.**
- When testing the game during development, I attempted to make an illegal move using the 'go' command that would take my player off the map.
- This prompted an `IndexError` to be raised.
- The problem was in the `GameBoard` class in `resources/game_board.py`. The private `GameBoard` method `_move_is_on_map` checks if a coordinates are on the map and returns `True` if they are, `False` if they are not. This in this then utilised in the public `move` method of `GameBoard` to check a potential move is valid.
- The `_move_is_on_map` private method was functioning incorrectly. It used greater than or equal to operators (>=) rather than greater than (>) operators when evaluating its argument set of coordinates as compared to the board size. This meant it would return `True` for an extra row and column that were not actually valid moves. Then, when the `move` method attempted to use the index, the `IndexError` exception was raised.
- The operators were corrected to greater than operators and the issue was resolved.

**4.**
- After initially developing the product with all Python files in the main directory, I decided that the product would be better organised if all Python files apart from `run.py` were in a separate subdirectory. I moved the files to the `resources` folder, and changed the `import` statements in `run.py` to accomodate this.
- This caused a `ModuleNotFoundError` to be raised, traceable to an `import` statement in `resources/leaderboard.py`.
- I had not realised that the working directory for the files in the `resources` folder would still be the main directory. `resources/leaderboard.py` was the first module to be imported to `run.py` that tried to import another file from the `resources` folder without referencing its directory in its `import` statement.
- As such, I changed all the `import` statements of the files in the `resources` folder to reflect this, resolving the issue.


## Deployment

- The site was deployed to Heroku using the following steps: 
  - Sign up or log in to <a target="_blank" href="https://www.heroku.com">Heroku</a>.
  - Create an new app.
  - Add any necessary environment variables to 'config vars' in settings. For example, the Google API credentials in this product.
  - Add any relevant buildpacks and ensure they are in the right order. Python and Node.js (JavaScript backend) were used for this product.
  - Connect the Heroku app to the GitHub repo in the deploy section.
  - Enable automatic deploys if desired. Automatic deploys were utilised for the deployment of this project.

The live link can be found here - <a target="_blank" href="https://forest-exploration-d70fdb263fd5.herokuapp.com/">https://forest-exploration-d70fdb263fd5.herokuapp.com/</a>.


## Credits 

All content apart from where stated below is my own work:

- emoji library by <a target="_blank" href="https://pypi.org/project/emoji/2.12.1/">Taehoon Kim</a>.
- gspread library by <a target="_blank" href="https://pypi.org/project/gspread/">Anton Burnashev</a>.
- google.oauth2.service_account module by <a target="_blank" href="https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html">Google</a>.
- Leaderboard spreadsheet made with Google Sheets and hosted by Google.
- Page structure to accomodate Python console from Code Institute.
- Syntax validation and PEP8 style format checks from <a target="_blank" href="https://docs.astral.sh/ruff/">Ruff linter</a>.

