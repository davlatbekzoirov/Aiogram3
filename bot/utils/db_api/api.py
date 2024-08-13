import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000/api/v1"
USERNAME = "davlatbek"
PASSWORD = "1234"

def create_user(name, age, phone_number, role, telegram_id):
    url = f"{BASE_URL}/users/"
    json_data = {
        "name": name,
        "age": age,
        "phone_number": phone_number,
        "role": role.lower(),
        "telegram_id": telegram_id  # Include this if you want to set telegram_id
    }
    
    try:
        response = requests.post(
            url=url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            json=json_data
        )
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        print("User created successfully.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")  # Add this to see the server's error message
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

def create_question(text):
    url = f"{BASE_URL}/applicant-questions/"

    try:
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    # Check if the question already exists
    question_exists = any(question["text"] == text for question in data)

    if not question_exists:
        try:
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"text": text}
            )
            post_response.raise_for_status()
            print("Question created successfully.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
    else:
        print("Question already exists.")

def create_option(question_id, text):
    url = f"{BASE_URL}/applicant-options/"

    try:
        # Fetch existing options to check if the option already exists
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    # Check if the option already exists for the given question
    option_exists = any(
        option["text"] == text and option["question"]["id"] == question_id
        for option in data
    )

    if not option_exists:
        try:
            # Post new option with nested dictionary for question
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"question": {"id": question_id}, "text": text}
            )
            post_response.raise_for_status()
            print("Option created successfully.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            print(f"Response content: {post_response.text}")
    else:
        print("Option already exists for the given question.")

def create_applicant(user_id, option_id):
    payload = {
        'id': user_id,
        'selected_option': option_id
    }
    response = requests.post(f"{BASE_URL}/applicants/", json=payload, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code != 200:
        print(f"Error creating applicant: {response.status_code} - {response.text}")

def create_student(user_id, option_id):
    payload = {
        'id': user_id,
        'selected_option': option_id
    }
    response = requests.post(f"{BASE_URL}/students/", json=payload, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code != 200:
        print(f"Error creating student: {response.status_code} - {response.text}")

def create_question_student(text):
    url = f"{BASE_URL}/student-questions/"

    try:
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    # Check if the question already exists
    question_exists = any(question["text"] == text for question in data)

    if not question_exists:
        try:
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"text": text}
            )
            post_response.raise_for_status()
            print("Question created successfully.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
    else:
        print("Question already exists.")

def create_option_student(question_id, text):
    url = f"{BASE_URL}/student-options/"

    try:
        # Fetch existing options to check if the option already exists
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    # Check if the option already exists for the given question
    option_exists = any(
        option["text"] == text and option["question"]["id"] == question_id
        for option in data
    )

    if not option_exists:
        try:
            # Post new option with nested dictionary for question
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"question": {"id": question_id}, "text": text}
            )
            post_response.raise_for_status()
            print("Option created successfully.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            print(f"Response content: {post_response.text}")
    else:
        print("Option already exists for the given question.")

def fetch_questions(role):
    url = f"{BASE_URL}/students/questions/" if role == "student" else f"{BASE_URL}/applicants/questions/"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching questions: {response.text}")
        return []

def fetch_options(role):
    url = f"{BASE_URL}/students/options/" if role == "student" else f"{BASE_URL}/applicants/options/"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching options: {response.text}")
        return []

def is_telegram_id_registered(telegram_id: int):
    """
    Tests whether a given Telegram ID is registered by making a request to an API endpoint.

    :param telegram_id: Telegram ID to check
    :param api_url: The URL of the API endpoint to check the Telegram ID
    :return: True if the Telegram ID is registered, False otherwise
    """
    try:
        response = requests.get(f"{BASE_URL}/check_telegram_id/", params={"telegram_id": telegram_id})

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data.get("is_registered", False)
        else:
            # Handle unexpected status codes
            print(f"Error: Received unexpected status code {response.status_code}")
            return False
    except requests.RequestException as e:
        # Handle any network-related errors
        print(f"Error: Failed to connect to API - {e}")
        return False

def create_referral_code(reffer_id, user_realy_name, points, flag=False):
    """
    Creates a new referral code via an HTTP POST request to the API endpoint.

    :param reffer_id: The unique ID associated with the referral code.
    :param user_realy_name: The real name of the user associated with the referral code.
    :param points: The number of points associated with the referral code.
    :param flag: A boolean indicating some status (default is False).
    :return: None
    """
    url = f"{BASE_URL}/referral-codes/"
    json_data = {
        "reffer_id": reffer_id,
        "user_realy_name": user_realy_name,
        "points": points,
        "flag": flag
    }
    
    try:
        response = requests.post(
            url=url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            json=json_data
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        print("Referral code created successfully.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

def increase_user_points(reffer_id, additional_points):
    """
    Increases the points of the referral code specified by reffer_id by additional_points.

    :param reffer_id: The unique ID associated with the referral code.
    :param additional_points: The number of points to add to the current points.
    :return: None
    """
    url = f"{BASE_URL}/referral-codes/"
    
    try:
        # Fetch the current referral codes data
        response = requests.get(
            url=url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()

        # Debugging: Print the fetched data
        print("Fetched data:", data)
        
        # Find the referral code with the matching reffer_id
        referral_code = next((item for item in data if item["reffer_id"] == reffer_id), None)

        if referral_code:
            # Calculate the new points
            current_points = referral_code.get("points", 0)
            new_points = current_points + additional_points
            
            # Update the referral code with the new points
            update_response = requests.patch(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"reffer_id": reffer_id, "points": new_points}
            )
            update_response.raise_for_status()  # Raises an HTTPError for bad responses
            print(f"Points updated successfully. New points: {new_points}")
        else:
            print("Referral code not found.")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

def get_user_points(user_id):
    """
    Retrieves the points for a specific user.

    :param user_id: The ID of the user whose points are to be retrieved.
    :return: The points of the user, or None if an error occurred or user does not exist.
    """
    url = f"{BASE_URL}/referral-codes/{user_id}/"
    
    try:
        response = requests.get(
            url=url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        if response.status_code == 404:
            print(f"Referral code with ID {user_id} does not exist.")
            return None
        
        data = response.json()
        return data.get('points', 0)
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return None
