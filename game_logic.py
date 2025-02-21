import random
import json
import os

# Percorso del file per salvare lo stato del gioco
game_data_file = "data/game_data.json"

# Funzione per caricare lo stato del gioco
def load_game_data():
    if not os.path.exists(game_data_file):
        save_game_data({"players": {}, "drawn_numbers": [], "game_active": False})
    with open(game_data_file, "r") as file:
        return json.load(file)

# Funzione per salvare lo stato del gioco
def save_game_data(data):
    with open(game_data_file, "w") as file:
        json.dump(data, file, indent=4)

# Funzione per avviare una nuova partita
def start_game():
    game_data = {"players": {}, "drawn_numbers": [], "game_active": True}
    save_game_data(game_data)
    return "🎲 La partita di Bingo è iniziata! Acquista le cartelle con /buy."

# Funzione per acquistare una cartella di gioco
def buy_ticket(user_id, num_cartelle=1):
    game_data = load_game_data()

    if not game_data["game_active"]:
        return "❌ Nessuna partita in corso. Aspetta l'inizio della prossima partita."

    if user_id not in game_data["players"]:
        game_data["players"][user_id] = []

    # Limita il numero massimo di cartelle acquistabili
    max_cartelle = 24
    if len(game_data["players"][user_id]) + num_cartelle > max_cartelle:
        return f"❌ Puoi acquistare al massimo {max_cartelle} cartelle."

    # Aggiunge nuove cartelle
    nuove_cartelle = [generate_bingo_card() for _ in range(num_cartelle)]
    game_data["players"][user_id].extend(nuove_cartelle)

    save_game_data(game_data)

    # Format output: mostra tutte le cartelle acquistate
    cartelle_testo = "\n\n".join(
        [f"📜 Cartella {i+1}:\n{format_bingo_card(cartella)}"
        for i, cartella in enumerate(nuove_cartelle)]
    )

    return f"✅ Hai acquistato {num_cartelle} cartelle!\n\n{cartelle_testo}"


    # Limita il numero massimo di cartelle acquistabili
    max_cartelle = 24  # Puoi cambiarlo se serve
    if len(game_data["players"][user_id]) + num_cartelle > max_cartelle:
        return f"❌ Puoi acquistare al massimo {max_cartelle} cartelle."

    # Aggiunge nuove cartelle al giocatore
    game_data["players"][user_id].extend([generate_bingo_card() for _ in range(num_cartelle)])

    save_game_data(game_data)
    return f"✅ Hai acquistato {num_cartelle} cartelle!\nEcco la tua prima cartella:\n{format_bingo_card(game_data['players'][user_id][0])}"


# Funzione per formattare la cartella di Bingo in output leggibile
def format_bingo_card(card):
    return "\n".join([" | ".join(str(num) if num != 0 else "  " for num in row) for row in card])

# Funzione per generare una cartella di Bingo 90
def generate_bingo_card():
    card = [[0] * 9 for _ in range(3)]  # Inizializza una griglia 3x9 con zeri
    columns = [list(range(i * 10 + 1, i * 10 + 11)) for i in range(9)]
    for col in columns:
        random.shuffle(col)
    
    filled_positions = set()
    for row in range(3):
        while len(filled_positions) < (5 * (row + 1)):
            col = random.randint(0, 8)
            if (row, col) not in filled_positions:
                card[row][col] = columns[col].pop()
                filled_positions.add((row, col))
    
    return card

# Funzione per estrarre un numero casuale
def draw_number():
    game_data = load_game_data()
    
    if not game_data["game_active"]:
        return "❌ Nessuna partita attiva. Usa /start_game per iniziare."
    
    if len(game_data["drawn_numbers"]) >= 90:
        game_data["game_active"] = False
        save_game_data(game_data)
        return "🎉 Il gioco è terminato! Tutti i numeri sono stati estratti."
    
    new_number = random.choice([n for n in range(1, 91) if n not in game_data["drawn_numbers"]])
    game_data["drawn_numbers"].append(new_number)
    save_game_data(game_data)
    
    check_winners(game_data)
    return f"🔢 Numero estratto: {new_number}"

# Funzione per controllare vincite
def check_winners(game_data):
    winners_cinquina = []
    winners_bingo = []
    
    for user_id, card in game_data["players"].items():
        if check_cinquina(card, game_data["drawn_numbers"]):
            winners_cinquina.append(user_id)
        if check_bingo(card, game_data["drawn_numbers"]):
            winners_bingo.append(user_id)
    
    for winner in winners_cinquina:
        print(f"🏆 {winner} ha fatto Cinquina!")
    
    for winner in winners_bingo:
        print(f"🎉 {winner} ha fatto Bingo! La partita è terminata.")
        game_data["game_active"] = False
        save_game_data(game_data)

# Funzione per verificare la Cinquina
def check_cinquina(card, drawn_numbers):
    for row in card:
        if sum(1 for num in row if num in drawn_numbers) == 5:
            return True
    return False

# Funzione per verificare il Bingo
def check_bingo(card, drawn_numbers):
    return sum(1 for row in card for num in row if num in drawn_numbers) == 15

# Funzione per formattare la cartella di Bingo in output leggibile
def format_bingo_card(card):
    return "\n".join([" | ".join(str(num) if num != 0 else "  " for num in row) for row in card])

# Funzione per verificare il saldo dell'utente
def get_balance(user_id):
    return "10.0 TON"

# Funzione per prelevare le vincite
def withdraw_funds(user_id):
    return "✅ Prelievo completato. I fondi verranno trasferiti sul tuo wallet Telegram."

if __name__ == "__main__":
    print(start_game())
