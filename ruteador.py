from typing import Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from pydantic import BaseModel, Field

load_dotenv()

model = init_chat_model("gpt-4.1-mini", model_provider="openai")

class RouteDecision(BaseModel):
  route: Literal["ventas", "soporte", "otros"] = Field(..., description="Ruta elegida para atender la solicitud del usuario")
  reason: str = Field(..., description="Breve explicación de por qué se eligió esa ruta")

agente_ruteador = create_agent(
  model=model,
  tools=[],
  system_prompt=(
    "Eres un agente especializado en clasificación de solicitudes."
    "Deberás clasificar la solicitud del usuario en solo una de estas 3 categorías: "
    "ventas, soporte u otros."
    "Usa ventas si pregunta por precios, planes, demos o contratación."
    "Usa soporte si reporta errores, problemas de acceso o fallas en el servicio."
    "Usa otros para cualquier otra solicitud que no encaje en las categorías anteriores."
  ),
  response_format=RouteDecision
)

agente_venta = create_agent(
  model=model,
  tools=[],
  system_prompt=(
    "Eres un agente especializado en ventas."
    "Tu tarea es atender preguntas relacionadas con precios, planes, demos o contratación."
    "Tus productos disponibles: Celulares, accesorios de celular, protectores de celular y cargadores."
    "No digas precios específicos, solo menciona que los precios son los más bajos del mercado y que ofrecemos promociones frecuentes."
    "Responde de manera breve y concisa."
  )
)

agente_soporte = create_agent(
  model=model,
  tools=[],
  system_prompt=(
    "Eres un agente especializado en soporte."
    "Tu tarea es atender preguntas relacionadas con errores, problemas de acceso o fallas en el servicio."
    "Debes hablar en español y responder con pasos concretos y en lista paso a paso para solucionar el problema del usuario."
    "Solo puedes atender soporte técnico, no respondas preguntas de ventas o de otros temas."
    "Responde de manera breve y concisa."
  )
)

agente_general = create_agent(
  model=model,
  tools=[],
  system_prompt=(
    "Eres un agente especializado en atención general."
    "Tu tarea es atender preguntas que no encajan en las categorías de ventas o soporte."
    "Responde de manera breve y concisa."
  )
)

def select_agent(route):
  if route == "ventas":
    return agente_venta
  elif route == "soporte":
    return agente_soporte
  else:
    return agente_general

while True:
  user_input = input("\nTú: ").strip()
  if user_input.lower() in ["salir", "exit"]:
    print("Agente Ruteador: ¡Hasta luego!")
    break

  print(f"Tú -> Agente Ruteador: {user_input}")

  res = agente_ruteador.invoke(
    {"messages": [{"role": "user", "content": user_input}]}
  )
  decision = res["structured_response"]
  print(f"Agente Ruteador -> Tú: Ruta elegida: {decision.route}, Razón: {decision.reason}")

  agente_seleccionado = select_agent(decision.route)
  res = agente_seleccionado.invoke(
    {"messages": [{"role": "user", "content": user_input}]}
  )
  print(f"{decision.route.capitalize()} -> Tú: {res['messages'][-1].content}")