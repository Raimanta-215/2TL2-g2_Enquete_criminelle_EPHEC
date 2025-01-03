from db.db import tout_creer
from interf.pages import PoliceApp
import logging
import os

LOG_PATH = os.path.abspath('logs/police.log')
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',

    )
    logger.info('Starting Police App')

    try:
        logger.info('Creation de la base de donnée..')
        tout_creer()
        logger.info('Base de donnée crée avec succès')
    except Exception as ex:
        logger.error(ex)
        return

    try:
        logger.info('lancement de l\'interface')
        app = PoliceApp()
        app.run()
        logger.info('application lancée avec succès')
    except Exception as ex:
        logger.critical(f"appli pas lancée {ex}", exc_info=True)

    logger.info('Finishing Police App')

if __name__ == '__main__':
    main()