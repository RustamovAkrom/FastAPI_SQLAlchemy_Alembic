# FastAPI SQLAlchemy MIgrations Guide

### Step 1: Getting Up the Enviroment
```
mkdir app
cd app
```
**Now, create a virtual enviroment to isolate our project dependencies:**
```sh
python -m venv venv
source venv/bin/activate # On Windows, use "venv\Scripts\activate"
```
### Step 2: Installing Required Packages
```txt
pip install fastapi[all] uvicorn[standart] sqlalchemy alembic
```
### Step 3: Creating the database
**How that we have defined our model, let`s create the SQLite database and tables**
```sh
alembic init alembic
```
### Step 3: Auto Migration
if you alembic handles migrations follow this method: In the alembic folder edit env.py and find target_metadata line and edit like the following
```py
# alembic/env.py

# NOTE we addedd
from app.db.base import Base
target_metadata = Base.metadata
```
### Step 5: Configuring Alembic
**Open the alembic.ini file in the alembic directory and make the following changes:**
```ini
# alembic.ini
[alembic]
script_location = alembic

sqlalchmey.url = sqlite:///./sqlite3.db # Replace with your database URL if different
```
### Step 6: Generating a Migration
```sh
alembic revision --autogenerate -m "Initial migration"
```
### Step 7: Applying the Migration
```sh
alembic upgrade head
```
### Step 8: Run project
```sh
python main.py
```