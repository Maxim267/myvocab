# myvocab (Python)

**Building a vocabulary by scanning .txt files starting from the base directory.**

Any text outside the `<<word>>` and `<</word>>` tag-only strings is treated as raw file lines. 
Text enclosed in `<<word>>` and `<</word>>` tag-only strings is interpreted as a list of isolated English words, 
which can optionally be converted to their singular or infinitive forms and translated into supported languages.
Set options in the auto-generated base_directory/Myvocab_58b254sv/settings.txt.
This directory contains all program output data.

Please refer to the `doc/instructions` for instructions in Russian.

## Installing tools

Installing Python and adding it to PATH ( >= 3.12, < 3.15):

    https://www.python.org/downloads/

Installing pipx:

    pip install pipx
    pipx ensurepath

Installing Poetry:

    pipx install poetry

Cloning the *myvocab* repository:

    git clone https://github.com/Maxim267/myvocab.git

Opening directory *myvocab*:

Open the *myvocab* project in an IDE (e.g., PyCharm or VS Code).


## Installing myvocab

Copy `.env.example` to `.env` configuration file in the IDE integrated terminal:

    cp .env.example .env

Create a .venv virtual environment in the project root.
Use the `env use` command to tell Poetry which Python version to use for the current project:

    poetry env use C:\full\path\to\python.exe

Display the .venv activation command:

    poetry env activate

Copy the path and activate the .venv:

    C:\full\path\to\myvocab\.venv\Scripts\activate.ps1

Verify that the command line begins with (myvocab-pyx.xx)

Install missing packages and remove unneeded ones:

    poetry sync

To start the program, run the script:

    python myvocab.py

Use the `-D` flag to write debug logs to `app.log`:

    python myvocab.py -D

Use the path argument to define the base directory for parsing:

    python myvocab.py C:\full\path\to\base_directory

## Building and executing `myvocab.exe`

Install missing packages (remove unneeded ones):

    poetry sync --with build_exe

Build `myvocab.exe` using `myvocab.spec`:

    pyinstaller myvocab.spec

The last log line shows the `myvocab.exe` output path:

    INFO: Build complete! The results are available in: C:\full\path\to\myvocab\dist

To launch the program, double-click the executable or run the scripts:

    myvocab.exe
    myvocab.exe -D
    myvocab.exe C:\full\path\to\base_directory

Running the exe from the base directory eliminates the need to specify this path.

## Changing authentication and installing packages

### Using public function to get an IAM token

This is the default authentication.

The `AUTH` variable is defined in the `.env` file as:
```dotenv
   AUTH=function_iam
```
Install packages:

    poetry sync
    poetry sync --with build_exe

### Getting an IAM token for a Yandex account

Set the `AUTH` variable in the `.env` file:
```dotenv
   AUTH=account_iam
```
set the `Yandex account` in `fetch_iam_oauth.py`:
```python
   data = {"yandexPassportOauthToken":"your_Yandex_account"}
```
install packages:

    poetry sync
    poetry sync --with build_exe

### Getting an IAM token using a JWT

Set the `AUTH` and `AUTH_KEY_PATH` variables in the `.env` file:
```dotenv
   AUTH=exchange_jwt_iam
   AUTH_KEY_PATH=C:\full\path\to\authorized_key.json
```
uncomment the line in `fetch_iam_oauth.py`:

```python
   from src.myvocab.authentication.auth_yandex.exchange_jwt_iam.create_iam_token import create_iam_token
```
install packages:

    poetry sync --with jwt
    poetry sync --with jwt --with build_exe

    