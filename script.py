import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.safari.options import Options

FIELDNAMES = [
    "position",
    "team",
    "points",
    "played",
    "won",
    "nul",
    "lost",
    "withdrawn",
    "goals_for",
    "goals_against",
    "pe",
    "diff",
]

safari_options = Options()
driver = None

try:
    print("start de  Safari: ")
    driver = webdriver.Safari(options=safari_options)
    driver.maximize_window()

    url = "https://normandie.fff.fr/competitions?tab=ranking&id=438497&phase=1&poule=1&type=ch"
    # print(f"Acces à l'URL : {url}")
    driver.get(url)

    time.sleep(4)

    page_content = driver.page_source

    soup = BeautifulSoup(page_content, "html.parser")
    table = soup.find("table")

    if table:
        headers = [header.text for header in table.find_all("th")]
        print("Headers:", headers)

        rows = table.find_all("tr")[1:]
        data = []

        for row in rows:
            columns = row.find_all("td")  # get  toute les balises "td" dans row
            if len(columns) == 12:
                team_data = {
                    "position": columns[0].text.strip(),
                    "team": columns[1].text.strip(),
                    "points": columns[2].text.strip(),
                    "played": columns[3].text.strip(),
                    "won": columns[4].text.strip(),
                    "nul": columns[5].text.strip(),
                    "lost": columns[6].text.strip(),
                    "withdrawn": columns[7].text.strip(),
                    "goals_for": columns[8].text.strip(),
                    "goals_against": columns[9].text.strip(),
                    "pe": columns[10].text.strip(),
                    "diff": columns[11].text.strip(),
                }
                data.append(team_data)
                print(f"voici la ligne {team_data}")
            else:
                print("ligne ignoree (pas assez de colonnes)")

        with open("classement.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

            writer.writerows(data)

        print(f"\nSucces ! {len(data)} lignes enregistrees dans 'classement.csv'.")

    else:
        # Ce 'else' est maintenant correctement rattaché au 'if table:'
        print("Tableau de classement non trouve sur la page.")

except WebDriverException as e:
    print(f"ERREUR SELENIUM")
    print(f"Détail : {e}")
except Exception as e:
    print(f"ERREUR : {e}")

finally:
    if driver:
        print("Fermeture du navigateur.")
driver.quit()
