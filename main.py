from nicegui import ui
from ui.router import setup_routes

def main():
    setup_routes()  
    ui.run(show=True, port=8080)

if __name__  in {"__main__", "__mp_main__"}:
    main()
