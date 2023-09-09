from google.oauth2 import service_account
from googleapiclient.discovery import build

from data.config import FILE_PATH


class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=FILE_PATH, scopes=self.SCOPES
        )

        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return (self.service.calendarList().list().execute())['items']

    def add_calendar(self, calendar_id):
        try:
            calendar_list_entry = {
                'id': calendar_id
            }
            self.service.calendarList().insert(body=calendar_list_entry).execute()
            return True
        except:
            return False

    def add_event(self, calendar_id, event):
        try:
            self.service.events().insert(calendarId=calendar_id, body=event).execute()
            return True
        except:
            return False
