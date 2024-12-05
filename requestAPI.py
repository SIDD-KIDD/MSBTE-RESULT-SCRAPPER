import requests
from bs4 import BeautifulSoup

# Function to scrape the result
def scrape_result(enrollment_number):
    # URL of the result page
    url = 'https://msbte.org.in/pcwebBTRes/pcResult01/pcfrmViewMSBTEResult.aspx'

    # Form data to be sent in the POST request
    form_data = {
        'txtEnrollment': enrollment_number,
        'btnSubmit': 'Submit'
    }

    # Sending POST request with form data
    response = requests.post(url, data=form_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting the result data from the parsed HTML
        result_data = soup.find('div', class_='content').text.strip()

        return result_data
    else:
        print('Failed to fetch result. Status Code:', response.status_code)
        return None

# Example enrollment number
enrollment_number = '2212270229'

# Scrape the result
result = scrape_result(enrollment_number)

# Print the result
if result:
    print('Result:')
    print(result)
else:
    print('Failed to fetch result.')
