from nicegui import ui
from ui.pages.home_page import HomePage
from ui.pages.page1 import Page1
from ui.pages.page2 import Page2
from ui.pages.page3 import Page3
from ui.pages.page4 import Page4
from ui.components.navbar import Navbar
from ui.components.footer import Footer

def setup_routes():
    @ui.page('/')
    def home():
        Navbar()
        HomePage()
        Footer()

    @ui.page('/page1')
    def page1():
        Navbar()
        Page1()
        Footer()
    
    @ui.page('/page2')
    def page2():
        Navbar()
        Page2()
        Footer()
    
    @ui.page('/page3')
    def page3():
        Navbar()
        Page3()
        Footer()
    
    @ui.page('/page4')
    def page4():
        Navbar()
        Page4()
        Footer()
