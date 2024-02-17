import os
import re
import streamlit as st

DELIMITER = "\n"
FILENAME_MATCH = "^[a-z0-9-_]+.txt$"
MOUNT_PATH = os.getenv("MOUNT_PATH", ".")
PERSON_MATCH = "^[a-zA-Z\\s]+$"


def validate_input(string: str, pattern: str) -> bool:
    """
    Returns True if string matches pattern.
    """
    return re.compile(pattern).match(string)


def main(person: str, filename: str):
    """
    Validates user input.
    Writes greeting to file.
    Reads greetings from file.
    """
    if not person:
        return st.text("Please enter person to greet.")
    if not validate_input(person, PERSON_MATCH):
        return st.error(f"Person does not match {PERSON_MATCH}", icon="🥲")
    if not validate_input(filename, FILENAME_MATCH):
        return st.error(f"Filename does not match {FILENAME_MATCH}", icon="🥲")

    with open(f"{MOUNT_PATH}/{filename}", "a+") as file:
        file.write(f"Hey {person}!{DELIMITER}")

    with open(f"{MOUNT_PATH}/{filename}", "r") as file:
        content = file.readlines()
        st.text("Contents of file:")
        st.write(DELIMITER.join(content))


st.title("Demo App")

person_input = st.text_input("Person to greet", "")
filename_input = st.text_input("Filename", "demo_file.txt")

main(person_input, filename_input)
