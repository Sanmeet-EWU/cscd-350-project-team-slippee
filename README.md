![Tests Passing](https://github.com/Sanmeet-EWU/cscd-350-project-team-slippee/actions/workflows/tests.yml/badge.svg)

<p align="center">
  <img src="1200px-SF643D_Slippy.webp" alt="logo" width="200" /> 
</p>

## Team Slippee
# ZELDAT
**Z**ELDAT **E**xtracts **L**ocal **D**ata And **T**ranslates


Not all emulator's are built equal, with some performing better on better hardware. Some slow way down in parts that would not be a problem in others, or some games will not even work on them.  

The problem we are trying to solve is that most N64 emulators store the save data in there own way, making it incompatible with other emulators. This is a problem for someone who wants to switch emulators and keep their hard earned save files. As it stands, there are few tools that allow transfer between several emulators, and even less are made for beginners.   

The intended user for this tool is someone who is looking to switch their main emulator and keep there saves. It also is intended to be intuitive and easy to use to ensure that anyone can use it reguardless of their knowledge of computers.  

ZELDAT aims to fix this problem by allowing seamless translation between any of the most common emulators. It extracts the core data of the save and allows conversion to a format that is compatible with the desired emulator. This way, you can float between emulators and figure out which one works best for you without losing progress in your game.

# To Use Program
## Python
1. Clone the repository to a local machine
2. In the cloned directory, run ```pip install -r requirements.txt```
3. In /src, run ```python manage.py runserver```
4. In a browser, go to the address shown in the terminal, or http://127.0.0.1:8000/
5. For information on how to use the program, navigate to the guide page
## Docker
1. Clone the repository to your local machine.
2. Change directory into the project folder.
3. Run the command ```docker build -t <desired_name> .```.
4. Once it is done, run the command ```docker run -d -p8000:8000 <desired_name>```.
5. In a browser, go to the address shown in the terminal, or http://127.0.0.1:8000/
6. For information on how to use the program, navigate to the guide page

# To Run Tests
## For pytest tests
1. ```pip3 install pytest```
2. Change directory into project directory (cscd-350-project-team-slippee)
3. Run ```PYTHONPATH=src pytest```
## For django tests
1. Change directory to location of manage.py (src)
1. Run ```python manage.py test```

[![Contributors](https://img.shields.io/github/contributors/Sanmeet-EWU/cscd-350-project-team-slippee)](https://github.com/Sanmeet-EWU/cscd-350-project-team-slippee/graphs/contributors)  
![Contributors](https://contrib.rocks/image?repo=Sanmeet-EWU/cscd-350-project-team-slippee)

