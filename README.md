# Countdown Game
(Developer: Matthew Shepherd)

![Mockup image](docs/amiresponsivepp3.PNG)

[Live webpage](https://countdown-game-ccaca8c4e1a7.herokuapp.com/)

## Table of Content

1. [Project Goals](#project-goals)
    1. [User Goals](#user-goals)
    2. [Site Owner Goals](#site-owner-goals)
2. [User Experience](#user-experience)
    1. [Target Audience](#target-audience)
    2. [User Requirements and Expectations](#user-requirements-and-expectations)
    3. [User Stories](#user-stories)
3. [Technical Design](#design)
    1. [Design Choices](#design-choices)
    2. [Colour](#colours)
4. [Technologies Used](#technologies-used)
    1. [Languages](#languages)
    2. [Frameworks & Tools](#frameworks-&-tools)
5. [Features](#features)
6. [Testing](#testing)
    1. [Browser compatibility](#browser-compatability)
    2. [PEP8 Python Validator](#PEP8-Python-Validator)
    3. [Manual Testing](#manual-testing)
    4. [Automated Testing](#automated-testing)
    5. [Testing user stories](#testing-user-stories)
8. [Bugs](#Bugs)
9. [Deployment](#deployment)
    - [Deploying in Heroku](#deploying-the-website-in-heroko)
    - [Forking the GitHub Repository](#forking-the-github-repository)
    - [Cloning of Repository i GitHub](#cloning-the-repository-in-github)
10. [Credits](#credits)
11. [Acknowledgements](#acknowledgements)

## Project Goals 
The goals of this app include:

### Site Owner Goals
- Create a fun interactive game that furthers my understanding of problem solving through code and the Python language
- Create an attractive and easy to use game
- Ensure the user understands the rules of the game
- Ensure the user is provided with clear instructions on how to play on each screen
- Ensure the user is provided with clear feedback on any errors and how to proceed
- Allow the user to keep track of their score in the game
- Allow the user to have thier score displaye don the leaderboard if it is a top ten high score

### User Goals
- Play a fun and interactive online numbers and words puzzle game similar to the U.K. T.V. gameshow Countdown 
- Quickly understand the rules of the game and how to play
- Be able to keep track of the game score and to try to beat their previous high score
- Play the game as often as desired
- Achieve a top ten high score that appears on the game leaderboard

[Back to Table of Contents](#table-of-contents)

## User Experience

### Target Audience
- Countdown is typically played by anyone age 12 and up, that can follow the rules to solve challenging word and number games.

### User Requirements and Expectations
- An intuitive and easy to navigate game interface
- A fun and educational gameplay experience with feedback on word and number game solutions
- Ability to quickly find game rules, view the score leaderboard, or start the game
- Ability to personalise the game by entering a player name
- Score tracking during the game and feedback if a top ten score is achieved
- Clear feedback on any input errors during gameplay and how to proceed
- Ability to have their name and score added to the leaderboard if a top ten score is achieved


### User Stories
I have divided my user stories into users and the site owner, as each of these users will have a distinct set of needs and goals.

#### Users
1. As a user, I want...


#### Site Owner 
13. As a site owner, I want...

[Back to Table of Contents](#table-of-contents)

## Technical Design

### Flowchart


### Data Model


[Back to Table of Contents](#table-of-contents)

## Technologies Used

### Languages
- Python

### Tools
- Git
- GitHub
- CodeAnywhere

### Python Libraries
[time](https://docs.python.org/3/library/time.html)
[re](https://docs.python.org/3/library/re.html)
[random](https://docs.python.org/3/library/random.html)
[termios](https://docs.python.org/3/library/termios.html)
[sys](https://docs.python.org/3/library/sys.html)
[tty](https://docs.python.org/3/library/tty.html)
[collections](https://docs.python.org/3/library/collections.html)

### Third Party Python Libraries
[PyDictionary](https://pypi.org/project/PyDictionary/)
[Colorama](https://pypi.org/project/colorama/)
[Alt-profanity-check](https://pypi.org/project/alt-profanity-check/)
[Numexpr](https://pypi.org/project/numexpr/2.6.1/)
[Pager](https://pypi.org/project/pager/)
[Inputimeout]()
[Art]()
[Num2words]()
[Countdown_numbers_solver]()
[gspread]()
[google.oauth2.service_account]()
[prettytable]()
[]()


[Back to Table of Contents](#table-of-contents)

## Features
The app consists of...

### Intro Screen
- 

![Intro Screen]()

### Enter Name Screen
- 

![Enter Name Screen]()


[Back to Table of Contents](#table-of-contents)

## Testing

### Browser compatability
The website was tested on the following browsers:
- Google Chrome
- Mozilla Firefox
- Microsoft Egde

### PEP8 Python Validator
The PEP8 Python Validator (from Code Institute) was used to validate all Python code. All files pass with no errors no warnings to show.
<details>
<summary>Run.py</summary>

</details>


### Manual Testing


### Automated Testing



### Testing user stories

1. As a user, 

| **Feature** | **Action** | **Expected Result** | **Actual Result** |
|-------------|------------|---------------------|-------------------|
| | | |
| | | |
| | | |

<details><summary>Screenshots</summary>

</details>


14. As the site owner,  

| **Feature** | **Action** | **Expected Result** | **Actual Result** |
|-------------|------------|---------------------|-------------------|
| | | |
| | | |
| | | |


<details><summary>Screenshots</summary>

</details>

15. As the site owner, 

| **Feature** | **Action** | **Expected Result** | **Actual Result** |
|-------------|------------|---------------------|-------------------|
| | | |
| | | |
| | | |

<details><summary>Screenshots</summary>

</details>


## Bugs

| **Bug** | **Fix** |
| ----------- | ----------- |
| | |
| | |
| | |
| | |


[Back to Table of Contents](#table-of-contents)

## Deployment

### Deploying the website in Heroko:
- The website was deployed to Heroko using following steps:
#### Login or create an account at Heroku
- Make an account in Heroko and login

<details>
    <summary>Heroko Login Page</summary>
    <img src="assets/heroku/heroku_login.png" alt="Heroko login page">
</details>

#### Creating an app
  - Create new app in the top right of the screen and add an app name.
  - Select region
  - Then click "create app".

<details>
    <summary>Create App</summary>
    <img src="assets/heroku/createapp.png" alt="Heroko create app screenshot">
</details>

#### Open settings Tab
  ##### Click on config var
  - Store CREDS file from gitpod in key and add the values
  - Store PORT in key and value

<details>
    <summary>Config var</summary>
    <img src="assets/heroku/config.png" alt="Config var screenshot">
</details>

  ##### Add Buildpacks
  - Add python buildpack first
  - Add Nodejs buildpack after that

<details>
    <summary>Buildpacks</summary>
    <img src="assets/heroku/buildpacks.png" alt="Buildpacks screenshot">
</details>

 #### Open Deploy Tab
   ##### Choose deployment method
  - Connect GITHUB
  - Login if prompted

<details>
    <summary>Deployment method</summary>
    <img src="assets/heroku/method.png" alt="Deployment method screenshot">
</details>

   ##### Connect to Github
  - Choose repositories you want to connect
  - Click "Connect"

<details>
    <summary> Repo Connect</summary>
    <img src="assets/heroku/repo-connect.png" alt="Repo connect screenshot">
</details>

  ##### Automatic and Manual deploy
  - Choose a method to deploy
  - After Deploy is clicked it will install various file

<details>
    <summary> Deploy methods</summary>
    <img src="assets/heroku/deploy.png" alt="deploy method screenshot">
</details>

  ##### Final Deployment
  - A view button will display
  - Once clicked the website will open

<details>
    <summary> Deploy</summary>
    <img src="assets/heroku/view.png" alt="view screenshot">
</details>

### Forking the GitHub Repository
1. Go to the GitHub repository
2. Click on Fork button in top right corner
3. You will then have a copy of the repository in your own GitHub account.
4. [GitHub Repository](https://github.com/mat-shepherd/CI_PP3_COUNTDOWN_GAME)

### Cloning the repository in GitHub
1. Visit the GitHub page of the website's repository
2. Click the “Clone” button on top of the page
3. Click on “HTTPS”
4. Click on the copy button next to the link to copy it
5. Open your IDE
6. Type ```git clone <copied URL>``` into the terminal

[Back to Table of Contents](#table-of-contents)

## Credits

### Content
In order of appearance:

Index Page
- [Image](https://www.hubspot.com/brand-kit-generator/) by [Author](https://www.hubspot.com/)
    <details><summary>Logo</summary>
    <img src="docs/credits/logo-variations.webp">
    </details>   

  
### Code
The markdown structure of this readme was based on the structure of the following readme.md files from other Code Institute student projects:
- https://github.com/4n4ru/CI_MS1_BodelschwingherHof
- https://github.com/jamie2210/CI_MS1_TBC
- https://github.com/jeremyhsimons/CI_PP3_DungeonEscape

The deployment steps for the project were adapted from the following readme.md file by Jeremy Simons:
- https://github.com/jeremyhsimons/CI_PP3_DungeonEscape

[Back to Table of Contents](#table-of-contents)

## Acknowledgements
- My mentor Mo Shami for your support, guidance, and encouragement as always!
- Alan Bushell and the February 2023 Student Cohort for their knowledge sharing, advice, and camaraderie during our weekly standup calls and in Slack
- ... for reviewing my project and providing great constructive feedback
- The Code Institute and their tutor support team for an excellent experience and great support leading up to this second project
- My wife for her exceptional patience and support while I sat in front of the computer for days on end and for listening to my constant updates and ramblings about this third project
- My son  William for helping me test the game, providing feedback and ideas, and for spotting bugs!

[Back to Table of Contents](#table-of-contents)