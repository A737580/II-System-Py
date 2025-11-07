from nicegui import ui
from ui.router import setup_routes
from models.exercise4.test2 import run_tests
from models.exercise4.test1 import test_fuzzy_system

def main():
    # test_fuzzy_system()
    # run_tests()
    setup_routes()  
    ui.run(show=True, port=8080)

if __name__  in {"__main__", "__mp_main__"}:
    main()
