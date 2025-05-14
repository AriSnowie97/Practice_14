import json
import os
from typing import Dict, List, Any, Optional

def save_data(filename: str, data: Any) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to file '{filename}'")
    except Exception as e:
        print(f"Error saving to file '{filename}': {e}")

def load_data(filename: str) -> Optional[Any]:
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist. Returning empty data.")
        return {}  

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Data successfully loaded from file '{filename}'")
        return data
    except Exception as e:
        print(f"Error loading from file '{filename}': {e}")
        return None

# Task 1: Saving Game Results
def save_game_results(filename: str, player: str, result: Dict[str, int]) -> None:
    data = load_data(filename) or {}  # Load existing data or create a new dictionary
    if not isinstance(data, dict):
        print(f"Previous data in file '{filename}' has the wrong format. Overwriting.")
        data = {}

    if player in data:
        # Update existing player statistics
        for key, value in result.items():
            data[player][key] = data[player].get(key, 0) + value
    else:
        # Add new player with their statistics
        data[player] = result

    save_data(filename, data)

# Task 2: Contacts in JSON
def save_contacts(filename: str, contacts: Dict[str, Dict[str, str]]) -> None:
    save_data(filename, contacts)

def load_contacts(filename: str) -> Dict[str, Dict[str, str]]:
    data = load_data(filename)
    if data is None:
        return {}  # Return an empty dictionary in case of error or missing file
    return data

# Task 3: Dynamic Database (simplified, without MongoDB)
#  Warning: This is a simplified version using an in-memory dictionary and a JSON file.
#  For a full-fledged database, it's recommended to use a DBMS like MongoDB.
class ClientDatabase:
    def __init__(self, filename: str):
        self.filename = filename
        self.clients = load_data(filename) or {}  # Load existing data or create a new dictionary
        if not isinstance(self.clients, dict):
            print(f"Previous data in file '{filename}' has the wrong format. Creating a new database.")
            self.clients = {}

    def save_changes(self) -> None:
        save_data(self.filename, self.clients)

    def add_client(self, client_id: str, client_data: Dict[str, Any]) -> None:
        if client_id in self.clients:
            raise ValueError(f"Client with ID '{client_id}' already exists.")
        self.clients[client_id] = client_data
        self.save_changes()
        print(f"Client with ID '{client_id}' added.")

    def find_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        if client_id in self.clients:
            print(f"Found client with ID '{client_id}': {self.clients[client_id]}")
            return self.clients[client_id]
        else:
            print(f"Client with ID '{client_id}' not found.")
            return None

    def update_client(self, client_id: str, new_data: Dict[str, Any]) -> None:
        if client_id not in self.clients:
            raise ValueError(f"Client with ID '{client_id}' does not exist.")
        self.clients[client_id].update(new_data)  # Update only the provided fields
        self.save_changes()
        print(f"Client data with ID '{client_id}' updated.")

    def delete_client(self, client_id: str) -> None:
        if client_id not in self.clients:
            raise ValueError(f"Client with ID '{client_id}' does not exist.")
        del self.clients[client_id]
        self.save_changes()
        print(f"Client with ID '{client_id}' deleted.")

    def get_all_clients(self) -> Dict[str, Dict[str, Any]]:
        return self.clients

if __name__ == '__main__':
    # Task 1: Saving Game Results
    results_file = "game_results.json"
    save_game_results(results_file, "Player1", {'wins': 3, 'losses': 1})
    save_game_results(results_file, "Player2", {'wins': 2, 'losses': 2, 'draws': 1})
    save_game_results(results_file, "Player1", {'wins': 1, 'losses': 0})  # Update existing player
    print(f"Game results data saved to '{results_file}'")

    # Task 2: Contacts in JSON
    contacts_file = "contacts.json"
    my_contacts = {
        "John": {"phone": "+380123456789", "email": "john@example.com"},
        "Mary": {"phone": "+380987654321", "email": "mary@example.com"}
    }
    save_contacts(contacts_file, my_contacts)
    loaded_contacts = load_contacts(contacts_file)
    print(f"Loaded contacts from '{contacts_file}': {loaded_contacts}")

    # Task 3: Dynamic Database
    database_file = "clients.json"
    clients_db = ClientDatabase(database_file)

    clients_db.add_client("123", {"name": "John", "age": 30, "city": "Kyiv"})
    clients_db.add_client("456", {"name": "Mary", "age": 25, "city": "Lviv"})
    clients_db.add_client("789", {"name": "Peter", "age": 40, "city": "Odesa"})

    found_client = clients_db.find_client("456")
    print(f"Found client: {found_client}")

    clients_db.update_client("456", {"age": 26, "email": "mary@newmail.com"})
    found_client = clients_db.find_client("456")
    print(f"Client after update: {found_client}")

    clients_db.delete_client("123")
    found_client = clients_db.find_client("123")  # Check deletion
    print(f"Client after deletion: {found_client}")

    all_clients = clients_db.get_all_clients()
    print(f"All clients: {all_clients}")
