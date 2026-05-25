from langchain.tools import tool
from langchain.agents import create_agent

class AgenteClima:
  def __init__(self, model):
    # self.obtener_clima_tool = tool("obtener_clima")(self.obtener_clima)
    self.agent = create_agent(
      model=model,
      tools=[self.obtener_clima],
      system_prompt=(
        "Eres un agente especialista en clima de ciudades"
        "Solo debes responder preguntas relacionadas con el clima"
        "Si necesitas conocer el clima de una ciudad, usa la herramienta obtener_clima"
        "Responde en español de manera breve y concisa"
      )
    )

  @tool
  def obtener_clima(ciudad: str):
    """Obtiene el clima actual de una ciudad"""
    print(f"Obteniendo el clima de {ciudad}...")

    data = {
      "madrid": "Soleado, 25°C",
      "barcelona": "Nublado, 22°C",
      "valencia": "Lluvioso, 18°C"
    }

    return data.get(ciudad.strip().lower(), "Ciudad no encontrada")
  
  def procesar(self, input):
    res = self.agent.invoke(
      {"messages": [{"role": "user", "content": input}], "config": {"recursion_limit": 6}}
    )
    return res["messages"][-1].content