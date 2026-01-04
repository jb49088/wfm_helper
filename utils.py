import requests


def build_id_to_name_mapping() -> dict[str, str]:
    """Build id to name mapping dictionary."""
    r = requests.get("https://api.warframe.market/v2/items")
    r.raise_for_status()

    id_to_name = {}

    id_to_name = {item["id"]: item["i18n"]["en"]["name"] for item in r.json()["data"]}

    return id_to_name
