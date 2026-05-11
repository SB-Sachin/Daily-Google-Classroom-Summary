import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me.readonly"
]

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                print("Error: credentials.json not found. Please follow the instructions in README.md to provide it.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_report():
    creds = get_credentials()
    if not creds:
        return "Authentication failed."

    try:
        service = build("classroom", "v1", credentials=creds)

        # Use local timezone for "today"
        local_now = datetime.datetime.now()
        today = local_now.date()
        
        # Get courses
        results = service.courses().list(courseStates="ACTIVE").execute()
        courses = results.get("courses", [])

        if not courses:
            return "No active courses found."

        report = f"Classroom Report for {datetime.date.today()}\n"
        report += "="*30 + "\n"

        for course in courses:
            course_id = course["id"]
            course_name = course["name"]
            report += f"\nCourse: {course_name}\n"
            report += "-"*len(f"Course: {course_name}") + "\n"

            # Fetch announcements
            announcements_res = service.courses().announcements().list(courseId=course_id).execute()
            announcements = announcements_res.get("announcements", [])
            
            today_announcements = []
            for ann in announcements:
                creation_time = datetime.datetime.fromisoformat(ann["creationTime"].replace("Z", "+00:00")).date()
                if creation_time == today:
                    today_announcements.append(ann.get("text", "No text"))

            if today_announcements:
                report += "  What we did today (Announcements):\n"
                for text in today_announcements:
                    report += f"    - {text}\n"
            else:
                report += "  No announcements today.\n"

            # Fetch coursework
            coursework_res = service.courses().courseWork().list(courseId=course_id).execute()
            courseworks = coursework_res.get("courseWork", [])

            today_coursework = []
            upcoming_homework = []

            for cw in courseworks:
                creation_time = datetime.datetime.fromisoformat(cw["creationTime"].replace("Z", "+00:00")).date()
                if creation_time == today:
                    today_coursework.append(cw["title"])
                
                due_date = cw.get("dueDate")
                if due_date:
                    due_dt = datetime.date(year=due_date["year"], month=due_date["month"], day=due_date["day"])
                    if due_dt >= today:
                        upcoming_homework.append(f"{cw['title']} (Due: {due_dt})")

            if today_coursework:
                report += "  New coursework today:\n"
                for title in today_coursework:
                    report += f"    - {title}\n"
            
            if upcoming_homework:
                report += "  Upcoming homework:\n"
                for hw in upcoming_homework:
                    report += f"    - {hw}\n"
            else:
                report += "  No upcoming homework.\n"

        return report

    except HttpError as error:
        return f"An error occurred: {error}"

if __name__ == "__main__":
    print(get_report())
