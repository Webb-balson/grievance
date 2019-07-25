# grievance
Grievance Redressal Portal


## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/Webb-balson/grievance.git
```
Start a virtual environment:
```bash
virtualenv venv -p python3.6
```
Initialize the virtualenv:
```bash
source venv/bin/activate
```
Get inside the directory:
```bash
cd grievance
```
Create a .env file and setup the local configurations:
```bash
cp .env .env
```
Install the requirements:

```bash
pip install -r requirements.txt
```
Create the database:

```bash
python manage.py migrate
```
Collect static files:
```bash
python manage.py collectstatic
```
Now create a super user for the application:
```bash
python manage.py createsuperuser
```
Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.
