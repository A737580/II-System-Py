from nicegui import ui
from core.config import Config

class Footer:
    def __init__(self):
        with ui.row().classes("w-full justify-center bg-gray-100 p-2 mt-4"):
            ui.label(f"© 2025 {Config.APP_NAME} v{Config.VERSION}")
