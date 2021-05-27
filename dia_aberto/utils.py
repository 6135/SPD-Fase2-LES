from selenium import webdriver
import os

browser = "chrome"
use_custom_driver = False

drivers = {
    "firefox": {
        "version": ">= 60",
        "name": "geckodriver",
        "driver": webdriver.Firefox,
    },
    "edge": {
        "version": "85.0.558.0",
        "name": "msedgedriver",
        "driver": webdriver.Edge,
    },
    "chrome": {
        "version": "83.0.4103.39",
        "name": "chromedriver",
        "driver": webdriver.Chrome,
    },
    "safari": {
        "driver": webdriver.Safari,
    },
    "opera": {
        "version": "83.0.4103.97",
        "name": "operadriver",
        "driver": webdriver.Opera,
    },
}


def init_driver(_browser, _use_custom_driver=False):
    global browser
    browser = _browser
    use_custom_driver = _use_custom_driver


def get_driver():
    if use_custom_driver or browser == "safari":
        driver = drivers[browser]["driver"]()
    else:
        driver_path = f"webdrivers/{drivers[browser]['name']}"
        if os.name == "nt":
            driver_path += ".exe"
        driver = drivers[browser]["driver"](executable_path=driver_path)
    return driver
