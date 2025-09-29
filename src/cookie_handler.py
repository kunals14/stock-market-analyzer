"""
Manages the creation, validation, and storage of browser session cookies.

This module helps maintain a logged-in state across multiple runs of the scraper,
reducing the need for manual logins and making the process more robust.
"""

import os
import pickle
import time
import random

import undetected_chromedriver as uc

def are_cookies_valid(file_path, max_age_days=7):
    """
    Checks if the cookie file exists and is not older than a specified maximum age.

    Args:
        file_path (str): The path to the cookie file.
        max_age_days (int): The maximum age of the cookie file in days.

    Returns:
        bool: True if the file exists and is recent, False otherwise.
    """
    # 1. Check if the file exists
    if not os.path.exists(file_path):
        print("Cookie file not found.")
        return False

    # 2. Check the age of the file
    file_mod_time = os.path.getmtime(file_path)
    age_in_seconds = time.time() - file_mod_time
    max_age_in_seconds = max_age_days * 24 * 60 * 60

    if age_in_seconds > max_age_in_seconds:
        print(f"Cookie file is older than {max_age_days} days, a new login is required.")
        return False

    print("Found recent cookie file.")
    return True


def generate_new_cookies(file_path):
    """
    Launches an interactive browser session for the user to log in manually.

    Once the user logs in and confirms by pressing Enter, the session cookies
    are saved to a file for future use. This is a creative way to handle
    authentication without hardcoding credentials and helps with anti-bot measures.

    Args:
        file_path (str): The path where the cookie file will be saved.
    """
    # Using undetected_chromedriver to avoid bot detection during login
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    try:
        # "Warm up" the browser by visiting a neutral site first.
        # This makes the subsequent navigation to Twitter/X look more natural.
        print("Warming up the browser...")
        driver.get("https://www.google.com/")
        time.sleep(random.uniform(1, 3))

        # Navigate to the main homepage, not the specific login page.
        print("Navigating to Twitter/X homepage...")
        driver.get("https://twitter.com")

        # Prompt the user to complete the login process manually
        print("\n" + "="*50)
        print("ACTION REQUIRED: PLEASE LOG IN")
        print("Please click 'Log in' or 'Sign in' in the browser window and log in.")
        print("Once you are successfully logged in, press 'Enter' in this terminal.")
        print("="*50 + "\n")

        input("Press Enter to continue after logging in...")

        # Retrieve all cookies from the now-authenticated session
        cookies = driver.get_cookies()

        with open(file_path, "wb") as file:
            pickle.dump(cookies, file)

        print(f"\nSUCCESS: Cookies have been saved to '{file_path}'!")

    finally:
        time.sleep(2)
        driver.quit()