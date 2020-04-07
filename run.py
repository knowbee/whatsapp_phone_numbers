#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
import re
import os
numbers = []
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 600)


def scrape():
    i = 0

    # right_side_component
    groups_people = driver.find_elements_by_xpath(
        '//*[@id="pane-side"]/div[1]/div/div/div')
    for p in groups_people:
        p.click()  # open a chat
        left_side = '//*[@id="main"]/header/div[2]'
        chat = wait.until(
            EC.presence_of_element_located((By.XPATH, left_side)))

        header = p.find_element_by_xpath('//*[@id="main"]/header/div[2]')
        title = header.find_element_by_xpath(
            '//*[@id="main"]/header/div[2]/div[1]/div/span').text  # get username
        header.click()  # click on the header inside chat
        time.sleep(2)
        phone = p.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]').text.split("\n")[-4]
        print(".")
        if ', ' in phone:
            numbers + phone.split(", ")
        numbers.append(phone.replace(" ", ""))
        i += 1
    with open("dirty_contacts.json", "w") as file:
        json.dump(numbers, file)


if __name__ == '__main__':
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)
    x_arg = '//*[@id="pane-side"]/div[1]/div/div/div[1]'
    chats = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    scrape()
    with open("dirty_contacts.json", encoding="utf-8") as file:
        contacts = json.load(file)
        array_of_contacts = []
        unique_contacts = []
        for contact in contacts:
            if len(contact) > 1:
                array_of_contacts = array_of_contacts + contact.split(",")

        for contact in array_of_contacts:
            if contact not in unique_contacts and re.match("\+|[0-9]", str(contact)):
                unique_contacts.append(contact)

        with open("clean_contacts.json", "w") as file:
            json.dump(unique_contacts, file)

os.remove("dirty_contacts.json")
print("done")
driver.quit()
