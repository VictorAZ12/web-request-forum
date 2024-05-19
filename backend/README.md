# Deployment Instruction
Install Python and pip if you haven't done so.  
In this folder, create a Python virtual environment, then use it.  
On windows:
```console
python -m venv venv
venv\Scripts\activate
```

On Linux:
```console
python3 -m venv venv
source venv/bin/activate
```

Then, install required packages:
```console
pip install -r requirements.txt
```

Run the program with
```console
flask run
```
Th tsting folder will run at 127.0.0.1:5000/. 
Currently, following pages and functionalities are available:
* `127.0.0.1:5000/index`: current index page, available for everyone. In Login tab, you can register and login.
* `127.0.0.1:5000/dashboard`: user dashboard, a user will be redirected to here after login.


# Technology Introduction
Flask is a lightweight and versatile web application framework for Python. It's known for its simplicity, flexibility, and ease of use, making it a popular choice for developers ranging from beginners to seasoned professionals. Flask provides the tools and libraries needed to build web applications quickly and efficiently, while still allowing for customization and scalability.
