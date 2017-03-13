import urllib
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os.path

urls = ["http://www.bbc.co.uk/sport/football/scottish-championship/table?print=true",
        "http://www.bbc.co.uk/sport/football/scottish-league-one/table?print=true",
        "http://www.bbc.co.uk/sport/football/scottish-league-two/table?print=true"]

date = str(datetime.now().strftime("%Y%m%d-%H%M"))

current_url = 0

for url in urls:
    #print current_url
    html = urllib.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    column_headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

    data_rows = soup.findAll('tr')[2:12]
    team_data = [[td.getText() for td in data_rows[i].findAll('td')] for i in range(len(data_rows))]

    df = pd.DataFrame(team_data, columns=column_headers)

    # Drop unnecessary columns
    df = df.drop('Last 10 games results', 1)
    df = df.drop('Match status', 1)
    df = df.drop(df.columns[[0]], axis=1)

    # Replace unnecessary strings with simple integers
    for x in range(0,10):
        df['Position'][x] = x + 1

    # Pick a filename depending on the URL we're scraping
    if current_url == 0:
        filename = "tables/championship_%s.html" % (date)
    elif current_url == 1:
        filename = "tables/league-one_%s.html" % (date)
    elif current_url == 2:
        filename = "tables/league-two_%s.html" % (date)

    # Return HTML table
    df.to_html(filename, index=False)

    if current_url == 0:
        filename = "tables/championship.html"
    elif current_url == 1:
        filename = "tables/league-one.html"
    elif current_url == 2:
        filename = "tables/league-two.html"

    if os.path.exists(filename):
        os.remove(filename)

    df.to_html(filename, index=False)

    current_url += 1
