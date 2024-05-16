import brawlstats

# Replace 'your_api_key_here' with your actual Brawl Stars API key
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZlMDhjZjFmLTM5ODEtNDVmYS1iNjU3LWQwYWQwYTg3YzEyMSIsImlhdCI6MTcxNTg0MTY1NCwic3ViIjoiZGV2ZWxvcGVyL2JhZDg3OWQyLTVhYmMtOWEyZi1jNzk4LTA5YWRlNzMwMDhkNyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNzAuNjYuMTU3LjEzNSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.-OWA7QtwsZ51JduTNJDlfGFCfJ1QwznHvGDnvxysW00eH27zAZzZgNbMbjQAfjCLQ-x1jYehFHuXUPPHsZzmpw'
client = brawlstats.Client(token, is_async=False)
rain_player_tag = '#2UJVL0CL'
player_tag = '#8J2Y2VCC'
eli_player_tag = '#Y0CL0VC'

#try:
    # Fetch player data using their tag
    #player = client.get_player(player_tag)
    #battle_log = client.get_battle_logs(player_tag)
    #print(player.name, player.trophies,player.club.name)
#finally:
    #client.close()

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
    highest_win_ratio = 0
    brawler_with_highest_win_ratio = None
    for brawler, stats in brawler_stats.items():
        print(brawler)
        if stats['games'] > 0:
            win_ratio = stats['wins'] / stats['games']
            if win_ratio > highest_win_ratio:
                highest_win_ratio = win_ratio
                brawler_with_highest_win_ratio = brawler

    return brawler_with_highest_win_ratio, highest_win_ratio

try:
    player = client.get_player(eli_player_tag)
    battle_logs = client.get_battle_logs(eli_player_tag)
    win_rate, win_count, loss_count, total_battles = analyze_battle_logs(battle_logs)
    most_played_brawler, most_played_count = find_most_played_brawler(battle_logs,eli_player_tag)
    brawler, win_ratio = find_brawler_with_highest_win_ratio(battle_logs,eli_player_tag)
    print(f"Name: {player.name}")
    print(f"Trophies: {player.trophies}")
    print(f"Club: {player.club.name}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Total Wins: {win_count}")
    print(f"Total Losses: {loss_count}")
    print(f"Total Battles affecting trophies: {total_battles}")
    print(f"Most Played Brawler: {most_played_brawler, most_played_count}")
    print(f"Brawler with highest win ratio: {brawler, win_ratio}")
finally:
    client.close()


