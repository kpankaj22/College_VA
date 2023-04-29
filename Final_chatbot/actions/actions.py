from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import ActiveLoop, SlotSet
from rasa_sdk.events import FollowupAction
from datetime import datetime
import mysql.connector
import random

class all_func:
    def create_conn(self):
        try:
            db = mysql.connector.connect(
                host="localhost", user="root", password="", database="clg_va"
            )
            print("connected")
        except:
            print("not connected")
            return 0

        return db

    def datetimenow(self): #datetimenow
        dt= datetime.now()
        #print(dt)
        return dt

    def today_day(self): #datetimeweekday
        dt= all_func.datetimenow(self)
        wd=dt.isoweekday()
        return wd

    def current_time(self): #datetimetime
        tm = all_func.datetimenow(self).hour
        #print(tm)
        return tm

    def text_to_int(self,day):
        weekday={"monday":1,"tuesday":2,"wednesday":3,"thursday":4,"friday":5,"saturday":6,"sunday":7}
        return weekday[day]
    
    def int_to_text(self,day):
        weekday=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        return weekday[day-1]
        


    def query_tt(self, branch, sem, division,time,day,prof_name,subject):

        tt_time=time
        tt_prof_name=prof_name
        tt_subject=subject
        tt_day=day
        #print(type(tt_day))
        
        if tt_time == None:
            tt_time=all_func.current_time(self)
            print("current_time",tt_time)
        if tt_day is None:
            tt_day=all_func.today_day(self)
            print(tt_day)
        if type(tt_day)==str:
            tt_day= all_func.text_to_int(self,tt_day.lower())
        if tt_day>5:
            tt_day=1
            tt_time=9
        db = all_func.create_conn(self)
        dbcursor = db.cursor()
        query = f"Select MAx(time) From time_table Where branch='{branch}' and sem='{sem}' and division='{division}' and day='{tt_day}'  LIMIT 5"
        dbcursor.execute(query)
        result = dbcursor.fetchone()
        if tt_time>=result[0] :
            tt_day+=1
            tt_time=9
        if tt_day>5:
            tt_day=1
            #print("updated day")
        if tt_time>=0 and tt_time<5:
            tt_time=tt_time+12
            print("updated time")
            print(tt_time)
        if prof_name != None and tt_subject==None and day==None: # prof_name without subject
            #print("psnd")
            return(f"Select time,day,prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}' and day>='{tt_day}' and prof_name LIKE '%{tt_prof_name}%'  LIMIT 5")
        # elif prof_name != None and tt_time!=None:
        #     return(f"Select prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}' and day='{day}' and prof_name='{prof_name}' and time>='{tt_time}'LIMIT 5" )
        elif tt_subject != None and tt_prof_name==None and day==None:
            #print("spnd")
            return(f"Select time,day,prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}'  and lecture ='{tt_subject}' and day>='{tt_day}' LIMIT 5")
        elif prof_name != None and tt_subject==None and day!=None: # prof_name without subject
            #print("psn")
            return(f"Select time,day,prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}' and day='{tt_day}'-1 and prof_name LIKE '%{tt_prof_name}%'  LIMIT 5")
        elif tt_subject != None  and tt_prof_name==None and day!=None:
            #print("spn")
            return(f"Select time,day,prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}'  and lecture ='{tt_subject}'and day='{tt_day}'-1 LIMIT 5")
        elif tt_subject != None  and tt_prof_name!=None :
            #print("spn")
            return(f"Select time,day,prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}'  and lecture ='{tt_subject}'and prof_name LIKE '%{tt_prof_name}%' LIMIT 5")
        
        elif day!=None:
            return(f"Select time,day,prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}' and day='{tt_day}' and time='{tt_time}' LIMIT 5")
        else:
            #print("none")
            return(f"Select time,day,prof_name,lecture,block,block_number,BATCH From time_table Where branch='{branch}' and sem='{sem}' and division='{division}' and day='{tt_day}' and time>='{tt_time}'  LIMIT 1")


class SayHello(Action):
    def name(self) -> Text:
        return "action_say_hello"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        var1 = tracker.current_state()
        db = all_func.create_conn(self)
        dbcursor = db.cursor()
        print(var1)
        if var1["slots"]["user_name"] != "User":
            query = f"SELECT * from `user_details` WHERE `username`='{var1['slots']['user_name']}'"
            dbcursor.execute(query)
            result = dbcursor.fetchone()
            
            dispatcher.utter_message(
                f"Hello {result[1]},{(random.choice(domain['responses']['utter_greet']))['text']}"
            )
            return [SlotSet("login_status", True)]
        else:
            dispatcher.utter_message(
                f"Hello User, {(random.choice(domain['responses']['utter_greet']))['text']}"
            )
            return [SlotSet("login_status", False)]


class ValidateTimeTableForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_time_table_form"

    def validate_branch(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'branch' value."""
        ALLOWED_BRANCH = ["INFT", "CMPN", "BIOM", "EXTC", "ETRX"]

        if slot_value.upper() not in ALLOWED_BRANCH:
            dispatcher.utter_message(
                text=f"We only have branches:INFT/CMPN/EXTC/ETRX/BIOM."
            )
            return {"branch": None}
        else:
            print("validated branch")
            #dispatcher.utter_message(text=f"OK! Your Branch is {slot_value}")
            return {"branch": slot_value}

    def validate_division(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'division' value."""
        ALLOWED_DIVISION = ["A", "B"]

        if slot_value.upper() not in ALLOWED_DIVISION:
            dispatcher.utter_message(
                text=f"We only have Division:A/B."
            )
            return {"division": None}
        else:
            print("validated division")
            #dispatcher.utter_message(text=f"OK! Your Division is {slot_value}")
            return {"division": slot_value}

    def validate_sem(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'sem' value."""

        ALLOWED_SEMESTER = ["1", "2", "3", "4", "5", "6", "7", "8"]

        if slot_value.upper() not in ALLOWED_SEMESTER:
            dispatcher.utter_message(text=f"We only have sem:1 to 8")
            return {"sem": None}
        else:
            print("validated sem")
            #dispatcher.utter_message(text=f"OK! Your Semester is {slot_value}")
            return {"sem": slot_value}

    
class ActionTimetable(Action):
    def name(self) -> Text:
        return "action_time_table"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        login_status=tracker.get_slot("login_status")
        if login_status==True:
            db = all_func.create_conn(self)
            dbcursor = db.cursor()
            username = tracker.get_slot("user_name")
            print(username)
            query = f"Select `branch`,`division`,`sem` from `user_details` WHERE `username`='{username}'"
            dbcursor.execute(query)
            result = dbcursor.fetchone()
            print(result)
            if result[0] == "" or result[1] == "" or result[2]==0:
                dispatcher.utter_message("I need a bit more information to assist you.") 
                return [ActiveLoop("time_table_form")]
            else:
                branch = result[0]
                sem = result[2]
                division = result[1]
                time=tracker.get_slot("time")
                day=tracker.get_slot("day")
                prof_name=tracker.get_slot("prof_name")
                subject=tracker.get_slot("subject")
                # db= all_func().create_conn()
                # dbcursor=db.cursor()
                # print(branch, sem, division,time,day,prof_name,subject)
                get_time_table = all_func.query_tt(self, branch, sem, division,time,day,prof_name,subject)
                print(get_time_table)
                dbcursor.execute(get_time_table)
                result1= dbcursor.fetchall()
                print(result1)
                if len(result1) == 0:
                    # print("hello")
                    dispatcher.utter_message((random.choice(domain['responses']['utter_outofscope']))['text'])
                else:
                    print(type(result1))
                    print(result1[0])
                    print(result1)
                    for i in result1:
                        if i[6]==None:
                            day=all_func.int_to_text(self,int(i[1]))
                            dispatcher.utter_message(f"Professor {i[2]} will be conducting {i[3]} lecture in Block {i[4]}{i[5]} at {i[0]} on {day}")
                            print(day,prof_name,subject,i[6])
                        else:
                            day=all_func.int_to_text(self,int(i[1]))
                            dispatcher.utter_message(f"Professor {i[2]} will be conducting {i[3]} lecture in Block {i[4]}{i[5]} at {i[0]} on {day} for batch {i[6]}")
                            print(day,prof_name,subject,i[6])        
                    return[SlotSet("prof_name",None),SlotSet("subject",None),SlotSet("day",None)]
        else:
            dispatcher.utter_message(domain["responses"]["utter_please_login"][0][Text])

class UploadUserDetails(Action):
    def name(self) -> Text:
        return "action_upload_user_details"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:  
        
        db=all_func.create_conn(self)
        dbcursor=db.cursor()
        d_a=tracker.get_intent_of_latest_message()
        print(d_a)
        if d_a == "affirm":
            branch=tracker.get_slot("branch")
            sem=tracker.get_slot("sem")
            division=tracker.get_slot("division")
            username=tracker.get_slot("user_name")
            print(branch,username,sem,division,"upload_details")
            query=f"UPDATE `user_details` SET `branch` = '{branch}', `division` = '{division}', `sem` = '{sem}' WHERE `user_details`.`username` = '{username}'" 
            dbcursor.execute(query)
            p=dbcursor.rowcount
            db.commit()
            print(d_a)
            print(p)

        else:
            dispatcher.utter_message("What slot do you want change?")
            return[FollowupAction("action_change_info")]
        
class ChangeUserDetails(Action):
    def name(self) -> Text:
        return "action_change_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:  
        print("change value")
        change_info= tracker.get_slot("d_info")
        return[FollowupAction["time_table_form"],SlotSet(f"{change_info}","None")]       
            

# class QueryTimeTable(Action):
#     def name(self) -> Text:
#         return "action_query_time_table"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         branch = tracker.get_slot("branch")
#         sem = tracker.get_slot("sem")
#         division = tracker.get_slot("division")
#         db= all_func().create_conn()
#         dbcursor=db.cursor()
#         get_time_table = all_func.query_tt(self, branch, sem, division)
#         dbcursor.execute(get_time_table)
#         result= dbcursor.fetchall()
#         if result == 0:
#             dispatcher.utter_message("Sorry! but there are no lecture according to the information provided")
#         else:
#             dispatcher.utter_message(result)


class QueryProfessordomain(Action):

    def name(self) -> Text:
        return "action_tell_prof_details"
    
    def run(
        self,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict,
        )-> Dict[Text,Any]:
        login_status=tracker.get_slot("login_status")
        if login_status==True:
            db = all_func.create_conn(self)
            dbcursor=db.cursor()
            prof_name=tracker.get_slot("prof_name")
            subject=tracker.get_slot("subject")
            if prof_name!=None and subject==None:
                query=f"Select * from `prof_details` WHERE `prof_details`.`prof_name` LIKE '%{prof_name}%'"
            elif prof_name==None and subject!=None:
                query=f"Select prof_name , website , email from `prof_details` WHERE `prof_details`.`domain` LIKE '%{subject}%'"
            else:
                dispatcher.utter_message(domain['responses']['utter_outofscope'][0]['text'])
                return []
            print(query)

            dbcursor.execute(query)
            i=dbcursor.fetchall()
            print(i)
            if prof_name!=None and subject== None:
                for result in i:
                    message={
                        "type":"template",
                        "payload":{
                            "template_type":"generic",
                            "elements":[
                                {
                                    "title":f"{result[0]}",
                                    "subtitle":f"{result[0]} is {result[3]} of branch {result[2]}",
                                    "text": f"You can send mail at: [{result[1]}]({result[1]})",
                                   }
                            ]
                        }
                    }
                    dispatcher.utter_message(image=f"{result[4]}")
                    dispatcher.utter_message(f"{result[0]} is {result[3]} of branch {result[2]}.\n")
                    dispatcher.utter_message(f"You can send mail at: [{result[1]}]({result[1]}).\n")
                    dispatcher.utter_message(f"To know more about them visit [website]({result[5]})")    
                    return[SlotSet("prof_name",None),SlotSet("subject",None)]       
            elif prof_name==None and subject!=None:
                if len(i)!= None and len(i)>1:
                    print("more than one")
                    text=""
                    for result in i :
                        text= text + f"[{result[0]}]({result[1]})"+" " 
                        print(text)
                    dispatcher.utter_message(text+f"can help you with {subject}")
                    return[SlotSet("prof_name",None),SlotSet("subject",None)]
                elif len(i)!= None and len(i)<2:
                    for result in i:
                        print(result)
                    return[SlotSet("prof_name",None),SlotSet("subject",None)]
                        
            else:
                dispatcher.utter_message((random.choice(domain['responses']['utter_outofscope']))['text'])
                return[SlotSet("prof_name",None),SlotSet("subject",None)]
        else:
            dispatcher.utter_message(domain["responses"]["utter_please_login"][0][Text])
            

        

# class Timetableaffirm(Action):
#     def name(self) -> Text:
#         return "action_time_table_affirm"

    # def run(
    #     self,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:   
    #     branch=tracker.get_slot("branch")
    #     division=tracker.get_slot("division")
    #     sem= tracker.get_slot("sem")
    #     print("Confirm_details")
    #     result=f"Are you sure this details are correct\n Branch:{branch}\n Division:{division}\n sem:{sem}"
    #     dispatcher.utter_message(result)        
    #     return []
    
class UploadUserDetails(Action):
    def name(self) -> Text:
        return "action_upload_user_details"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:  
        
        db=all_func.create_conn(self)
        dbcursor=db.cursor()
        d_a=tracker.get_intent_of_latest_message()
        print(d_a)
        if d_a == "affirm":
            branch=tracker.get_slot("branch")
            sem=tracker.get_slot("sem")
            division=tracker.get_slot("division")
            username=tracker.get_slot("user_name")
            print(branch,username,sem,division,"upload_details")
            query=f"UPDATE `user_details` SET `branch` = '{branch}', `division` = '{division}', `sem` = '{sem}' WHERE `user_details`.`username` = '{username}'" 
            dbcursor.execute(query)
            p=dbcursor.rowcount
            db.commit()
            print(d_a)
            print(p)

        else:
            dispatcher.utter_message("What slot do you want change?")
            return[FollowupAction("action_change_info")]
        
class ChangeUserDetails(Action):
    def name(self) -> Text:
        return "action_change_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:  
        print("change value")
        change_info= tracker.get_slot("d_info")
        return[FollowupAction["time_table_form"],SlotSet(f"{change_info}","None")]
    
class ChangeUserDetails(Action):
    def name(self) -> Text:
        return "action_check_login_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]: 
        login_status=tracker.get_slot("login_status")
        if login_status == True:
            print("hello")
            return[SlotSet("login_status",True)]
        else:
            print("hii")
            return[SlotSet("login_status",False)]
        
class AdministrativeOffice(Action):
    def name(self) -> Text:
        return "action_administrative_office"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]: 
        office_name=tracker.get_slot("office_location")
        db=all_func.create_conn(self)
        dbcursor=db.cursor()
        query=f"Select * from administrative_office Where office_name LIKE %{office_name}% "
        result=dbcursor.execute(query)
        if len(result)==0:
            dispatcher.utter_message("I don't think this place exits")
        else:
            dispatcher.utter_message(f"{result[1]} is located at {result[2]}")

class CoursedOffered(Action):
    def name(self) -> Text:
        return "action_courses_offered"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]: 
        CoursedOffered=tracker.get_latest_entity_values("branch")
        print(CoursedOffered)
        ALLOWED_BRANCH = ["INFT", "CMPN", "BIOM", "EXTC", "ETRX"]
        if CoursedOffered == None:
            dispatcher.utter_message(domain['responses']['utter_courses_offered'][0]['text'])

        elif CoursedOffered.upper() not in ALLOWED_BRANCH:
            dispatcher.utter_message(
                f"we don't have a program for {CoursedOffered}, but we do offer other engineering programs you may be interested in.",
                domain['responses']['utter_courses_offered'][0]['text']
            )
        elif CoursedOffered.upper() in ALLOWED_BRANCH:
            
            if CoursedOffered.upper()=="INFT":
                dispatcher.utter_message(f"Yes we do offer {CoursedOffered} program" ,f"To know more about [Information Technology](https://vit.edu.in/information-technology.html) click on it")
            elif CoursedOffered.upper()=="CMPN":
                dispatcher.utter_message(f"Yes we do offer {CoursedOffered} program" ,f" [Computer Engineering](https://vit.edu.in/computer-engineering.html) click on it" )
            elif CoursedOffered.upper()=="ETRX":
                dispatcher.utter_message(f"Yes we do offer {CoursedOffered} program" ,f" [Electronics and Computer Science](https://vit.edu.in/electronics-engineering.html) click on it" )
            elif CoursedOffered.upper()=="EXTC":
                dispatcher.utter_message(f"Yes we do offer {CoursedOffered} program" ,f" [Electronics and Telecommunication Engineering](https://vit.edu.in/electronics-telecommunication-engineering.html) click on it" )
            elif CoursedOffered.upper()=="BIOM":
                dispatcher.utter_message(f"Yes we do offer {CoursedOffered} program" ,f" [Biomedical Engineering](https://vit.edu.in/biomedical-engineering.html) click on it" )
            else:
                dispatcher.utter_message(domain['responses']['utter_courses_offered'][0]['text'])
        else:
            dispatcher.utter_message(domain['responses']['utter_courses_offered'][0]['text'])
    