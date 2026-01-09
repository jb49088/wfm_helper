import requests

from utils import (
    build_id_to_name_mapping,
    build_name_to_max_rank_mapping,
    determine_widths,
    display_listings,
    get_all_items,
)

STATUS_MAPPING = {"offline": "Offline", "online": "Online", "ingame": "In Game"}
RIGHT_ALLIGNED_COLUMNS = ("price", "rank", "quantity", "reputation")


def extract_item_listings(id_to_name):
    """Extract and process listings for a specific item."""
    r = requests.get("https://api.warframe.market/v2/orders/item/lohk")
    r.raise_for_status()

    item_listings = []

    for listing in r.json()["data"]:
        if listing["type"] == "sell":
            item_listings.append(
                {
                    "seller": listing.get("user", {}).get("ingameName", "Unknown"),
                    "reputation": listing.get("user", {}).get("reputation", 0),
                    "status": listing.get("user", {}).get("status", "offline"),
                    "item": id_to_name[listing.get("itemId", "")],
                    "itemId": listing.get("itemId", ""),
                    "price": listing.get("platinum", 0),
                    "rank": listing.get("rank"),
                    "quantity": listing.get("quantity", 1),
                    "updated": listing.get("updatedAt", ""),
                }
            )

    return item_listings


def sort_item_listings(listings, sort_by="price", order=None):
    """Sort listings with sane defaults."""
    default_orders = {
        "seller": "asc",
        "reputation": "desc",
        "status": "asc",
        "item": "asc",
        "price": "asc",
        "rank": "desc",
        "quantity": "desc",
        "created": "desc",
        "updated": "desc",
    }

    is_desc = (default_orders[sort_by] == "desc") if not order else (order == "desc")

    sorted_listings = list(
        sorted(
            listings,
            key=lambda listing: listing[sort_by]
            if listing[sort_by] is not None
            else float("-inf")
            if is_desc
            else float("inf"),
            reverse=is_desc,
        )
    )

    return (sorted_listings, sort_by, default_orders[sort_by] if not order else order)


def build_rows(listings, max_ranks, copy=True):
    """Build rows for table rendering."""
    data_rows = []
    for i, listing in enumerate(listings, start=1):
        row = {
            "#": str(i),
            "seller": listing["seller"],
            "status": STATUS_MAPPING[listing["status"]],
            "item": listing["item"],
            "price": f"{listing['price']}p",
            "rank": f"{listing['rank']}/{max_ranks[listing['item']]}"
            if listing["rank"] is not None
            else "",
            "quantity": str(listing["quantity"]),
            "reputation": str(listing["reputation"]),
            "updated": str(listing["updated"]),
        }
        if not copy:
            del row["#"]
        data_rows.append(row)

    return data_rows


def display_item_listings():
    all_items = get_all_items()
    id_to_name = build_id_to_name_mapping(all_items)
    max_ranks = build_name_to_max_rank_mapping(all_items, id_to_name)
    item_listings = extract_item_listings(id_to_name)
    sorted_item_listings, sort_by, order = sort_item_listings(item_listings)
    data_rows = build_rows(sorted_item_listings, max_ranks)
    column_widths = determine_widths(data_rows, sort_by)
    display_listings(data_rows, column_widths, RIGHT_ALLIGNED_COLUMNS, sort_by, order)


if __name__ == "__main__":
    display_item_listings()
