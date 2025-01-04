# Signant

## Tests Coverage:

### A. As a UI user I can:
1. Register through web portal
2. Review my own user information from the main view

### B. As an API Consumer I can:
1. Register new users
2. Review users registered in system
3. If authenticated, get personal information of users
4. If authenticated, update personal information of users

### Test Result
[Test Report](https://myresult.surge.sh/log.html)

### Server and Database Setup:
- The server and the database must be connected at all times for any executed test to be successful.

#### On Windows:
**UI server:**
```bash
set FLASK_APP=demo_app
flask run
```

**API database:**
```bash
set FLASK_APP=demo_app
flask init-db
flask run --host=0.0.0.0 --port=8080
```
