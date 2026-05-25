from langchain.tools import tool
from langchain.agents import create_agent

class AgenteCalendario:
  def __init__(self, model):
    self.agent = create_agent(
      model=model,
      tools=[self.revisar_disponibilidad],
      system_prompt=(
        "Eres un agente especialista en calendario, agendar eventos y disponibilidad de fechas y horarios"
        "Solo debes responder preguntas relacionadas con el calendario"
        "Si necesitas conocer disponibilidad de eventos o fechas, usa la herramienta revisar_disponibilidad"
        "Responde en español de manera breve y concisa"
      )
    )

  @tool("revisar_disponibilidad")
  def revisar_disponibilidad(self, fecha: str):
    """Obtiene eventos de una fecha"""
    print(f"Obteniendo eventos de {fecha}...")

    data = {
      "2024-06-01": "Reunión de equipo a las 10:00",
      "2024-06-02": "Entrega de proyecto",
      "2024-06-03": "Día libre"
    }

    return data.get(fecha, "No se encontraron eventos para esta fecha")
  
  def procesar(self, input):
    res = self.agent.invoke(
      {"messages": [{"role": "user", "content": input}], "config": {"recursion_limit": 6}}
    )
    return res["messages"][-1].content