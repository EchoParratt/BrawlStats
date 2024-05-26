from flask import Flask, request, jsonify
from flask_cors import CORS
import brawlstats
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# The backend is initialized with Flask and Flask-CORS to handle cross-origin requests
app = Flask(__name__) 
CORS(app)

# A client instance is created to interact with the Brawl Stars API
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjE3YWQzYjMyLTY1ZDYtNGQxYS04YjU1LTZhMmUwN2IzMTEzYiIsImlhdCI6MTcxNjA3MDMwMCwic3ViIjoiZGV2ZWxvcGVyL2JhZDg3OWQyLTVhYmMtOWEyZi1jNzk4LTA5YWRlNzMwMDhkNyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNzAuNjYuMTU3LjEzNSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.YldRTfEFDJbGX3KJ0LDCFIxDjLlyrO0yR0hbLvOA7PWUBwRPEP6H2IqVv_cSC_k2rW9Daq1H7TdS3sHk59NPpg'
client = brawlstats.Client(token, is_async=False)

# Analyzes battle logs to calculate win rate, win count, loss count, and total battles
def analyze_battle_logs(battle_logs):
    win_count = 0
    loss_count = 0
    total_battles = 0

    print("Total Battle Logs Fetched:", len(battle_logs))  # Debugging output

    for battle in battle_logs:
        trophy_change = battle.battle.get('trophy_change', None)
        if trophy_change is not None:  # Check if trophyChange is present
            total_battles += 1
            if trophy_change > 0:
                win_count += 1
            elif trophy_change < 0:
                loss_count += 1
        
    if total_battles > 0:
        win_rate = (win_count / total_battles) * 100
    else:
        win_rate = 0

    return win_rate, win_count, loss_count, total_battles

# Processes battle logs to calculate trophy changes and starting trophies:
def process_battle_logs(battle_logs, current_trophies):
    trophy_changes = []

    for battle in battle_logs:
        trophy_change = battle.battle.get('trophy_change', 0) 
        trophy_changes.append(trophy_change)

    total_trophy_change = sum(trophy_changes)
    starting_trophies = current_trophies - total_trophy_change

    return trophy_changes, starting_trophies

# Finds the most played brawler by the player
def find_most_played_brawler(battle_logs,player_tag):
    brawler_count = {}

    for battle in battle_logs:
        for team in battle.battle.get('teams', []):
            for player in team:
                if player.get('tag') == player_tag:
                    brawler_name = player.get('brawler', {}).get('name', None)
                    print(brawler_name)
                    if brawler_name:
                        if brawler_name in brawler_count:
                            brawler_count[brawler_name] += 1
                        else:
                            brawler_count[brawler_name] = 1

    most_played_brawler = max(brawler_count, key=brawler_count.get, default=None)
    most_played_count = brawler_count.get(most_played_brawler, 0)


    return most_played_brawler, most_played_count

# Finds the brawler with the highest win ratio for the player
def find_brawler_with_highest_win_ratio(battle_logs, player_tag):
    brawler_stats = {}

    for battle in battle_logs:
        if 'battle' in battle and 'teams' in battle['battle']:
            for team in battle['battle']['teams']:
                for player in team:
                    if player.get('tag') == player_tag:
                        brawler_name = player.get('brawler', {}).get('name', None)
                        result = battle['battle'].get('result', None)
                        if brawler_name:
                            if brawler_name not in brawler_stats:
                                brawler_stats[brawler_name] = {'wins': 0, 'games': 0}
                            
                            brawler_stats[brawler_name]['games'] += 1
                            if result == 'victory':
                                brawler_stats[brawler_name]['wins'] += 1

    # Calculate win ratios and find the brawler with the highest win ratio
    highest_wins = 0
    brawler_with_highest_win_ratio = None
    for brawler, stats in brawler_stats.items():
        print(brawler)
        if stats['games'] > 0:
            win_ratio = stats['wins'] 
            if win_ratio > highest_wins:
                highest_wins = win_ratio
                brawler_with_highest_win_ratio = brawler

    return brawler_with_highest_win_ratio, highest_wins

# These functions use Selenium to scrape data from the Brawl Time Ninja website

