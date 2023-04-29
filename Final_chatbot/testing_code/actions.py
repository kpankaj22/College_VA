from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker , FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions import tt_query
from actions import sql_conn

class ActionSayBranch(Action):

    def name(self) -> Text:
        return "action_say_branch"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        branch = tracker.get_slot("branch")
        if not branch:
            dispatcher.utter_message(text="I don't know your shirt size.")
        else:
            dispatcher.utter_message(text=f"Your branch is {branch}!")
        return []
    
    
class ValidateTimeTableForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_time_table_form"

    def validate_branch(
        self,
        slot_value:Any,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict,
        )-> Dict[Text,Any]:
        """Validate 'branch' value."""

        ALLOWED_BRANCH  =["INFT","CMPN","BIOM","EXTC","ETRX"]

        if slot_value.upper() not in ALLOWED_BRANCH:
            dispatcher.utter_message(text=f"We only have branches:INFT/CMPN/EXTC/ETRX/BIOM.")
            return{"branch":None}
        dispatcher.utter_message(text=f"OK! Your Branch is {slot_value}")
        return{"branch":slot_value}

    def validate_division(
        self,
        slot_value:Any,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict,
        )-> Dict[Text,Any]:
        """Validate 'division' value."""

        ALLOWED_DIVISION=["A","B"]

        if slot_value.upper() not in ALLOWED_DIVISION:
            dispatcher.utter_message(text=f"We only have branches:INFT/CMPN/EXTC/ETRX/BIOM.")
            return{"division":None}
        dispatcher.utter_message(text=f"OK! Your Division is {slot_value}")
        return{"division":slot_value}
        
    def validate_sem(
        self,
        slot_value:Any,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict,
        )-> Dict[Text,Any]:
        """Validate 'sem' value."""

        ALLOWED_SEMESTER=["1","2","3","4","5","6","7","8"]

        if slot_value.upper() not in ALLOWED_SEMESTER:
            dispatcher.utter_message(text=f"We only have :INFT/CMPN/EXTC/ETRX/BIOM.")
            return{"sem":None}
        dispatcher.utter_message(text=f"OK! Your Semester is {slot_value}")
        return{"sem":slot_value}
    
class QueryTimeTable(Action):

    def name(self) -> Text:
        return "action_query_time_table"
    
    def run(
        self,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict,
        )-> Dict[Text,Any]:
        
        branch= tracker.get_slot("branch")
        sem= tracker.get_slot("sem")
        division=tracker.get_slot("division")
        day=tracker.get_slot("day")
        tt_time=tracker.get_slot("tt_time")
        
        db=sql_conn.create_conn()
        dbcursor=db.cursor()

        if day is not None and tt_time is not None:
            if tt_time>16:
                if day =="tommorrow":
                    
        
"""class QueryProfessordomain(Action):

    def name(self) -> Text:
        return "action_professor_domain"
    
    def run(
        self,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict,
        )-> Dict[Text,Any]:

        subject= tracker.get_slot("subject")

        get_professor_domain= query_prof_domain.query_pd(subject)"""