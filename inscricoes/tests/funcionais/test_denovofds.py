# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestDenovofds():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_denovofds(self):
    self.driver.get("http://127.0.0.1:8000/")
    self.driver.set_window_size(1918, 1027)
    self.driver.find_element(By.LINK_TEXT, "Minhas Inscrições").click()
    self.driver.find_element(By.NAME, "areacientifica").click()
    self.driver.find_element(By.NAME, "areacientifica").send_keys("Ciencias")
    self.driver.find_element(By.CSS_SELECTOR, ".is-primary > span:nth-child(2)").click()
    self.driver.find_element(By.CSS_SELECTOR, ".is-light").click()
    self.driver.find_element(By.CSS_SELECTOR, ".is-expanded > .is-primary").click()
    self.driver.find_element(By.CSS_SELECTOR, ".even > td:nth-child(2)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".even > td:nth-child(2)").text == "1"
    assert self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text == "Escola Básica e Secundária do Cadaval - Cadaval"
    assert self.driver.find_element(By.CSS_SELECTOR, "tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)").text == "Rafael Duarte"
  
