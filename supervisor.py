from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model

from agente_calendario import AgenteCalendario
from agente_clima import AgenteClima

class Supervisor:
  def __init__(self, model, agente_clima, agente_calendario):
    self.model = model
    self.agente_clima = agente_clima
    self.agente_calendario = agente_calendario

    @tool
    def delegar_a_agente_clima(input):
      """Consulta al especialista en clima cuando la solicitud hable de clima o temperatura"""
      print(f"Supervisor delega a agente_clima: {input}")
      return self.agente_clima.procesar(input)
    
    @tool
    def delegar_a_agente_calendario(input):
      """Consulta al especialista en calendario cuando la solicitud hable de eventos, fechas o disponibilidad"""
      print(f"Supervisor delega a agente_calendario: {input}")
      return self.agente_calendario.procesar(input)

    self.supervisor = create_agent(
      model=model,
      tools=[delegar_a_agente_clima, delegar_a_agente_calendario],
      system_prompt=(
        "Eres un supervisor que coordina dos agentes: uno especialista en clima y otro especialista en calendario"
        "Tu tarea es recibir preguntas del usuario, determinar cuál agente es el adecuado para responder y delegar la pregunta a ese agente"
        "Si la solicitud mezcla temas, puedes usar más de un especialista."
        "No llames especialistas que no sean necesarios para responder la pregunta"
        "Responde en español de manera breve y concisa"
      )
    )

  def chat(self):
    while True:
      user_input = input("\nTú: ").strip()
      if user_input.lower() in ["salir", "exit"]:
        print("Supervisor: ¡Hasta luego!")
        break

      print(f"Tú -> Supervisor: {user_input}")

      res = self.supervisor.invoke(
        {"messages": [{"role": "user", "content": user_input}], "config": {"recursion_limit": 6}}
      )
      print(f"Supervisor -> Tú: {res['messages'][-1].content}")

load_dotenv()

model = init_chat_model("gpt-4.1-mini", model_provider="openai")

agente_clima = AgenteClima(model)
agente_calendario = AgenteCalendario(model)
supervisor = Supervisor(model, agente_clima, agente_calendario)

supervisor.chat()