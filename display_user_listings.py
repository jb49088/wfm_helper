from utils import (
    build_id_to_name_mapping,
    extract_user_listings,
    get_all_items,
)


def build_rows(listings):
    """Build rows for table rendering."""
    data_rows = []
    for item, details in listings.items():
        row = {
            "item": item,
            "price": str(details["price"]),
            "rank": str(details["rank"]) if details["rank"] is not None else "N/A",
            "quantity": str(details["quantity"]),
            "updated": str(details["updated"]),
            "created": str(details["created"]),
        }
        data_rows.append(row)

    return data_rows


def determine_widths(data_rows):
    """Determine maximum width for each colunm."""
    column_widths = {
        "item": 0,
        "price": 0,
        "rank": 0,
        "quantity": 0,
        "updated": 0,
        "created": 0,
    }

    for row in data_rows:
        for key in row:
            column_widths[key] = max(column_widths[key], len(row[key]), len(key))

    # Account for spacing
    column_widths = {key: width + 2 for key, width in column_widths.items()}

    return column_widths


def display_listings(data_rows, column_widths):
    """Display listings in a sql-like table."""
    separator_row = ["-" * width for width in column_widths.values()]

    header_row = [key.title().center((width)) for key, width in column_widths.items()]

    print(f"+{'+'.join(separator_row)}+")
    print(f"|{'|'.join(header_row)}|")
    print(f"+{'+'.join(separator_row)}+")

    for row in data_rows:
        data_row = [
            (" " + value).ljust(column_widths[key]) for key, value in row.items()
        ]

        print(f"|{'|'.join(data_row)}|")

    print(f"+{'+'.join(separator_row)}+")


def display_user_listings():
    """Main entry point."""
    all_items = get_all_items()
    id_to_name = build_id_to_name_mapping(all_items)
    user_listings = extract_user_listings("bhwsg", id_to_name)
    data_rows = build_rows(user_listings)
    column_widths = determine_widths(data_rows)
    display_listings(data_rows, column_widths)


if __name__ == "__main__":
    display_user_listings()
