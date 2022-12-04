
#ChatGPT Input: 
#Write a pyton script that fetches alerts from a wazuh manager and lookup for scr ip in abuseip db  if it is reported more than 20 times then create a acl in aws security group 


import requests
import json

# Replace with the URL of your Wazuh manager
wazuh_url = 'http://wazuh-manager:55000/api/v2/alerts'

# Replace with your AbuseIPDB API key
abuseipdb_key = 'your-api-key'

# Set the maximum number of reports for an IP to trigger the ACL creation
max_reports = 20

# AWS security group ID to add the ACL to
security_group_id = 'sg-12345678'

# Wazuh API credentials
wazuh_user = 'foo'
wazuh_password = 'bar'

# Fetch alerts from Wazuh
response = requests.get(wazuh_url, auth=(wazuh_user, wazuh_password))

if response.status_code != 200:
  print('Error fetching alerts from Wazuh:', response.text)
  exit(1)

# Parse the JSON response
alerts = json.loads(response.text)

# Create a set to store unique IPs
ips = set()

# Loop through the alerts and extract the source IPs
for alert in alerts:
  if 'srcip' in alert:
    ips.add(alert['srcip'])

# Loop through the unique IPs and check their reports in AbuseIPDB
for ip in ips:
  # Build the AbuseIPDB API URL
  url = f'https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=365&verbose'

  # Make the API request
  response = requests.get(url, headers={'Key': abuseipdb_key, 'Accept': 'application/json'})

  if response.status_code != 200:
    print('Error checking IP reports in AbuseIPDB:', response.text)
    continue

  # Parse the JSON response
  result = json.loads(response.text)

  # Check if the IP has more than the maximum number of reports
  if result['data']['totalReports'] > max_reports:
    print(f'IP {ip} has {result["data"]["totalReports"]} reports in AbuseIPDB')
    # Add the IP to the AWS security group ACL
    # Replace with your own code to add the IP to the security group
    print(f'Adding IP {ip} to security group {security_group_id}')
