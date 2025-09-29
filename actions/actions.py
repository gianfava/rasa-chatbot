from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionValidarSabor(Action):
    """Valida se o sabor é feito pela pizzaria"""

    def name (self) -> Text:
        return "action_validar_sabor"
    
    def run (self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sabor =tracker.get_slot("sabor")

        sabores_disponiveis = ["portuguesa", "calabresa", "frango", "mussarela", "margherita", "picanha"]

        if sabor and sabor.lower() in sabores_disponiveis:
            dispatcher.utter_message(text=f"Boa escolha! Pizza de {sabor} é nossa especialidade")
            return[]
        else:
            dispatcher.utter_message(text=f"Não temos pizza de {sabor}, escolha outro sabor")
            return [SlotSet("sabor", None)]