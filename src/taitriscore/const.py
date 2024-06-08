from pathlib import Path


def get_project_root():
    current_path = Path.cwd()
    while True:
        if (
            (current_path / ".git").exists()
            or (current_path / ".project_root").exists()
            or (current_path / ".gitignore").exists()
        ):
            return current_path
        parent_path = current_path.parent
        if parent_path == current_path:
            raise Exception("Project root not found.")
        current_path = parent_path


try:
    ENV_ROOT = get_project_root()
    PROJECT_ROOT = get_project_root() / "src"
    DATA_PATH = PROJECT_ROOT / "data"
    WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
    PROMPT_PATH = PROJECT_ROOT / "taitriscore/prompts"
    TMP = PROJECT_ROOT / "tmp"
    RESEARCH_PATH = DATA_PATH / "research"
except:
    ENV_ROOT = Path("/Users/belhalkarimi/Desktop/Belhal/Tech/taitris/taitris-ai")
    PROJECT_ROOT = Path(
        "/Users/belhalkarimi/Desktop/Belhal/Tech/taitris/taitris-ai/src"
    )
    DATA_PATH = PROJECT_ROOT / "data"
    WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
    PROMPT_PATH = PROJECT_ROOT / "taitriscore/prompts"
    TMP = PROJECT_ROOT / "tmp"
    RESEARCH_PATH = DATA_PATH / "research"

MEM_TTL = 24 * 30 * 3600
