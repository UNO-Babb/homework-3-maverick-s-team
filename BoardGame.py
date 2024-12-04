from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Initialize game state
game_state = {
    "players": [
        {"name": "Red", "position": 0, "color": "red"},
        {"name": "Blue", "position": 0, "color": "blue"}
    ],
    "current_player_index": 0,
    "winner": None
}
 
# Game rules
SPECIAL_SPOTS = [5, 10, 15]
WINNING_SPOT = 19

@app.route('/')
def index():
    return render_template('index.html', game_state=game_state)

@app.route('/roll', methods=['POST'])
def roll():
    if game_state["winner"] is not None:
        return jsonify({"winner": game_state["winner"]})

    # Roll dice and move current player
    roll_value = random.randint(1, 6)
    current_player = game_state["players"][game_state["current_player_index"]]
    other_player = game_state["players"][(game_state["current_player_index"] + 1) % 2]

    # Calculate new position
    new_position = current_player["position"] + roll_value

    # Check if the player reaches or surpasses the winning spot
    if new_position >= WINNING_SPOT:
        new_position = WINNING_SPOT
        game_state["winner"] = current_player["name"]

    # Check if the player lands on a special spot (5, 10, or 15) and reset to start
    elif new_position in SPECIAL_SPOTS:
        new_position = 0

    # Check if the player lands on the same spot as the other player
    elif new_position == other_player["position"]:
        new_position = 0

    # Update player position
    current_player["position"] = new_position

    # Move to the next player
    game_state["current_player_index"] = (game_state["current_player_index"] + 1) % len(game_state["players"])

    return jsonify({
        "roll_value": roll_value,
        "new_position": new_position,
        "current_player": current_player["name"],
        "winner": game_state["winner"]
    })

if __name__ == '__main__':
    app.run(debug=True)
