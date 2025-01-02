import sqlite3
import os
from citoyen.citoyen import Citoyen

CHEMIN = os.path.join(os.path.dirname( os.path.dirname( __file__ )), "interf", "enquete.db")

def tout_creer():
    creer_table_temoin()
    creer_table_preuves()
    creer_table_suspect()
    creer_table_user()
    creer_table_enquete()
    creer_table_rapport()
    creer_table_victime()
    creer_table_criminel()
    creer_table_citoyens()



def creer_table_citoyens():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS citoyen (
        cId INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        nationalite TEXT NOT NULL,
        date_naissance DATETIME NOT NULL,
        date_mort DATETIME null,
        adresse TEXT NULL,
        age INTEGER NOT NULL
        
        )
    """)
    connexion.commit()
    connexion.close()

def creer_table_user():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS inspecteur (
            idUser INTEGER PRIMARY KEY AUTOINCREMENT,
            mail TEXT NOT NULL,
            cId INTEGER NOT NULL,
            poste TEXT NOT NULL,
            droitsEnquete INTEGER NOT NULL,
            FOREIGN KEY (cId) REFERENCES citoyen(cId)
        );
        """)
    cursor.execute(f"""
CREATE TABLE IF NOT EXISTS inspecteur_enquete (
idUser INTEGER NOT NULL,
eId INTEGER NOT NULL,
PRIMARY KEY (idUser, eId),
FOREIGN KEY (idUser) REFERENCES citoyen(cId),
FOREIGN KEY (eId) REFERENCES citoyen(cId)
)

""")

    connexion.commit()
    connexion.close()

def creer_table_victime():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(
        f"""
    CREATE TABLE IF NOT EXISTS victime (
        idVictime INTEGER PRIMARY KEY AUTOINCREMENT,
        cId INTEGER NOT NULL,
        foreign key (cId) REFERENCES citoyen(cId));
        """)
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS victime_enquete (
        idVictime INTEGER NOT NULL,
        eId INTEGER NOT NULL,
        cause TEXT ,
        
        PRIMARY KEY (idVictime, eId),
        FOREIGN KEY (eId) REFERENCES enquete(eId),
        FOREIGN KEY (idVictime) REFERENCES victime(idVictime)
           
    )"""
    )
    connexion.commit()
    connexion.close()

def creer_table_criminel():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS criminel (
        idCriminel INTEGER PRIMARY KEY AUTOINCREMENT,
        cId INTEGER NOT NULL UNIQUE,
        statut TEXT NOT NULL,
        FOREIGN KEY (cId) REFERENCES citoyen(cId));
        """)
    cursor.execute(f"""    
        CREATE TABLE IF NOT EXISTS criminel_enquete (
        idCriminel INTEGER NOT NULL,
        eId INTEGER NOT NULL,
        typeCriminel TEXT NOT NULL,
        PRIMARY KEY (eId, idCriminel),
        foreign key (eId) REFERENCES enquete(eId),
        FOREIGN KEY (idCriminel) REFERENCES criminel(cId));
        """
    )
    connexion.commit()
    connexion.close()

def creer_table_suspect():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS suspect (
        idSuspect INTEGER PRIMARY KEY AUTOINCREMENT,
        cId INTEGER NOT NULL,
        FOREIGN KEY (cId) REFERENCES citoyen(cId));
        """)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS suspect_enquete (
        idSuspect INTEGER NOT NULL,
        eId INTEGER NOT NULL,
        PRIMARY KEY (eId, idSuspect),
        foreign key (eId) REFERENCES enquete(eId),
        FOREIGN KEY (idSuspect) REFERENCES suspect(idSuspect)
        );
        
        """
    )
    connexion.commit()
    connexion.close()

def creer_table_temoin():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS temoin (
        idTemoin INTEGER NOT NULL,
        cId INTEGER NOT NULL,
        PRIMARY KEY (idTemoin)
        ,FOREIGN KEY (cId) REFERENCES citoyen(cId));
        """)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS temoin_enquete (
        idTemoin INTEGER NOT NULL,
        eId INTEGER NOT NULL,
        temoignage TEXT NOT NULL,
        PRIMARY KEY (idTemoin, eId),
        foreign key (eId) REFERENCES enquete(eId),
        FOREIGN KEY (idTemoin) REFERENCES temoin(idTemoin));
        
        """

    )
    connexion.commit()
    connexion.close()


def creer_table_preuves():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(
        f"""
CREATE TABLE IF NOT EXISTS preuves (
idPreuve PRIMARY KEY NOT NULL,
typePreuve TEXT NOT NULL,
categoriePreuve TEXT NOT NULL,
analyse TEXT,
description TEXT,
imageUrl TEXT,
dateDecouverte DATETIME NOT NULL);
""")
    cursor.execute(f"""
CREATE TABLE IF NOT EXISTS preuves_enquete (
idPreuve INTEGER NOT NULL,
eId INTEGER NOT NULL,
emplacement TEXT NOT NULL,
PRIMARY KEY (idPreuve, eId),
foreign key (eId) REFERENCES enquete(eId),
FOREIGN KEY (idPreuve) REFERENCES preuves(idPreuve));
""")
    cursor.execute(f"""
CREATE TABLE IF NOT EXISTS preuves_suspect (
idPreuve INTEGER NOT NULL,
idSuspect INTEGER NOT NULL,
PRIMARY KEY (idPreuve, idSuspect),
FOREIGN KEY (idPreuve) REFERENCES preuves(idPreuve),
FOREIGN KEY (idSuspect) REFERENCES suspect(idSuspect)
);

"""
    )
    connexion.commit()
    connexion.close()

def creer_table_rapport():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(
        f"""
CREATE TABLE IF NOT EXISTS rapport (
idRapport INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
eId INTEGER NOT NULL,
FOREIGN KEY (eId) REFERENCES enquete(eId));

"""
    )
    connexion.commit()
    connexion.close()

def creer_table_enquete():
    connexion = sqlite3.connect(CHEMIN)
    cursor = connexion.cursor()
    cursor.execute(
        f"""
CREATE TABLE IF NOT EXISTS enquete (
eid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
nom TEXT NOT NULL,
lieu TEXT NOT NULL,
description TEXT,
dateOuverture DATETIME NOT NULL,
dateFermeture DATETIME ,
statut TEXT NOT NULL
);

"""
    )
    connexion.commit()
    connexion.close()

if __name__ == "__main__":
    tout_creer()
    # Ajouter un citoyen
    """citoyen1 = Citoyen(
        nom="Diallo",
        prenom="Hassan",
        nationalite="Belge",
        adresse="",
        date_naissance="2002-11-21"
    )
    citoyen1.ajouter_citoyen()"""

