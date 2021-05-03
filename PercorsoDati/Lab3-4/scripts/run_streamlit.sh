
#!/bin/bash
# The ping job will help keep awesome-streamlit.org alive.
# See https://lnx.azurewebsites.net/python-app-on-azure-web-apps-frequently-restarts/
echo "launching streamlit dashboard" &
streamlit run main.py