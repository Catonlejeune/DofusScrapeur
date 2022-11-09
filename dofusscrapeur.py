import os
import time
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

    def run(self):
        L = []
        self.firefox.get(self.url)
        self.firefox.find_element(by=By.CSS_SELECTOR,value="button[class='btn btn-primary btn-lg ak-accept']").click()
        self.firefox.find_elements(by=By.CSS_SELECTOR, value="select[class='ak-triggeraction'] option")[2].click()
        for i in range(30):
            time.sleep(5)
            url = f'https://www.dofus.com/fr/mmorpg/encyclopedie/ressources?size=96&page={i+1}'
            self.firefox.get(url)
            df = pd.read_html(self.firefox.find_element(by=By.CSS_SELECTOR, value="table[class='ak-table ak-responsivetable']").get_attribute(
            'outerHTML'))[0]
            df = df[['Nom', 'Type', 'Niveau']]
            df.Nom = df.Nom.str.split('{').str[0]
            L.append(df)
        pd.concat(L).to_csv(pathlib.Path(os.path.dirname(os.path.abspath(__file__))).joinpath('items.csv'))

if __name__ =='__main__':
    scrapeur = DofusScrapeur()
    scrapeur.run()