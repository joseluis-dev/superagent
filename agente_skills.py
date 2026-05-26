from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

SKILLS_DIR = Path(__file__).parent / "skills"

model = init_chat_model("gpt-4.1-mini", model_provider="openai")
checkpointer = InMemorySaver()

def get_metadata_value(metadata: str, key: str) -> str | None:
    prefix = f"{key}:"

    for line in metadata.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()

    return None


def read_skill(skill_file: Path) -> dict[str, str]:
    content = skill_file.read_text(encoding="utf-8")
    _, metadata, instructions = content.split("---", 2)

    name = get_metadata_value(metadata, "name") or skill_file.parent.name
    description = get_metadata_value(metadata, "description") or "Sin descripción"

    return {
        "name": name,
        "description": description,
        "instructions": instructions.strip(),
    }

def load_skills() -> dict[str, dict[str, str]]:
    skills = {}

    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        skill = read_skill(skill_file)
        skills[skill["name"]] = skill

    return skills

SKILLS = load_skills()

def build_skill_catalog() -> str:
    lines = ["Skills disponibles:"]

    for skill in SKILLS.values():
        lines.append(f"- {skill['name']}: {skill['description']}")

    return "\n".join(lines)


print(build_skill_catalog())

@tool
def load_skill(skill_name: str) -> str:
    """Carga una skill por su nombre y devuelve sus instrucciones"""
    print(f"Cargando skill '{skill_name}'...")
    skill = SKILLS.get(skill_name)
    if skill is None:
        return f"No se encontró la skill '{skill_name}'"
    
    return skill["instructions"]

agent = create_agent(
    model=model,
    tools=[load_skill],
    checkpointer=checkpointer,
    system_prompt=(
        "Eres un asistente con skills bajo demanda."
        "No tienes que cargar skills para solicitudes simples."
        "Cuando la tarea requiera una especialidad, usa load_skill en tu respuesta final."
        "Responde en español de manera breve y concisa, y solo carga la skill que sea estrictamente necesaria para resolver la solicitud del usuario.\n\n"
        f"{build_skill_catalog()}"
    )
)

config = {
    "configurable": {"thread_id": "1"},
    "recursion_limit": 8,
}

while True:
    user_input = input("\nTú: ").strip()

    if user_input.lower() in ["salir", "exit"]:
        print("Asistente: ¡Hasta luego!")
        break

    print(f"Tú -> Asistente: {user_input}")

    res = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config
    )
    print(f"Asistente -> Tú: {res['messages'][-1].content}")