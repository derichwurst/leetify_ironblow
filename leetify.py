import requests

leetifiy_key = "48d2c42a-73bb-4298-81e8-7314d3616cf3"

class LeetifyAPIClient:
    """
    Client zur Interaktion mit der öffentlichen Leetify CS API.
    """
    BASE_URL = "https://api-public.cs-prod.leetify.com/v3/profile?id=76561197983756284"

    def __init__(self):
        """
        Initialisiert den Client mit dem API-Key.

        :param api_key: Der Leetify API-Schlüssel.
        """
        # Der API-Key wird im Header '_leetify_key' übergeben
        self.headers = {
            '_leetify_key': leetifiy_key,
            'Accept': 'application/json'
        }

    def _make_request(self, endpoint, params=None):
        """
        Interne Methode zur Durchführung einer GET-Anfrage an die API.

        :param endpoint: Der spezifische API-Endpunkt (z.B. '/profile').
        :param params: Optional: Dictionary mit URL-Parametern.
        :return: Das JSON-Ergebnis oder None bei Fehler.
        """
        url = f"{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # Löst einen Fehler für 4xx/5xx Statuscodes aus
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP-Fehler beim Endpunkt {endpoint}: {e}")
            print(f"Antworttext: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Verbindungsfehler beim Endpunkt {endpoint}: {e}")
            return None

    ## --- WICHTIGE FUNKTIONEN ---

    def get_player_profile(self, steam_id):
        """
        Ruft das Basisprofil eines Spielers ab (Name, Avatar, Grund-Info).

        :param steam_id: Die Steam-ID des Spielers.
        :return: Profil-Daten als Dictionary.
        """
        endpoint = f"https://api-public.cs-prod.leetify.com/v3/profile?id=" + str(steam_id)
        print(f"Rufe Profil für Steam ID {steam_id} ab...")
        return self._make_request(endpoint)



