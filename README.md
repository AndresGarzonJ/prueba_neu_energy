# Requirements
- Python >= 3.10.6
- Pip >= 23.3.1
- virtualenv (pip install virtualenv)
- PostgreSQL 14
- OS: Windows 10

# 1. Initial settings
## 1.1 Virtual Environment
##### 1. Navigate to the folder
    cd prueba_neu_energy
##### 2. Create virtual environment
    virtualenv venv --python=python310
##### 3. Activate virtual environment
    source venv/Scripts/activate
##### 4. Install libraries
    pip install -r requirements.txt
##### 5. (Optional) Deactivate virtual environment
    deactivate

## 1.2 Database
##### 1. Configure database settings in the .env file
##### 2. Create database
    cd src/python/db && python create_db.py
##### 3. Create database tables
    python connection_db.py create_tables
##### 4. Load data into tables
    python upload_data.py

# 2. Run solutions
## 1.1 Python Function
##### 1. Navigate to the back folder
    cd ..
    python main.py

## 1.2 PostgreSQL Function
    Not achieved :(