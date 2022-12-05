import requests
import syslog

# Define the Wazuh API URL and credentials
api_url = "http://localhost:55000"
user = "wazuh"
password = "wazuh"

# Authenticate with the Wazuh API
auth_url = f"{api_url}/auth"
auth_data = {"username": user, "password": password}
auth_response = requests.post(auth_url, json=auth_data)

# Extract the API token from the authentication response
api_token = auth_response.json()["data"]["api_token"]

# Use the API token to restart the Wazuh manager
restart_url = f"{api_url}/manager/restart"
restart_headers = {"Authorization": f"Bearer {api_token}"}
restart_response = requests.post(restart_url, headers=restart_headers)

# Check the response from the restart request
if restart_response.status_code == 200:
    # Log success message to system log
    syslog.syslog(syslog.LOG_INFO, "Wazuh manager restarted successfully")
else:
    # Log error message to system log
    syslog.syslog(syslog.LOG_ERR, "Error restarting Wazuh manager")
