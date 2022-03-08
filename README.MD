# Wordle API
## About the Project: 
The project was inspired by the game Wordle (a word game created by Josh Wardle) and built as a REST API. This implementation of Wordle in Python is meant to be played as a REST API. Each game instance will have a secret word that each user can try to guess. The length of each word is currently set to 5 letters long. Players are allowed only 6 attempts at each word per game. Each guess must be a word from the english dictionary and 5 letters long. After guessing each word, the player will receive some feed back pertaining to the guess and all the guesses made. If the letter in the guess is in the correct position as the letter in the secret word, then it will be noted with the word green. If the letter is in the word but not at the correct position then the letter will be noted with the word yellow by the letter.


## How to use the API:
[API Documentation](https://documenter.getpostman.com/view/15868454/UVsEVoya)

The API will require user authentication to the API. Register with the '/register' route and the login with '/login'. All requests must be in JSON format.

Each player can create an account, and get that account by ID. After creating an account and logging in, each user can create a game instance. Please remember the game_id that you want to make a guess too. Or alternatively, you can call the '/games' to see which game is linked to your account. Only the user who created the game can delete or add/remove users to the game. To add/remove users, use a PUT request with:
```
'add' : *USERS YOU WANT TO ADD* or 'remove' : *USERS YOU WANT TO REMOVE* 
```
After creating a game, you can make guesses to each instance of the game with a POST request. Please refer to the documentation for more information.

## Installation on local machine:
1. Pull files from repository.
``` 
git clone https://github.com/williamle92/wordle_API.git 
```
2. This project is created with .env variables. To create a virtual environment run the following command: 
```
python -m venv venv
```
3. To install all requirements to clone project
```
pip install -r requirements.txt
```
4. Create a .env file
5. Create a SECRET KEY and a JWT SECRET KEY variable in the .env file
6. Link database url: "postgresql://scott:tiger@localhost/mydatabase", for more information please visit: [Flask-SQLAlchemy Configurations](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/)
7. Set up database 
```
flask db init
```
8. migrate 
```
flask db migrate
```
9. Upgrade: 
```
flask db upgrade
```
10. To run on local machine:
```
flask run
```

## Contact
Email: williamkle92@gmail.com