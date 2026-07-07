# Scrapper to access autius login, then calendar, then tracking, then infinite loop

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from discordwebhook import Discord
import emoji
import requests
import json
from unidecode import unidecode
import time

import config

class DiscordWebHook:

    def __init__(self, url) -> None:

        self.url = url
        self.discord = Discord(url=self.url)

    def send_message(self, msg, emojize=True, addSeparatorMsg=True):

        # Drawing emojis if requested
        if emojize:
            msg = emoji.emojize(msg)

        # Sending (posting) message to webhook
        self.discord.post(content=msg)
        # Adding separator message if requested
        if addSeparatorMsg:
            self.discord.post(content="_ _")


class AutiusTracker:
    def __init__(self, username, password, chromedriver_path=None, chromiumbrowser_path=None, headless=False, loginInit=True):

        # Tipster credentials
        self.username = username
        self.password = password

        ############### DRIVER INSTANTIATION
        uc.TARGET_VERSION = 126
        # options = uc.ChromeOptions()
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-xss-auditor')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-client-side-phishing-detection')
        options.add_argument('--no-sandbox')
        options.headless = headless

        # Set actual binary and chromedriver path
        options.binary_location = chromiumbrowser_path or config.CHROMIUM_BINARY_PATH
        chromedriver_path = chromedriver_path or config.CHROMEDRIVER_PATH

        # Pass driver path directly to uc.Chrome
        # self.driver = uc.Chrome(driver_executable_path=chromedriver_path, options=options)

        # Optional: store paths in self
        self.chromedriver_path = chromedriver_path
        self.chromiumbrowser_path = options.binary_location

        try:
            if self.chromiumbrowser_path is not None and self.chromedriver_path is not None:
                print(f"[INFO] AUTIUS tracker initialized with custom paths {self.chromiumbrowser_path}\n{self.chromedriver_path}")
                # Attempt to create a Chrome instance with specified options
                # self.driver = uc.Chrome(browser_executable_path=self.chromiumbrowser_path, driver_executable_path=self.chromedriver_path, options=options, use_subprocess=True)
                self.driver = uc.Chrome(driver_executable_path=self.chromedriver_path, options=options, use_subprocess=True)
            else:
                print(f"[INFO] AUTIUS tracker initialized with defaults")
                self.driver = uc.Chrome(options=options, use_subprocess=True)

        except Exception as e:
            # Handle exception and print more informative details
            print("An error occurred while initializing the browser:")
            print(f"Exception Type: {type(e).__name__}")
            print(f"Exception Details: {str(e)}")

        self.loginInit = loginInit

        ############### DRIVER LOGIN
        if self.loginInit:
            self.login(email=self.username, password=self.password)

    def login(self, email, password):
        self.driver.get('https://gestion.autius.com/')
        time.sleep(5)
        try:
            # Locate and interact with the username input field
            uname = self.driver.find_element(By.XPATH, "//input[@placeholder='Usuario']")
            uname.send_keys(email)

            # Locate and interact with the password input field
            pword = self.driver.find_element(By.XPATH, "//input[@placeholder='*********']")
            pword.send_keys(password)

            # Locate and click the login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            time.sleep(5)
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")

    def set_availability_type(self, type: str = 'Todas'):
        try:
            # Locate the dropdown element with role="button" and default value "Todas"
            dropdown = self.driver.find_element(By.XPATH, "//div[@role='button' and text()='Libres']")
            dropdown.click()
            time.sleep(1)  # Wait for the dropdown options to appear

            # Select the desired option based on the provided type
            option = self.driver.find_element(By.XPATH, f"//li[text()='{type}']")
            option.click()
        except Exception as e:
            print(f"[ERROR] Failed to set availability type: {e}")

    def book_lesson(self):
        try:
            # Locate the "Confirmar Clase" button
            confirm_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Confirmar Clase')]")
            confirm_button.click()
            print("[INFO] 'Confirmar Clase' button clicked successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to click 'Confirmar Clase' button: {e}")


    def locate_next_week_arrow(self, num_weeks=5):
        '''try:
            # Locate the button arrow to jump to the next week
            next_week_arrow = self.driver.find_element(By.XPATH, "//div[contains(@class, 'MuiGrid-root') and contains(@style, 'margin-right: 20px;')]//svg[contains(@class, 'MuiSvgIcon-root') and @aria-hidden='true']")
            next_week_arrow.click()
            print("[INFO] Next week arrow clicked successfully.")
            return next_week_arrow
        except Exception as e:
            print(f"[ERROR] Failed to locate or click next week arrow: {e}")
            return None'''

        # Find all SVG arrow buttons by class
        arrow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "svg.MuiSvgIcon-root")
        # print(arrow_buttons, "arrows", len(arrow_buttons), "arrows")

        # Click the left arrow (first one)
        #arrow_buttons[0].click()
        time.sleep(1)  # Optional: wait to see the change

        for i in range(num_weeks):
            # Make sure there are at least 12 elements
            if len(arrow_buttons) > 11:
                arrow_buttons[11].click()
                # print("Clicked element at index 11.")
            else:
                print(f"Only found {len(arrow_buttons)} elements. Index 11 not available.")
            # time.sleep(2)

        # Click the right arrow (second one)
        #arrow_buttons[1].click()

    def locate_prev_week_arrow(self, num_weeks=5):
        '''try:
            # Locate the button arrow to jump to the next week
            next_week_arrow = self.driver.find_element(By.XPATH, "//div[contains(@class, 'MuiGrid-root') and contains(@style, 'margin-right: 20px;')]//svg[contains(@class, 'MuiSvgIcon-root') and @aria-hidden='true']")
            next_week_arrow.click()
            print("[INFO] Next week arrow clicked successfully.")
            return next_week_arrow
        except Exception as e:
            print(f"[ERROR] Failed to locate or click next week arrow: {e}")
            return None'''

        # Find all SVG arrow buttons by class
        arrow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "svg.MuiSvgIcon-root")
        # print(arrow_buttons, "arrows", len(arrow_buttons), "arrows")

        # Click the left arrow (first one)
        #arrow_buttons[0].click()
        time.sleep(1)  # Optional: wait to see the change

        for i in range(num_weeks):
            # Make sure there are at least 12 elements
            if len(arrow_buttons) > 11:
                arrow_buttons[10].click()
                # print("Clicked element at index 11.")
            else:
                print(f"Only found {len(arrow_buttons)} elements. Index 10 not available.")
            time.sleep(2)

        # Click the right arrow (second one)
        #arrow_buttons[1].click()

    def get_weekly_schedule(self, date: str, num_weeks=5):

        informer_bot        = DiscordWebHook(url=config.AUTIUS_DISCORD_WEBHOOK_URL)
        num_weeks_to_check = num_weeks

        for i in range(num_weeks_to_check):
            try:
                # Locate the container with class "rbc-events-container"
                events_containers = self.driver.find_elements(By.CLASS_NAME, "rbc-events-container")
                # print(len(events_containers), "available days")
                # Locate the label date and print it
                label_date = unidecode(self.driver.find_element(By.CLASS_NAME, "label-date").text)
                print(f"[INFO] Label Date: {label_date}")
                # print(len(event_divs), "booking slots")
                lessons_available, num_lessons = False, 0

                for events_container in events_containers:
                    # Find all div elements with class "rbc-event" and role "button" inside each container
                    event_divs = events_container.find_elements(By.XPATH, ".//div[contains(@class, 'rbc-event') and @role='button']")
                    # Iterate through each div and check the background-color attribute
                    for event_div in event_divs:
                        background_color = event_div.value_of_css_property("background-color")
                        # print(f"[INFO] Background color: {background_color}")
                        # Check if the background-color matches the specified RGB values
                        # if "rgba(173, 32, 28, 1)" in background_color:  # Ocupada: RED "rgba(173, 32, 28, 1)"
                        #     lessons_available = True
                        #     num_lessons += 1
                        #     # print("[INFO] Event with background-color rgb(173, 32, 28) found.")
                        #     #informer_bot.send_message(msg="IMPORTANTE: Todo ocupado :(", addSeparatorMsg=False)
                        if "rgba(0, 128, 0, 1)"  in background_color:  # Mi clase: YELLOW "rgba(207, 179, 55, 1)" GREEN "rgba(0, 128, 0, 1)"
                            # print("[INFO] Event with background-color rgb(207, 179, 55) found.")
                            lessons_available = True
                            num_lessons += 1
                            # self.send_discord_message("Available lessons to book!")
                    # print(num_lessons, lessons_available)
                    # print("Sending Discord notification...")
                if lessons_available:
                    informer_bot.send_message(msg=f"IMPORTANTE: Hay {num_lessons} clase(s) abiertas para reservar en la semana {label_date} !", addSeparatorMsg=False)
                    # else:
                    #     informer_bot.send_message(msg="IMPORTANTE: Todo ocupado :(", addSeparatorMsg=False)

                if i != num_weeks_to_check-1:
                    self.locate_next_week_arrow(num_weeks=1)

            except Exception as e:
                print(f"[ERROR] Failed to get weekly schedule: {e}")

        self.locate_prev_week_arrow(num_weeks=num_weeks_to_check-1)

    # def send_discord_message(self, message: str):
    #     webhook_url = "YOUR_DISCORD_WEBHOOK_URL"  # Replace with your Discord webhook URL
    #     data = {"content": message}
    #     try:
    #         response = requests.post(webhook_url, json=data)
    #         if response.status_code == 204:
    #             print("[INFO] Discord message sent successfully.")
    #         else:
    #             print(f"[ERROR] Failed to send Discord message. Status code: {response.status_code}")
    #     except Exception as e:
    #         print(f"[ERROR] Exception occurred while sending Discord message: {e}")

    def auto_tracker(self):

        # Login if it was not done in initialization process
        if not self.loginInit:
            self.login(email=self.username, password=self.password)


    def close_browser(self, wait_time=60):
        time.sleep(wait_time)
        self.driver.quit()



