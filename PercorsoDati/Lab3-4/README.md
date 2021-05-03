# Streamlit project example

Streamlit project example.

This is a simple project example with good structure and code organization for dashboard.

The objective of this project is to have a project template for your dashboards.

If you want to see a beautiful cheatsheet with all commands and API for dashboard see:
- https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

If you want to see the full documentation and reference for the streamlit components see:
- https://docs.streamlit.io/en/stable/api.html

Interesting intermediate concepts:
- https://pmbaumgartner.github.io/streamlitopedia/

Pandas Styling documentation 
- https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html

Streamlit global settings configuration docs
- https://docs.streamlit.io/en/stable/streamlit_configuration.html#set-configuration-options



**Features**:
- Dashboard created with: `Streamlit`
- Beautiful plots with `Plotly`
- Automatic documentation with: `Mkdocs`
- Project organization with `Poetry`
- Linter on the project with: `Flake8`
- Test with `pytest`

## Create the project with Poetry

Follow this steps if you want to create the project from zero.  
Warning = in the project there's already a `pyproject.toml` config file so this commands are not required

```bash
#Initialize the project
poetry init
#compile the 

#Add the libraries
poetry add streamlit matplotlib seaborn plotly plotly-express pandas numpy pytest mkdocs mkdocs-macros-plugin mkdocs-material mkdocstrings mkdocs-autorefs mkdocs-simple-plugin mkdocs-jupyter PyYAML SQLAlchemy

#Add the dev libraries
poetry add -D black bandit flak8 flake8-bandit flake8-isort flake8-builtins

#If you want to use the shell with the venv of the project
poetry shell

#Now you can develop your project
```

## Create the environment in the project

It's important to have installed in your default python (on your machine) the library: `poetry`.

If you want to have a good python tool to manage different python versions use: `pyenv`

If you want to see some documentation about poetry and pyenv please check the documentation or our website (in Italian, sorry...) [Python Biella Group Documentation](https://pythonbiellagroup.github.io/ModernPythonDevelopment)

```bash
#Install the libraries
poetry install
```

If you want to launch the project remember to launch the ETL first to download and prepare the data, then launch:
```bash
#Launch the project
streamlit run main.py
```


## ETL

The dashboard is based on a custom ETL program.

The ETL have this functionalities:
- Extract and download the information
- Transform: the data into a usable version by dashboard
- Load: extract the csv saving to disk

We suggest to execute the ETL before launching the dashboard:
```bash

#After the installation do
python etl.py

```


## Launch the code with Docker

If you have Docker and Docker compose installed in your system you can install and launch the dashboard by doing
```bash
#Launch the dockercompose + build in detach mode
docker-compose up --build -d
```
You can visualize the dashboard in the following url: http://localhost:8051


## Launch the Documentation

This project have an automatic documentation system built with `mkdocs`.

To launch the documentation install the dependencies before looking for the previous chapter and then:
```bash
#launch mkdocs in the project
mkdocs serve

```


## Other useful information

How to download a file from streamlit (online forum discussion)
- https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/49
- custom download button: https://gitlab.com/-/snippets/2106399


## Configure VSCode
If you want to configure the VSCode debugger for your project please consider to create inside the `.vscode` folder the file: `launch.json`.
Inside this file insert this configurations to use the debugger with streamlit or to launch a single python file
```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${cwd}"
      }
    },
    {
      "name": "Python: Streamlit",
      "type": "python",
      "request": "launch",
      "module": "streamlit.cli",
      "args": ["run", "${workspaceFolder}/main.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${cwd}"
      }
    },
    {
      "name": "Flask Backend",
      "type": "python",
      "request": "launch",
      "port": 8000,
      "host": "localhost",
      "program": "${workspaceFolder}/server.py",
      "console": "integratedTerminal",
      "env": {
        "API_ENDPOINT_PORT": "8000",
        "VERBOSITY": "debug"
        // "PYTHONPATH": "${cwd}"
      }
    }
  ]
}

```