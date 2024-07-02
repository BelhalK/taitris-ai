from pathlib import Path

custom_env="/Users/belhalkarimi/Desktop/Belhal/Tech/taitris/taitris-ai"

def get_project_root():
    """
    Finds the project root by searching for .git, .project_root, or .gitignore
    files or directories. Raises an exception if not found.
    """
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
    PROJECT_ROOT = ENV_ROOT / "src"
    DATA_PATH = PROJECT_ROOT / "data"
    WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
    PROMPT_PATH = PROJECT_ROOT / "taitriscore/prompts"
    TMP = PROJECT_ROOT / "tmp"
    RESEARCH_PATH = DATA_PATH / "research"
except Exception as e:
    # Log the exception if needed
    print(f"Error finding project root: {e}")
    
    # Default paths if project root is not found
    ENV_ROOT = Path(custom_env)
    PROJECT_ROOT = ENV_ROOT / "src"
    DATA_PATH = PROJECT_ROOT / "data"
    WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
    PROMPT_PATH = PROJECT_ROOT / "taitriscore/prompts"
    TMP = PROJECT_ROOT / "tmp"
    RESEARCH_PATH = DATA_PATH / "research"

# Time-to-live for memory in seconds
MEM_TTL = 24 * 30 * 3600