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
try:
    connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='avengers007',
                    database='studentdata'
                )
except Error as e:
            # Handle any errors that occur during the database connection or query execution
            print(f"Error connecting to MySQL: {e}")

# class ActionSessionStart(Action):
#     def name(self) -> Text:
#         return "action_session_start"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         student_id = tracker.sender_id
#         print(student_id)

#         try:
#             # Connect to the MySQL database
#             # connection = mysql.connector.connect(
#             #     host='localhost',
#             #     user='root',
#             #     password='avengers007',
#             #     database='studentdata'
#             # )

#             # # Execute your SQL query using the conversation_id
#             # query = f"SELECT mark FROM result WHERE student_id = '{student_id}'"
#             # cursor = connection.cursor()
#             # cursor.execute(query)

#             # # Fetch the results
#             # results = cursor.fetchall()

#             # # Perform any necessary actions with the query results
#             # print(results)
#             # dispatcher.utter_message("mark = ",results)
#             # # Close the cursor and database connection
#             # cursor.close()
#             # connection.close()

#         except Error as e:
#             # Handle any errors that occur during the database connection or query execution
#             print(f"Error connecting to MySQL: {e}")

#         return []

class ActionCgpa(Action):
    def name(self) -> Text:
        return "action_cgpa"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        student_id = tracker.sender_id
        print(student_id)

        try:
            # connection = mysql.connector.connect(
            #     host='localhost',
            #     user='root',
            #     password='avengers007',
            #     database='studentdata'
            # )
            query = f"SELECT year_1_cgpa FROM main_table WHERE user_id = '{student_id}'"
            cursor = connection.cursor()
            cursor.execute(query)

            results = cursor.fetchall()

            # Perform any necessary actions with the query results
            print(results)
            mark=float((results[0])[0])
            ans = f"your cgpa is {mark}"
            dispatcher.utter_message(ans)
            cursor.close()

        except Error as e:
            # Handle any errors that occur during the database connection or query execution
            print(f"Error parsing database: {e}")
            dispatcher.utter_message("Error parsing database")

        return []
    
class ActionCgpaYear(Action):
    def name(self) -> Text:
        return "action_cgpa_year"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        student_id = tracker.sender_id
        year = tracker.get_slot('year')
        try:
            query = f"SELECT year_{year}_cgpa FROM main_table WHERE user_id = '{student_id}'"
            cursor = connection.cursor()
            cursor.execute(query)

            results = cursor.fetchall()
            
            print(results)

            mark=float((results[0])[0])
            ans = f"your cgpa is {mark}"
            dispatcher.utter_message(ans)
            cursor.close()

        except Error as e:
            print(f"Error parsing database: {e}")
            dispatcher.utter_message("Error parsing database")

class ActionSemTotal(Action):
    def name(self) -> Text:
        return "action_sem_total"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        student_id = tracker.sender_id
        sem = tracker.get_slot('sem')
        series = tracker.get_slot('series')
        try:
            query = f"select subject,series_{series} from semester_{sem} where user_id = '{student_id}'"
            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()

            table = "| Subject | Mark |\n"
            table += "|----------|----------|\n"

            for row in rows:
                table += "| {} | {} |\n".format(row[0], row[1])
            
            print(table)

            msg = f"Here is your Semester_{sem} Series_{series} results:\n {table}"
            dispatcher.utter_message(msg)
            cursor.close()

        except Error as e:
            print(f"Error parsing database: {e}")
            dispatcher.utter_message("Error parsing database")

class ActionSubMark(Action):
    def name(self) -> Text:
        return "action_sub_mark"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        sub = tracker.get_slot('sub')
        user_id = tracker.sender_id
        try:
            q = f"SELECT subject_sem from semester_subject where subject_code='{sub}'"
            cursor = connection.cursor()
            cursor.execute(q)

            sem = cursor.fetchall()
            print(sem[0][0])

            query = f"SELECT series_1,series_2 FROM {sem[0][0]} where subject='{sub}' AND user_id='{user_id}'"
            cursor.execute(query)

            mark = cursor.fetchall()

            table = "| Series 1 | Series 2 |\n"
            table += "|----------|----------|\n"

            for row in mark:
                table += "|    {}    |    {}    |\n".format(row[0], row[1])
                    
            print(table)
            msg = f"Here is your {sub} results:\n {table}"
            dispatcher.utter_message(msg)
            cursor.close()
        except:
            print(f"Error parsing database: {e}")
            dispatcher.utter_message("Error parsing database")

class ActionSubMarkSeries(Action):
    def name(self) -> Text:
        return "action_sub_mark_series"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        sub = tracker.get_slot('sub')
        user_id = tracker.sender_id
        series = tracker.get_slot('series')
        try:
            q = f"SELECT subject_sem from semester_subject where subject_code='{sub}'"
            cursor = connection.cursor()
            cursor.execute(q)

            sem = cursor.fetchall()
            print(sem[0][0])

            query = f"SELECT series_{series} FROM {sem[0][0]} where subject='{sub}' AND user_id='{user_id}'"
            cursor.execute(query)

            mark = cursor.fetchall()
                    
            msg = f"{mark[0][0]}"
            dispatcher.utter_message(msg)
            cursor.close()
        except:
            print(f"Error parsing database: {e}")
            dispatcher.utter_message("Error parsing database")

class FallbackAction(Action):
    def name(self) -> Text:
        return "fallback_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Handle case when no entity is recognized
        # Perform any desired actions, prompts, or fallback behavior
        # For example, you could ask the user to rephrase or provide more information
        dispatcher.utter_message("Unrecognized entity")

        return []

        
