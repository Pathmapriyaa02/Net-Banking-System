# Net Banking System

A beginner friendly full-stack Net Banking System built with Python Flask, MySQL, SQLAlchemy, Bootstrap, Jinja templates, and JavaScript.

## Features

- User registration, login, logout, session management
- Password hashing with Werkzeug
- Dashboard with balance, statistics, recent transactions, and transfer form
- IMPS transfer simulation with confirmation popup and loading spinner
- Transaction validation, failed transaction handling, rollback state, and error logs
- Admin panel for users and error log review
- Flask Blueprints and MVC-style folder structure
- MySQL database integration using Flask-SQLAlchemy and mysql-connector
- Flash messages, responsive UI, Bootstrap cards and tables

## Folder Structure

```text
Net Banking System/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── services.py
│   ├── utils.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── transactions.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── signup.html
│   │   ├── admin/
│   │   │   └── panel.html
│   │   └── partials/
│   │       └── sidebar.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── database/
│   └── schema.sql
└── logs/
    └── net_banking.log
```

## Transaction Statechart

Success flow:

```text
Initial State -> Idle
Idle -> Logged In using login()
Logged In -> Transaction Initiated using initiate_transaction()
Transaction Initiated -> Payment Authorized using authorize_payment()
Payment Authorized -> Processing using initiate_IMPS_transfer()
Processing -> Completed using confirm_transfer()
Completed -> Validated using validate_transaction()
Validated -> Finalized using finalize_transaction()
Finalized -> Logged using transactions()
```

Failure flow:

```text
Processing -> Failed using transfer_failed()
Failed -> RolledBack using rollback_transaction()
RolledBack -> ErrorLogged using record_error()
```

The implementation lives in `app/services.py`.

## MySQL Setup

1. Start MySQL Server.
2. Open MySQL Workbench or terminal.
3. Run the schema:

```bash
mysql -u root -p < database/schema.sql
```

4. Create `.env` from `.env.example`:

```text
SECRET_KEY=replace-with-a-long-random-secret
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=net_banking
```

## Run in VS Code

1. Open this folder in VS Code.
2. Open the terminal in VS Code.
3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate it on Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the app:

```bash
python app.py
```

7. Open:

```text
http://127.0.0.1:5000
```

## Sample Login Data

The schema creates these users:

```text
admin@example.com
asha@example.com
ravi@example.com
```

Password:

```text
password123
```

Receiver account for successful tests:

```text
100000000003
```

## Test Transactions

Successful transaction:

1. Login as `asha@example.com`.
2. Transfer `1000` to account `100000000003`.
3. Check dashboard balance, recent transactions, and transaction history.

Failed transaction:

1. Login as `asha@example.com`.
2. Transfer an amount larger than the available balance.
3. The status becomes `rolled_back`, final state becomes `ErrorLogged`, and a row is saved in `error_logs`.

Admin panel:

1. Login as `admin@example.com`.
2. Visit `/admin`.
3. Review users and error logs.

## Screenshot Design Ideas

- Login screen with banking background image and a compact login card.
- Dashboard with balance card, success card, failed card, and total sent card.
- IMPS transfer panel beside a recent transaction table.
- Confirmation modal with animated transfer dots and loading spinner.
- Admin panel with users table and error log table.
- Mobile layout where sidebar links stack above dashboard content.

## Secure Coding Practices Used

- Passwords are hashed, never stored as plain text.
- Flask-WTF CSRF protection is enabled through forms.
- Session cookies are HTTP-only and SameSite=Lax.
- SQLAlchemy is used instead of raw string SQL in routes.
- Form validation is enforced on the backend.
- Failed transfers are not debited.
- Application errors are logged using Python logging.
- Sensitive settings are read from environment variables.

## Production Notes

- Replace `SECRET_KEY` before deployment.
- Use HTTPS and keep `SESSION_COOKIE_SECURE=True`.
- Create a dedicated MySQL user with limited permissions.
- Do not use the sample users or dummy data in production.
- Add rate limiting for login attempts before real-world use.
