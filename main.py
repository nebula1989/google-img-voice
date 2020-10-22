# libraries
import time
import speech_recognition as sr

# selenium packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

# selenium exceptions
from selenium.common.exceptions import \
    StaleElementReferenceException, \
    NoSuchElementException, \
    TimeoutException, \
    ElementClickInterceptedException


# Global variables
WAIT_SECONDS = 15

# browswer config
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


def main():
    query = get_mic_input()
    goog_img_srch(query)


def get_mic_input():
    """
    gets voice input as string
    :return: audio_data
    """
    # audio engine components
    r = sr.Recognizer()

    mic = sr.Microphone()

    with mic as source:
        is_audio = False
        while not is_audio:
            try:
                print("Say something...")
                r.adjust_for_ambient_noise(source)
                audio_data = r.listen(source)
                text_speech = r.recognize_google(audio_data)
                is_audio = True
            except Exception:
                no_audio_input_alert()
                is_audio = False

        return text_speech


def goog_img_srch(query):
    """
    takes users speech text and google image searches and clicks first image
    :param query:
    :return: none
    """
    # selenium firefox browser object
    browser = webdriver.Chrome()
    browser.maximize_window()

    # open chrome window of google images
    browser.get("https://www.google.com/imghp?hl=EN")

    # identify query bar and  go button
    search_bar = WebDriverWait(browser, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.XPATH, '//input[@title="Search"]'))
    )

    go_btn = WebDriverWait(browser, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))
    )

    # init search bar text
    search_bar.clear()
    # input users' voice query into google search bar
    search_bar.send_keys(query)

    # click go button
    go_btn.click()

    # identify first image
    first_img = WebDriverWait(browser, WAIT_SECONDS).until(
        EC.presence_of_element_located((By.XPATH, '//img[@class="rg_i Q4LuWd"]'))
    )

    first_img.click()

    print("Ran all selenium stuff")
    time.sleep(WAIT_SECONDS)


def no_audio_input_alert():
    print("No audio input detected. Try again")


if __name__ == '__main__':
    main()
