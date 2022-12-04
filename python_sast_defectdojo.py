import os
import requests

# Set GitLab API URL
gitlab_api_url = 'https://gitlab.com/api/v4'

# Set GitLab project ID
project_id = 123456

# Set DefectDojo API URL
dojo_api_url = 'https://defectdojo.com/api/v1'

# Set DefectDojo API key
dojo_api_key = '1234567890abcdefghijklmnopqrstuvwxyz'

# Set SAST SCA scanner
scanner = 'bandit'

# Set SAST SCA scanner options
scanner_options = {
    'recursive': True
}

# Set SAST SCA scanner output format
scanner_output_format = 'json'

# Set SAST SCA scanner output file
scanner_output_file = 'output.json'

# Set SAST SCA scanner command
scanner_command = f'{scanner} -r -f {scanner_output_format} . > {scanner_output_file}'

# Set GitLab API token
gitlab_api_token = os.environ['GITLAB_API_TOKEN']

# Set GitLab API headers
gitlab_api_headers = {
    'Private
# Clone GitLab project
os.system(f'git clone https://oauth2:{gitlab_api_token}@gitlab.com/{project_id}.git')

# Change working directory
os.chdir(str(project_id))

# Scan GitLab project with SAST SCA scanner
os.system(scanner_command)

# Read SAST SCA scanner output
with open(scanner_output_file, 'r') as f:
    scanner_output = f.read()

# Parse SAST SCA scanner output
scanner_output_json = json.loads(scanner_output)

# Initialize list of findings
findings = []

# Iterate over scanner findings
for finding in scanner_output_json:
    # Initialize finding
    finding = {
        'title': finding['test_name'],
        'date': finding['date'],
        'severity': finding['issue_severity'],
        'description': finding['issue_text'],
        'mitigation': finding['issue_confidence'],
        'impact': finding['issue_severity'],
        'references': finding['more_info'],
        'file_path': finding['filename'],
        'line_number': finding['line_number']
    }

    # Add finding to list of findings
    findings.append(finding)

# Set DefectDojo API headers
dojo_api_headers = {
    'Authorization': f'Token {dojo_api_key}',
    'Content-Type': 'application/json'
}

# Set DefectDojo product
product = {
    'name': 'Sample GitLab Project',
    'description': 'This is a sample GitLab project that has been scanned with a SAST SCA scanner.'
}

# Create DefectDojo product
product_response = requests.post(f'{dojo_api_url}/products/', headers=dojo_api_headers, json=product)

# Parse DefectDojo product
product = product_response.json()

# Set DefectDojo engagement
engagement = {
    'product': product['id'],
    'name': 'Sample GitLab Project Scan',
    'status': 'In Progress',
    'target_start': datetime.utcnow().isoformat(),
    'target_end': (datetime.utcnow() + timedelta(days=7)).isoformat()
}

# Create DefectDojo engagement
engagement_response = requests.post(f'{dojo_api_url}/engagements/', headers=dojo_api_headers, json=engagement)

#
# Parse DefectDojo engagement
engagement = engagement_response.json()

# Set DefectDojo test
test = {
    'engagement': engagement['id'],
    'test_type': 1,
    'environment': 'Development',
    'target_start': datetime.utcnow().isoformat(),
    'target_end': (datetime.utcnow() + timedelta(days=7)).isoformat()
}

# Create DefectDojo test
test_response = requests.post(f'{dojo_api_url}/tests/', headers=dojo_api_headers, json=test)

# Parse DefectDojo test
test = test_response.json()

# Set DefectDojo finding
finding = {
    'test': test['id'],
    'title': finding['test_name'],
    'date': finding['date'],
    'severity': finding['issue_severity'],
    'description': finding['issue_text'],
    'mitigation': finding['issue_confidence'],
    'impact': finding['issue_severity'],
    'references': finding['more_info'],
    'file_path': finding['filename'],
    'line_number': finding['line_number']
}

# Create DefectDojo finding
finding_response = requests.post(f'{dojo_api_url}/findings/', headers=dojo_api_headers, json=finding)

# Parse DefectDojo finding
finding = finding_response.json()

# Print DefectDojo finding
print(finding)
