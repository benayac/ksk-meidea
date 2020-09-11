from helper import *
from database import Database
from google_api import GoogleApi
from secrets import *
import time

google_api = GoogleApi()
database = Database()

email_sent_cell = 'G'
email_index = 3
name_index = 1
sleep_time = 300

while True:
    try:
        sheet_value = google_api.read_sheet(SPREADSHEET_ID, RANGE)
        for idx, value in enumerate(sheet_value):
            email = value[email_index]
            name = value[name_index]
            if(database.is_data_available({'email':email}) is not True):
                print(f"Sending Email To: {email} index: {idx+2}")

                msg = google_api.create_message(my_email, email, msg_title, message.format(name))
                google_api.send_message("me", msg)
                google_api.update_cell(SPREADSHEET_ID, f'{email_sent_cell}{idx+2}', 'EMAIL SENT')

                database.insert_data({'email':email})
            else:
                print(f"Email have been sent to {email}")
            time.sleep(1)
        sleep(sleep_time)
    except Exception as e:
        print(e)
        sleep(sleep_time)
        continue