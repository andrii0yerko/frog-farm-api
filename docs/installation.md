# Installation
API server is a typical Python application, so you can install it with the next steps

1. Go to the application working folder
```bash
cd ./application
```
Notice that work working is not a root one, this is important for the correct program execution.

2. _(optionally, but recommended)_ Create and activate a venv
```bash
python3 -m venv env
# on Unix-based OS
source env/bin/activate 
# on Windows
env\Scripts\activate.bat
```

3. Install dependencies with
```bash
pip3 install -r ../requirements.txt
```
Dependencies include PyTorch. For portability reasons, requirements.txt includes link for the CPU-only build. If you want to use GPU for the generative model, you should change a corresponding line as specified in the [PyTorch user guide](https://pytorch.org/get-started/locally/).

4. Define environmental variables
```bash
# on Unix-based OS
export DATABASE_URL="dbms://username:password@host:port/database_name"
# if you want to use flask shell
# or run the application with the flask command 
export FLASK_APP="main.py"  
```
```bash
# on Windows
set DATABASE_URL="dbms://username:password@host:port/database_name"
set FLASK_APP="main.py"
```

5. Now you can run it with
```bash
python3 main.py
```