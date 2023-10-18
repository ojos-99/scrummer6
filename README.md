# FIT2101 Project

## Installation

1. Clone the repository: `https://git.infotech.monash.edu/FIT2101-S2-2023/CL_Thursday6pm_Team3/project.git`
2. Navigate to the project directory: `cd project`
3. (Optional) Create and Activate a virtual environment: `python -m venv venv` and `venv\Scripts\activate`
4. Install the requirements (assuming you have pip installed):
`pip install -r requirements.txt` 


## To Run

-   run `python manage.py runserver` in the terminal in the root directory

## Create admin user

-   run `python manage.py createsuperuser` and then enter your details

## If you make changes to the model/database

-   run `python manage.py makemigrations [app]` to update and store as migration
-   run `python manage.py runserver` to apply migration operations

## Git Workflow

-   run `git add .` in the terminal in the root directory to add all your files
-   run `git commit -m "[message]"` in the terminal in the root directory to commit all your files and add a meaningful message to describe what you've done
-   run `git push` in the terminal in the root directory to push your changes to the remote repository

## If you want to enable password reset feature

-   In settings.py, replace line 140 with password listed here: https://docs.google.com/document/d/1lWfqZ7zaaHyHOhH_5lIjyU5-PEK0XIxTh4z1yBaTWTE/edit