# Fetches the top 9 brawlers by win rate
def get_top_brawler():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = 'https://brawltime.ninja/tier-list/brawler'
    driver.get(url)

    html = driver.page_source
    driver.quit()

    tables = pd.read_html(html)

    if tables:
        df = tables[0]  
        top_nine_brawlers = df.head(9)
        top_brawlers_info = [
        {"name": row['Brawler'], "winRate": row['Adjusted Win Rate']}
        for index, row in top_nine_brawlers.iterrows()
        ]
        return top_brawlers_info
    else:
        return "No tables found"

# The below 6 functions fetch the best current brawler for each game mode based off win-rate

def brawl_ball():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = 'https://brawltime.ninja/tier-list/mode/brawl-ball'
    driver.get(url)

    html = driver.page_source
    driver.quit()

    tables = pd.read_html(html)
    df = tables[0]
    bb_brawler = df.head(1)
    for index, row in bb_brawler.iterrows():
        return f"{row['Brawler']}"

def knockout():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = 'https://brawltime.ninja/tier-list/mode/knockout'
    driver.get(url)

    html = driver.page_source
    driver.quit()

    tables = pd.read_html(html)
    df = tables[0]
    k_brawler = df.head(1)
    for index, row in k_brawler.iterrows():
        return f"{row['Brawler']}"

def gem_grab():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = 'https://brawltime.ninja/tier-list/mode/gem-grab'
    driver.get(url)

    html = driver.page_source
    driver.quit()

    tables = pd.read_html(html)
    df = tables[0]
    gg_brawler = df.head(1)
    for index, row in gg_brawler.iterrows():
        return f"{row['Brawler']}"

def hot_zone():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = 'https://brawltime.ninja/tier-list/mode/hot-zone'
    driver.get(url)

    html = driver.page_source
    driver.quit()

    tables = pd.read_html(html)
    df = tables[0]
    hz_brawler = df.head(1)
    for index, row in hz_brawler.iterrows():
        return f"{row['Brawler']}"

def wipeout():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = 'https://brawltime.ninja/tier-list/mode/wipeout'
    driver.get(url)

    html = driver.page_source
    driver.quit()

    tables = pd.read_html(html)
    df = tables[0]
    w_brawler = df.head(1)
    for index, row in w_brawler.iterrows():
        return f"{row['Brawler']}"

def showdown():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = 'https://brawltime.ninja/tier-list/mode/solo-showdown'
    driver.get(url)

    html = driver.page_source
    driver.quit()

    tables = pd.read_html(html)
    df = tables[0]
    s_brawler = df.head(1)
    for index, row in s_brawler.iterrows():
        return f"{row['Brawler']}"

# Flask Route
# Defines the endpoint to fetch player data and analyze battle logs

@app.route('/player/<player_tag>', methods=['GET']) # Defines the URL path for the endpoint
# This function is called when a request is made to the /player/<player_tag> endpoint
def get_player_data(player_tag):    
    try:
        player = client.get_player(player_tag)
        battle_logs = client.get_battle_logs(player_tag)
        win_rate, win_count, loss_count, total_battles = analyze_battle_logs(battle_logs)
        most_played_brawler, most_played_count = find_most_played_brawler(battle_logs, player_tag)
        brawler, wins = find_brawler_with_highest_win_ratio(battle_logs, player_tag)
        top_stars = get_top_brawler()
        trophy_changes, starting_trophies = process_battle_logs(battle_logs,player.trophies)
        bb_brawler = brawl_ball()
        k_brawler = knockout()
        gg_brawler = gem_grab()
        w_brawler = wipeout()
        hz_brawler = hot_zone()
        s_brawler = showdown()


        return jsonify({
            "name": player.name,
            "trophies": player.trophies,
            "club": player.club.name,
            "win_rate": f"{win_rate:.2f}%",
            "most_played_brawler": most_played_brawler,
            "most_played_count": most_played_count,
            "highest_win_ratio_brawler": brawler,
            "highest_wins": wins,
            "top_9_brawlers" : top_stars,
            "trophy_changes": trophy_changes,
            "starting_trophies": starting_trophies,
            "bb_brawler": bb_brawler,
            "k_brawler": k_brawler,
            "gg_brawler": gg_brawler,
            "w_brawler": w_brawler,
            "hz_brawler": hz_brawler,
            "s_brawler": s_brawler




        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

