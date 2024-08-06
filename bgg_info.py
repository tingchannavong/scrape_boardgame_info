#A program to request for public board game information from BGG
import requests
import xml.etree.ElementTree as ET

def get_board_game_info(board_game):
    url = f'https://www.boardgamegeek.com/xmlapi/search?search={board_game}&exact=1'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the response XML
        root = ET.fromstring(response.content)
        
        # Get the first search result (assuming it's the most relevant)
        boardgame = root.find('.//boardgame')
        if boardgame is None:
            print(f"No information found for {board_game}.")
            return None
        
        game_id = boardgame.attrib.get('objectid')
        if not game_id:
            print(f"No game ID found for {board_game}.")
            return None
        
        # Use the game ID to fetch detailed information
        url = f'https://www.boardgamegeek.com/xmlapi/boardgame/{game_id}?stats=1'
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the response XML
        root = ET.fromstring(response.content)
        
        # Extract the desired information
        playing_time_elem = root.find('.//playingtime')
        playing_time = playing_time_elem.text if playing_time_elem is not None else "Not specified"
        
        min_players_elem = root.find('.//minplayers')
        min_players = min_players_elem.text if min_players_elem is not None else "Not specified"
        
        max_players_elem = root.find('.//maxplayers')
        max_players = max_players_elem.text if max_players_elem is not None else "Not specified"
        
        min_age_elem = root.find('.//minage')
        min_age = min_age_elem.text if min_age_elem is not None else "Not specified"
        
        categories_elems = root.findall('.//boardgamecategory')
        categories = ', '.join(category.text for category in categories_elems) if categories_elems else "Not specified"
        
        return {
            'Playing Time': playing_time,
            'Minimum Players': min_players,
            'Maximum Players': max_players,
            'Minimum Age': min_age,
            'Categories': categories
        }
    except Exception as e:
        print(f"Error fetching information for {board_game}: {e}")
        return None

def main():
    board_games = ['Catan', 'Ticket to Ride', 'Codenames']  # List of board games to fetch information for
    
    for game in board_games:
        game_info = get_board_game_info(game)
        if game_info:
            print(f"Information for {game}:")
            for key, value in game_info.items():
                print(f"{key}: {value}")
            print()

if __name__ == "__main__":
    main()
