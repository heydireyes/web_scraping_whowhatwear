
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

url = "https://whowhatwear.com/"

page = requests.get(url)

if page.status_code == 200:
    doc = BeautifulSoup(page.text, "lxml")

    scraped_data = []

    for item in doc.select(".card__title a"):
        article_name = item.text.strip().replace("â", " ")

        
        time_tag = item.find_next("time")
        article_time = time_tag.get("datetime").strip() if time_tag else "N/A"

       
        article_time = article_time.replace(" +0000 UTC", "")

        try:
            parsed_time = datetime.strptime(article_time, "%Y-%m-%d %H:%M:%S")
            formatted_time = parsed_time.strftime("%B %d, %Y, %I:%M %p")
        except ValueError:
            formatted_time = "N/A"

        print(f"Article Name: {article_name}")
        print(f"Article Time: {formatted_time}")
        print()

        scraped_data.append((article_name, formatted_time))
        
    df = pd.DataFrame(scraped_data, columns=["Article Name", "Article Time"])
    df.to_excel("scraped_data.xlsx", index=False)

else:
    print("Failed to retrieve the page.")
