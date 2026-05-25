from langchain.tools import tool
from langchain.agents import create_agent

class AgenteCalendario:
  def __init__(self, model):
    # self.revisar_disponibilidad_tool = tool("revisar_disponibilidad")(self.revisar_disponibilidad)
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

  @tool
  def revisar_disponibilidad(fecha: str):
    """Obtiene eventos de una fecha"""
    print(f"Obteniendo eventos de {fecha}...")

    return "No hay eventos programados para esta fecha"
  
  def procesar(self, input):
    res = self.agent.invoke(
      {"messages": [{"role": "user", "content": input}], "config": {"recursion_limit": 6}}
    )
    return res["messages"][-1].content