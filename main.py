from db.db import tout_creer
from interf.pages import PoliceApp
import db.db

if __name__ == '__main__':
    tout_creer()
    app = PoliceApp()
    app.run()