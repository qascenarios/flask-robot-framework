import glob
import os
import shutil


def get_chrome_driver_path():
    """Return ChromeDriver path from CHROMEDRIVER env, PATH, or ~/.wdm cache."""
    env_path = os.environ.get("CHROMEDRIVER", "").strip()
    if env_path and os.path.exists(env_path):
        return env_path

    path_driver = shutil.which("chromedriver")
    if path_driver:
        return path_driver

    # Fall back to any cached driver installed by webdriver-manager
    cache_pattern = os.path.expanduser("~/.wdm/drivers/chromedriver/**/*chromedriver")
    matches = sorted(glob.glob(cache_pattern, recursive=True))
    if matches:
        return matches[-1]

    return ""
