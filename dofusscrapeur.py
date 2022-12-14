import os
import time
import logging
import pathlib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

class DofusScrapeur():

    def __init__(self) -> None:
        """
        Initialisation Dofus Scrapeur with selenium
        """
        self.url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/ressources'
        self.firefox = webdriver.Firefox()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def run(self):
        L = []
        self.firefox.get(self.url)
        self.firefox.find_element(by=By.CSS_SELECTOR,value="button[class='btn btn-primary btn-lg ak-accept']").click()
        self.firefox.find_elements(by=By.CSS_SELECTOR, value="select[class='ak-triggeraction'] option")[2].click()
        for i in range(30):
            try:
                time.sleep(5)
                url = f'https://www.dofus.com/fr/mmorpg/encyclopedie/ressources?size=96&page={i+1}'
                self.firefox.get(url)
                df = pd.read_html(self.firefox.find_element(by=By.CSS_SELECTOR, value="table[class='ak-table ak-responsivetable']").get_attribute(
                'outerHTML'))[0]
                df = df[['Nom', 'Type', 'Niveau']]
                df.Nom = df.Nom.str.split('{').str[0]
                L.append(df)
                self.logger.info(f'Done {url}')
            except Exception as e:
                self.logger.exception(e)
        pd.concat(L).to_csv(pathlib.Path(os.path.dirname(os.path.abspath(__file__))).joinpath('items.csv'))

if __name__ =='__main__':
    scrapeur = DofusScrapeur()
    scrapeur.run()