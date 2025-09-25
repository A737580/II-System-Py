from nicegui import ui
from ui.pages.home_page import HomePage
from ui.pages.page1 import Page1
from ui.components.navbar import Navbar
from ui.components.footer import Footer

def setup_routes():
    @ui.page('/')
    def home():
        Navbar()
        HomePage()
        Footer()

    @ui.page('/page1')
    def page3():
        Navbar()
        Page1()
        Footer()
