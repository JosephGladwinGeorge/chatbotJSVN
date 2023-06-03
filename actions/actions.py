# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector
from mysql.connector import Error
print("started")

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        student_id = tracker.sender_id
        print(student_id)

        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='avengers007',
                database='studentdata'
            )

            # Execute your SQL query using the conversation_id
            query = f"SELECT mark FROM result WHERE student_id = '{student_id}'"
            cursor = connection.cursor()
            cursor.execute(query)

            # Fetch the results
            results = cursor.fetchall()

            # Perform any necessary actions with the query results
            print(results)
            dispatcher.utter_message("mark = ",results)
            # Close the cursor and database connection
            cursor.close()
            connection.close()

        except Error as e:
            # Handle any errors that occur during the database connection or query execution
            print(f"Error connecting to MySQL: {e}")

        return []

class ActionCgpa(Action):
    def name(self) -> Text:
        return "action_cgpa"
    
    def run(self, dispatcher:CollectingDispatcher, tracker: Tracker):
        student_id = tracker.sender_id
        print(student_id)

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='avengers007',
                database='studentdata'
            )
            query = f"SELECT year_1_cgpa FROM result WHERE user_id = '{student_id}'"
            cursor = connection.cursor()
            cursor.execute(query)

            results = cursor.fetchall()

            # Perform any necessary actions with the query results
            print(results)
            print(int(results))
            dispatcher.utter_message("your cgpa is ",results)
            cursor.close()
            connection.close()

        except Error as e:
            # Handle any errors that occur during the database connection or query execution
            print(f"Error connecting to MySQL: {e}")

        return []
