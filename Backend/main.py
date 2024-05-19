from flask import Flask, request, jsonify
from flask_cors import CORS
import brawlstats
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
CORS(app)

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjE3YWQzYjMyLTY1ZDYtNGQxYS04YjU1LTZhMmUwN2IzMTEzYiIsImlhdCI6MTcxNjA3MDMwMCwic3ViIjoiZGV2ZWxvcGVyL2JhZDg3OWQyLTVhYmMtOWEyZi1jNzk4LTA5YWRlNzMwMDhkNyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNzAuNjYuMTU3LjEzNSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.YldRTfEFDJbGX3KJ0LDCFIxDjLlyrO0yR0hbLvOA7PWUBwRPEP6H2IqVv_cSC_k2rW9Daq1H7TdS3sHk59NPpg'
client = brawlstats.Client(token, is_async=False)


def analyze_battle_logs(battle_logs):
    win_count = 0
    loss_count = 0
    total_battles = 0

    print("Total Battle Logs Fetched:", len(battle_logs))  # Debugging output

    for battle in battle_logs:
        # Use the .get() method to avoid KeyError if 'trophyChange' does not exist
        trophy_change = battle.battle.get('trophy_change', None)
        if trophy_change is not None:  # Check if trophyChange is present
            total_battles += 1
            if trophy_change > 0:
                win_count += 1
            elif trophy_change < 0:
                loss_count += 1
        #else:
            #print("No trophyChange in this battle:", battle)  # Print the battle log for inspection

    if total_battles > 0:
        win_rate = (win_count / total_battles) * 100
    else:
        win_rate = 0

    return win_rate, win_count, loss_count, total_battles

def process_battle_logs(battle_logs, current_trophies):
    trophy_changes = []

    for battle in battle_logs:
        trophy_change = battle.battle.get('trophy_change', 0)  # Assuming 'trophyChange' is the key for trophy gain/loss
        trophy_changes.append(trophy_change)

    total_trophy_change = sum(trophy_changes)
    starting_trophies = current_trophies - total_trophy_change

    return trophy_changes, starting_trophies

def find_most_played_brawler(battle_logs,player_tag):
    brawler_count = {}

    for battle in battle_logs:
        #print(battle)
        for team in battle.battle.get('teams', []):
            #print(team)
            for player in team:
                #print(player.get('tag'))
                #print(player.get('tag'))
                #print(player_tag)
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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
        df = tables[0]  # Assume the first table is the correct one
        top_eight_brawlers = df.head(8)
        top_brawlers_info = [
        {"name": row['Brawler'], "winRate": row['Adjusted Win Rate']}
        for index, row in top_eight_brawlers.iterrows()
        ]
        return top_brawlers_info
    else:
        return "No tables found"



@app.route('/player/<player_tag>', methods=['GET'])
def get_player_data(player_tag):
    try:
        player = client.get_player(player_tag)
        battle_logs = client.get_battle_logs(player_tag)
        win_rate, win_count, loss_count, total_battles = analyze_battle_logs(battle_logs)
        most_played_brawler, most_played_count = find_most_played_brawler(battle_logs, player_tag)
        brawler, wins = find_brawler_with_highest_win_ratio(battle_logs, player_tag)
        top_stars = get_top_brawler()
        trophy_changes, starting_trophies = process_battle_logs(battle_logs,player.trophies)

        return jsonify({
            "name": player.name,
            "trophies": player.trophies,
            "club": player.club.name,
            "win_rate": f"{win_rate:.2f}%",
            "most_played_brawler": most_played_brawler,
            "most_played_count": most_played_count,
            "highest_win_ratio_brawler": brawler,
            "highest_wins": wins,
            "top_8_brawlers" : top_stars,
            "trophy_changes": trophy_changes,
            "starting_trophies": starting_trophies

        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

