import pyperclip
import requests

from utils import (
    build_id_to_name_mapping,
    build_name_to_max_rank_mapping,
    determine_widths,
    display_listings,
    get_all_items,
)

RIGHT_ALLIGNED_COLUMNS = ("price", "rank", "quantity")


def extract_user_listings(user, id_to_name):
    """Extract and process listings for a specific user."""
    r = requests.get(f"https://api.warframe.market/v2/orders/user/{user.lower()}")
    r.raise_for_status()

    user_listings = []

    for listing in r.json()["data"]:
        if listing["type"] == "sell":
            user_listings.append(
                {
                    "item": id_to_name[listing.get("itemId", "")],
                    "itemId": listing.get("itemId", ""),
                    "price": listing.get("platinum", 0),
                    "rank": listing.get("rank"),
                    "quantity": listing.get("quantity", 1),
                    "updated": listing.get("updatedAt", ""),
                }
            )

    return user_listings


def sort_user_listings(listings, sort_by="updated", order=None):
    """Sort listings with sane defaults."""
    default_orders = {
        "item": "asc",
        "price": "desc",
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
            "item": listing["item"],
            "price": f"{listing['price']}p",
            "rank": f"{listing['rank']}/{max_ranks[listing['item']]}"
            if listing["rank"] is not None
            else "",
            "quantity": str(listing["quantity"]),
            "updated": str(listing["updated"]),
        }
        if not copy:
            del row["#"]
        data_rows.append(row)

    return data_rows


def copy_listing(user, data_rows):
    listing = input("Listing to copy: ").strip()

    for row in data_rows:
        if row["#"] == listing:
            segments = [
                "WTB",
                f"{row['item']}",
                f"Rank: {row['rank']}" if row.get("rank") else "",
                f"Price: {row['price']}",
            ]
            segments = [s for s in segments if s]
            message = f"/w {user} {' | '.join(segments)}"
            pyperclip.copy(message)
            print(f"Copied to clipboard: {message}")
            return

    print(f"Listing {listing} not found")


def display_user_listings():
    """Main entry point."""
    args = {
        "user": "bhwsg",
        "copy": True,
    }
    all_items = get_all_items()
    id_to_name = build_id_to_name_mapping(all_items)
    max_ranks = build_name_to_max_rank_mapping(all_items, id_to_name)
    user_listings = extract_user_listings(args["user"], id_to_name)
    sorted_user_listings, sort_by, order = sort_user_listings(user_listings)
    data_rows = build_rows(sorted_user_listings, max_ranks, args["copy"])
    column_widths = determine_widths(data_rows, sort_by)
    display_listings(data_rows, column_widths, RIGHT_ALLIGNED_COLUMNS, sort_by, order)
    if args["copy"]:
        copy_listing(args["user"], data_rows)


if __name__ == "__main__":
    display_user_listings()
