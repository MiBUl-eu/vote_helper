# load .env file
set dotenv-load

@_default:
  just --list

# setup virtual environment, install dependencies
venv:
  [ -d .venv ] || python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt

# upgrade all installed pip packages
upgrade: venv
  ./.venv/bin/pip install -r requirements.txt --upgrade
  #./.venv/bin/python -Wa manage.py migrate

run: venv
  ./.venv/bin/streamlit run main.py

test: venv
  echo "No Test Yet"
  #./.venv/bin/python -Wa manage.py test

# virtual environment wrapper for manage.py
manage *COMMAND:
  ./.venv/bin/streamlit run main.py $COMMAND

patch_version:
  git describe --tags > $VERSION_FILE