# Example usage of the class:
if __name__=="__main__":

    # Tipster configuration & credentials
    headless    = True # Set to False takes 25,52 seconds to run, in True takes around 1s less
    username    = config.AUTIUS_USERNAME
    password    = config.AUTIUS_PASSWORD
    num_weeks  = 5 # Number of weeks to check for available lessons

    # Tipster execution
    tipster = AutiusTracker(username=username, password=password, headless=headless)

    while True:
        try:
            start_time = time.time()  # Start measuring time
            tipster.driver.refresh()
            time.sleep(5)
            tipster.set_availability_type(type="Todas")
            time.sleep(3)
            tipster.get_weekly_schedule(date="2023-10-16", num_weeks=num_weeks)
            # time.sleep(3)  # Wait for 1 minute before running again
            end_time = time.time()  # End measuring time
            exec_time = end_time - start_time
            print(f"[INFO] Iteration execution time: {exec_time:.2f} seconds")
            time.sleep(10)  # Wait for 1 minute before running again
        except Exception as e:
            informer_bot = DiscordWebHook(url=config.AUTIUS_DISCORD_WEBHOOK_URL)
            error_message = f"[ERROR] Process error in current run, please check: {e}"
            print(error_message)
            informer_bot.send_message(msg=error_message, addSeparatorMsg=False)
