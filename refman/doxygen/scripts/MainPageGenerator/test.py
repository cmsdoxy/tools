from MainPageGenerator import *

l = MainPageGenerator(path = "C:/eclipseWorkspace/MPG/", test = True)

l.CreateNewMainPage("test.html")

l.ExportJSON("data.json")