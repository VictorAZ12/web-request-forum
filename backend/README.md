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
Currently, following pages and functionalities are available:
* `/index`: current index page, available for everyone. In Login tab, you can register and login.
* `/protected`: a protected page, only authenticated users can access. You will be redirected to this page after you logged in successfully. Will be replaced with the user dashboard in the future.
* `/`: a protected page, only authenticated users can access. No functionalities at the moment.
* `/logout`: log out current user.

# Technology Introduction
Flask is a lightweight and versatile web application framework for Python. It's known for its simplicity, flexibility, and ease of use, making it a popular choice for developers ranging from beginners to seasoned professionals. Flask provides the tools and libraries needed to build web applications quickly and efficiently, while still allowing for customization and scalability.

# APIs
# API Documentation

## **Habits API**

<details>
  <summary>GET /api/habits</summary>

### Retrieve all habits of the current user

**Endpoint:** `/api/habits`

**Method:** `GET`

**Authentication:** Required

**Response:**
- **200 OK**

```json
[
    {
        "user_id": "string",
        "habit_name": "string",
        "description": "string",
        "target_date": "string"
    },
    ...
]
```

**Description:** This endpoint retrieves all habits associated with the currently authenticated user.
</details>

<details>
  <summary>POST /api/add_habit</summary>

### Add a new habit for the current user

**Endpoint:** `/api/add_habit`

**Method:** `POST`

**Authentication:** Required

**Request Body:** (Form data)
- `habit_name`: string, required
- `description`: string, not required
- `target_date`: string, required (date format)


**Description:** This endpoint allows the currently authenticated user to add a new habit by submitting a form.
</details>

## **Challenges API**

<details>
  <summary>GET /api/challenges</summary>

### Retrieve all challenges: public and user's private ones

**Endpoint:** `/api/challenges`

**Method:** `GET`

**Authentication:** Required

**Response:**
- **200 OK**

```json
[
    {
        "id": "integer",
        "name": "string",
        "content": "string",
        "public": "boolean",
        "modifiable": "boolean"
    },
    ...
]
```

**Description:** This endpoint retrieves all challenges, including public ones and private ones created by the currently authenticated user.
</details>

<details>
  <summary>POST /api/add_challenge</summary>

### Add a new challenge

**Endpoint:** `/api/add_challenge`

**Method:** `POST`

**Authentication:** Required

**Request Body:** (Form data)
- `challenge_name`: string, required
- `content`: string, required
- `public`: boolean, required


**Description:** This endpoint allows the currently authenticated user to add a new challenge by submitting a form.
</details>