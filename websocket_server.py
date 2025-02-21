import asyncio
import json
import websockets
from game_logic import load_game_data

connected_clients = set()

async def notify_clients():
    """
    Invia aggiornamenti ai client WebSocket ogni 2 secondi.
    """
    while True:
        if connected_clients:
            try:
                game_data = load_game_data()
                data = {
                    "numero_estratto": game_data["drawn_numbers"][-1] if game_data["drawn_numbers"] else None,
                    "game_status": {
                        "cartelle_vendute": sum(len(p) for p in game_data["players"].values()),
                        "jackpot": len(game_data["players"]) * 1,  # 1 TON per cartella
                        "giocatori_attivi": len(game_data["players"])
                    }
                }
                message = json.dumps(data)
                
                # Invia il messaggio a tutti i client connessi
                await asyncio.gather(*[client.send(message) for client in connected_clients if not client.closed])
            except Exception as e:
                print(f"Errore nell'aggiornamento WebSocket: {e}")
        
        await asyncio.sleep(2)  # Aggiorna ogni 2 secondi

async def handler(websocket, path):
    """
    Gestisce la connessione WebSocket con la WebApp.
    """
    connected_clients.add(websocket)
    try:
        async for _ in websocket:
            pass  # Mantiene la connessione attiva
    except Exception as e:
        print(f"Errore WebSocket: {e}")
    finally:
        connected_clients.remove(websocket)

async def start_server():
    async with websockets.serve(handler, "0.0.0.0", 8002):
        print("✅ WebSocket Server avviato su ws://0.0.0.0:8002/ws")
        await notify_clients()

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except Exception as e:
        print(f"Errore nell'avvio del WebSocket Server: {e}")
