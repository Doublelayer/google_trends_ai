import json
import os

from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
from dotenv import load_dotenv

from database import save_trends, is_trend_exists
from logger_config import logger
from notifiyer import send

load_dotenv()


@browser(headless=True, output=None)
def scrape_html(driver: Driver, data):
    url_ = data["url"]
    logger.debug(f"now loading {url_}")
    driver.get(url_)

    page_soup = soupify(driver)

    trend_table = page_soup.find('div', id='trend-table')
    tr_elements = trend_table.find_all('tr') if trend_table else []

    trends = []

    for tr in tr_elements:
        tds = tr.find_all('td')
        if len(tds) > 1:
            all_divs = tds[1].find_all('div')
            # print(f"found: {all_divs[0].get_text()}")
            # driver.click_element_containing_text(all_divs[0].get_text())
            # page_soup = soupify(driver)
            # links = [x['href'] for x in
            #          page_soup.find(text="In den Nachrichten").find_parent().find_parent().find_all("a") if
            #          'href' in x.attrs]
            trend_ = all_divs[0].get_text()

            if not trend_ or is_trend_exists(trend_):
                continue

            trend_ = {
                "trend": all_divs[0].get_text() or "N/A",
                "search_volume": all_divs[1].get_text().split("·")[0].replace('\xa0', ' ') or "N/A",
                # "links": links
            }
            logger.debug(trend_)
            trends.append(trend_)

        if os.getenv("RUNNING_PROFILE") == "dev" and len(trends) >= 3:
            logger.debug(f"running profile is {os.getenv('RUNNING_PROFILE')} therefore 3 trends should be enough")
            return trends
    return trends


@browser(headless=True, output=None)
def scrape_from_perplexity(driver: Driver, data):
    trend_ = data["trend"]
    logger.info(f"start prompting for perplexity with trend: {trend_}")
    q = f"""
        Erstelle eine kurze Zusammenfassung aktueller Ereignisse und Nachrichten zum Thema '{data["trend"]}' mit maximal 150 Wörtern. 
        Die Zusammenfassung sollte prägnant und informativ sein und nur die relevantesten Informationen enthalten. 
        Verzichte auf Quellennachweise im Text. Deine Antwort soll als Code ausgegeben werden.
        
        Formatiere das Ergebnis als valides JSON mit folgenden Schlüsseln:
        1. "trend": Immer das exakte thema. => {data["trend"]}
        2. "summary": Die Zusammenfassung der aktuellen Ereignisse und Nachrichten
        3. "sources": Eine Liste von maximal drei absoluten URLs zu vertrauenswürdigen Quellen
        
        Stelle sicher, dass das JSON-Format korrekt ist, indem du Sonderzeichen und Zeilenumbrüche entsprechend escapest. Das Ergebnis sollte direkt mit Python gelesen werden können.
        
        Beispiel für das erwartete JSON-Format:
        {{
        "trend": "Beispiel-Trend",
        "summary": "Dies ist eine Beispiel-Zusammenfassung...",
        "sources": [
        "https://www.beispiel1.com",
        "https://www.beispiel2.com",
        "https://www.beispiel3.com"
        ]
        }}
    """
    url = f"https://www.perplexity.ai/?q={q}"
    driver.get(url)
    page_soup = soupify(driver)
    raw_ = page_soup.find("code").get_text()
    logger.debug(raw_)
    json_ = json.loads(raw_)
    json_["search_volume"] = data["search_volume"]
    json_["trend"] = data["trend"]
    return json_


def get_trends():
    trends = scrape_html({"url": "https://trends.google.de/trending?geo=DE&hours=24&sort=search-volume"})
    new_trends = []

    for trend in trends:
        _new_trend = scrape_from_perplexity(trend)
        logger.debug(_new_trend)
        new_trends.append(_new_trend)

    save_trends(new_trends)
    for trend in new_trends:
        send(trend)
