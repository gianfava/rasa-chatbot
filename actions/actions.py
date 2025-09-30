from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionValidarSabor(Action):
    """Valida se o sabor é feito pela pizzaria"""
    def name (self) -> Text:
        return "action_validar_sabor"
    def run (self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sabor = tracker.get_slot("sabor")
        sabores_disponiveis = ["portuguesa", "calabresa", "frango", "mussarela", "margherita", "picanha"]
        if sabor and sabor.lower() in sabores_disponiveis:
            dispatcher.utter_message(text=f"Boa escolha! Pizza de {sabor} é nossa especialidade")
            return []
        else:
            dispatcher.utter_message(text=f"Não temos pizza de {sabor}, escolha outro sabor")
            return [SlotSet("sabor", None)]

class ActionValidarTamanho(Action):
    """Valida se o tamanho da pizza está disponível"""
    def name(self) -> Text:
        return "action_validar_tamanho"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tamanho = tracker.get_slot("tamanho")
        tamanhos_disponiveis = ["pequena", "média", "grande"]
        if tamanho and tamanho.lower() in tamanhos_disponiveis:
            dispatcher.utter_message(text=f"Ok, pizza tamanho {tamanho}.")
            return []
        else:
            dispatcher.utter_message(text=f"Não temos o tamanho {tamanho}, por favor escolha entre pequena, média ou grande.")
            return [SlotSet("tamanho", None)]

class ActionCalcularPreco(Action):
    """Calcula o preço da pizza e pergunta a forma de pagamento"""
    def name(self) -> Text:
        return "action_calcular_preco"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sabor = tracker.get_slot("sabor")
        tamanho = tracker.get_slot("tamanho")
        precos = {
            "pequena": {"portuguesa": 20, "calabresa": 22, "frango": 21, "mussarela": 18, "margherita": 23, "picanha": 25},
            "média": {"portuguesa": 30, "calabresa": 32, "frango": 31, "mussarela": 28, "margherita": 33, "picanha": 35},
            "grande": {"portuguesa": 40, "calabresa": 42, "frango": 41, "mussarela": 38, "margherita": 43, "picanha": 45}
        }
        preco = precos.get(tamanho, {}).get(sabor)
        if preco:
            message = f"O preço da sua pizza de {sabor} tamanho {tamanho} é de R${preco:.2f}."
            dispatcher.utter_message(text=message)
            dispatcher.utter_message(response="utter_pedir_forma_pagamento")
            return [SlotSet("preco", preco)]
        else:
            dispatcher.utter_message(text="Não foi possível calcular o preço. Por favor, verifique seu pedido.")
            return []

class ActionFinalizarPedido(Action):
    """Agradece e informa o tempo de entrega"""
    def name(self) -> Text:
        return "action_finalizar_pedido"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_finalizar_pedido")
        return []