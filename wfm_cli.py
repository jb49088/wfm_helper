# ================================================================================
# =                                   WFM_CLI                                    =
# ================================================================================

import argparse

from copy_user_listings import copy_user_listings
from display_item_listings import display_item_listings
from display_user_listings import display_user_listings


def wfm_cli():
    """Main entry point for wfm_cli."""
    copy_user_listings()
    display_item_listings()
    display_user_listings()


if __name__ == "__main__":
    wfm_cli()
