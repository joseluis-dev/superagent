from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

SKILLS_DIR = Path(__file__).parent / "skills"

model = init_chat_model("gpt-4.1-mini", model_provider="openai")

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