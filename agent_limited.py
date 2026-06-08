from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
# from langchain.agents.middleware import ModelCallLimitMiddleware
# from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.agents.middleware import PIIMiddleware

load_dotenv()

DATA = {
    "laptop": {
        "precio": 399.99,
        "costo": 299.99,
        "caracteristicas": "Laptop Gamer 16GB RAM 1TB SSD Intel i5 NVIDIA 4050",
        "disponibilidad": 3
    },
    "celular": {
        "precio": 199.99,
        "costo": 129.99,
        "caracteristicas": "Samsung Galaxy S26 Ultra, Desbloqueado, 512GB, Negro",
        "disponibilidad": 19
    },
    "audifonos": {
        "precio": 59.99,
        "costo": 39.99,
        "caracteristicas": "Soundcore P30i con CancelaciÃ³n de Ruido. 45H de ReproducciÃ³n, InalÃ¡mbricos. Color Verde"
    },
}

@tool
def get_product_catalog() -> str:
    """
    Obtener el listado de productos existentes (solo su nombre), para despuÃ©s poder buscar su informaciÃ³n con get_product_info(producto)
    """
    
    print(f"  * Llamando herramienta get_product_catalog")
    
    return {
        "products": ", ".join(DATA.keys()),
        "number_of_products": len(DATA)
    }

@tool
def get_product_info(product: str) -> str:
    """
    Obtener información de productos, como características, precios y disponibilidad, en base al nombre del producto
    """
    
    print(f"  * Llamando herramienta get_product_info con {product}")
    
    return DATA.get(product.lower(), "No contamos con ese producto en existencia")

SYSTEM_PROMPT = """
Eres un asistente encargado de dar servicio al cliente para una tienda de productos de tecnología.

Reglas:
- Siempre habla en español y de manera concisa.
- Si el usuario quiere saber información de un producto, usa la herramienta get_product_info, enviando el producto que desea conocer (e.g. laptop, celular, audifonos)
"""

model = init_chat_model("gpt-4.1-mini", model_provider="openai")

agent = create_agent(
    model=model,
    tools=[get_product_catalog, get_product_info],
    system_prompt=SYSTEM_PROMPT,
    middleware=[
        # ModelCallLimitMiddleware(
        #     run_limit=2,
        #     exit_behavior="error"
        # )
        # ToolCallLimitMiddleware(
        #     tool_name="get_product_info",
        #     run_limit=2,
        #     exit_behavior="continue"
        # )
        PIIMiddleware("email", strategy="redact"),
    ],
    checkpointer=InMemorySaver(),
)

while True:
    user_message = input("You: ").strip()

    if user_message.lower() in {"exit", "salir"}:
        break

    if not user_message:
        continue

    try:
        result = agent.invoke(
            {"messages": [{"role": "user","content": user_message}]},
            config={"configurable": {"thread_id": "1",}}
        )
        print(f"Agente: {result["messages"][-1].content}")
    except Exception as exc:
        print(f"Error: {type(exc).__name__}: {exc}\n")