import json
import os
from pathlib import Path
from typing import Any

# =============================================================================
# Package Directory & Install Detection
# =============================================================================


def get_package_dir() -> Path:
    """Get the base directory of the package."""
    env_dir = os.environ.get("PI_PACKAGE_DIR")
    if env_dir:
        return Path(env_dir).resolve()

    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        # In a monorepo, locate the coding-agent package
        if (parent / "packages/coding-agent/package.json").exists():
            return (parent / "packages/coding-agent").resolve()
        if (parent / "package.json").exists() and parent.name == "coding-agent":
            return parent.resolve()

    return current


def get_package_json_path() -> Path:
    return get_package_dir() / "package.json"


def get_readme_path() -> Path:
    return get_package_dir() / "README.md"


def get_docs_path() -> Path:
    return get_package_dir() / "docs"


def get_examples_path() -> Path:
    return get_package_dir() / "examples"


def get_changelog_path() -> Path:
    return get_package_dir() / "CHANGELOG.md"


def detect_install_method() -> str:
    return "unknown"


# =============================================================================
# Load Configuration from package.json
# =============================================================================

pkg: dict[str, Any] = {}
try:
    with open(get_package_json_path(), "r", encoding="utf-8") as f:
        pkg = json.load(f)
except Exception:
    pass

pi_config = pkg.get("piConfig", {})
pi_config_name = pi_config.get("name")

PACKAGE_NAME: str = pkg.get("name", "@earendil-works/pi-coding-agent")
APP_NAME: str = pi_config_name or "pi"
APP_TITLE: str = APP_NAME if pi_config_name else "π"
CONFIG_DIR_NAME: str = pi_config.get("configDir", ".pi")
VERSION: str = pkg.get("version", "0.0.0")

ENV_AGENT_DIR = f"{APP_NAME.upper()}_CODING_AGENT_DIR"
ENV_SESSION_DIR = f"{APP_NAME.upper()}_CODING_AGENT_SESSION_DIR"


def expand_tilde_path(path: str) -> str:
    return os.path.expanduser(path)


# =============================================================================
# User Config Paths (~/.pi/agent/*)
# =============================================================================


def get_agent_dir() -> Path:
    """Get the agent config directory (e.g., ~/.pi/agent/)"""
    env_dir = os.environ.get(ENV_AGENT_DIR)
    if env_dir:
        return Path(expand_tilde_path(env_dir)).resolve()
    return Path(os.path.expanduser("~")) / CONFIG_DIR_NAME / "agent"


def get_custom_themes_dir() -> Path:
    return get_agent_dir() / "themes"


def get_models_path() -> Path:
    return get_agent_dir() / "models.json"


def get_auth_path() -> Path:
    return get_agent_dir() / "auth.json"


def get_settings_path() -> Path:
    return get_agent_dir() / "settings.json"


def get_tools_dir() -> Path:
    return get_agent_dir() / "tools"


def get_bin_dir() -> Path:
    return get_agent_dir() / "bin"


def get_prompts_dir() -> Path:
    return get_agent_dir() / "prompts"


def get_sessions_dir() -> Path:
    return get_agent_dir() / "sessions"


def get_debug_log_path() -> Path:
    return get_agent_dir() / f"{APP_NAME}-debug.log"


# =============================================================================
# Helper function
# =============================================================================

DEFAULT_SHARE_VIEWER_URL = "https://pi.dev/session/"


def get_share_viewer_url(gist_id: str) -> str:
    base_url = os.environ.get("PI_SHARE_VIEWER_URL", DEFAULT_SHARE_VIEWER_URL)
    return f"{base_url}#{gist_id}"
