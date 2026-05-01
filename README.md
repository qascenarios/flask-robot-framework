# Flask Demo App — Robot Framework Test Automation

A Flask-based demo web application with automated test coverage using [Robot Framework](https://robotframework.org/). Includes both UI tests (via SeleniumLibrary) and API tests (via Python Requests).

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Server & Database Setup](#server--database-setup)
- [Running the Tests](#running-the-tests)
- [Running with Docker](#running-with-docker)
- [API Endpoints](#api-endpoints)
- [Test Coverage](#test-coverage)
- [Test Report](#test-report)

---

## Project Overview

This project demonstrates end-to-end test automation for a Flask REST API and its accompanying web portal. Tests are written in Robot Framework and cover user registration, authentication, and profile management across both the UI and API layers.

---

## Project Structure

```
.
├── Dockerfile
├── requirements.txt
├── run.sh
├── Requests/                   # API request scripts
│   ├── createUsers.py
│   ├── retrieveUser.py
│   ├── retrieveUsers.py
│   ├── tokenGeneration.py
│   └── updateUser.py
└── RobotTest/                  # Robot Framework test suites
    ├── PageObject/
    │   ├── Generic.robot
    │   ├── LoginPage.robot
    │   └── RegisterPage.robot
    └── Tests/
        ├── login.robot
        └── register.robot
```

---

## Prerequisites

- Python 3.8+
- pip
- A modern web browser (Chrome or Firefox) with the matching WebDriver installed
- Flask (`pip install flask`)
- Docker (optional, for containerised execution)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/qascenarios/flask-robot-framework.git
cd flask-robot-framework

# Install Python dependencies
pip install -r requirements.txt
```

---

## Server & Database Setup

> The server and the database must be running at all times for any test to succeed.

### macOS / Linux

**Initialise the database and start the API server:**

```bash
export FLASK_APP=demo_app
flask init-db
flask run --host=0.0.0.0 --port=8080
```

**Start the UI server (separate terminal):**

```bash
export FLASK_APP=demo_app
flask run
```

### Windows

**UI server:**

```bash
set FLASK_APP=demo_app
flask run
```

**API server with database initialisation:**

```bash
set FLASK_APP=demo_app
flask init-db
flask run --host=0.0.0.0 --port=8080
```

---

## Running the Tests

> Ensure the Flask server is running before executing any test suite.

**Run all tests:**

```bash
robot RobotTest/Tests/
```

**Run a specific suite:**

```bash
# UI login tests
robot RobotTest/Tests/login.robot

# UI registration tests
robot RobotTest/Tests/register.robot
```

**Run with a custom output directory:**

```bash
robot --outputdir results RobotTest/Tests/
```

Test artifacts (`output.xml`, `log.html`, `report.html`) are saved to the current directory (or `--outputdir`) after each run.

---

## Running with Docker

```bash
# Build the image
docker build -t flask-robot-app .

# Run the container (API server on port 8080)
docker run -p 8080:8080 flask-robot-app
```

The container automatically initialises the SQLite database on first run via `run.sh`.

---

## API Endpoints

| Method | Endpoint          | Auth Required | Description                      |
| ------ | ----------------- | ------------- | -------------------------------- |
| POST   | `/api/users`      | No            | Register a new user              |
| GET    | `/api/users`      | No            | Retrieve all registered users    |
| GET    | `/api/users/<id>` | Yes           | Get a specific user's details    |
| PUT    | `/api/users/<id>` | Yes           | Update a user's information      |
| POST   | `/api/token`      | No            | Generate an authentication token |

---

## Test Coverage

### A. As a UI user I can:

1. Register through the web portal
2. Review my own user information from the main view

### B. As an API consumer I can:

1. Register new users
2. Review users registered in the system
3. If authenticated, get personal information of users
4. If authenticated, update personal information of users

---

## Test Report

[View Latest Test Report](https://myresult.surge.sh/log.html)
