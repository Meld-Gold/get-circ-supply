import datetime
from dateutil import tz
from algosdk.v2client import indexer

TO_ZONE = tz.gettz("Australia/Sydney")

DEFAULT_INDEXER_ADDRESS = "https://mainnet-idx.algonode.cloud"
DEFAULT_INDEXER_TOKEN = ""

SNAPSHOT_ROUND = 29_987_135
RESERVE_ADDRESS = "V3NFJSXNZJKEB76N7VSKJXH7AZMYS6NFOJ7K2CYYORO74LM3USCF4HEC6Y"
GOLD_ASA_ID = 246516580
SILVER_ASA_ID = 246519683
TOTAL_SUPPLY = 100_000_000_000_000_000


def get_indexer_client(
    addr: str = DEFAULT_INDEXER_ADDRESS, token: str = DEFAULT_INDEXER_TOKEN
) -> indexer.IndexerClient:
    return indexer.IndexerClient(indexer_token=token, indexer_address=addr)


indexer = get_indexer_client()

# Get account balance at round
account_info = indexer.account_info(
    round_num=SNAPSHOT_ROUND,
    address=RESERVE_ADDRESS,
)

# Get time at that round
round_time = indexer.block_info(round_num=SNAPSHOT_ROUND)["timestamp"]

# This should return in our local timezone
round_time = datetime.datetime.fromtimestamp(round_time)

print(f"Round time AEST: {round_time}")

# Get assets
assets = account_info["account"]["assets"]

# Find asset that matches gold

gold_asset = [asset for asset in assets if asset["asset-id"] == GOLD_ASA_ID][0]

# Calculate circulating supply by subtracting gold asset amount from total supply
circulating_supply = TOTAL_SUPPLY - gold_asset["amount"]

print(f"Circulating supply of GOLD$: {circulating_supply}")

# Save to CSV
with open("circulating_supply.csv", "w") as f:
    # asset_name","asset_id","circulating_supply", "round_time
    f.write("asset_name,asset_id,circulating_supply,round_time\n")
    f.write(f"GOLD$, {GOLD_ASA_ID}, {circulating_supply}, {round_time}\n")


# Find asset that matches silver
silver_asset = [asset for asset in assets if asset["asset-id"] == SILVER_ASA_ID][0]

# Calculate circulating supply by subtracting silver asset amount from total supply
circulating_supply = TOTAL_SUPPLY - silver_asset["amount"]

# Append to CSV
with open("circulating_supply.csv", "a") as f:
    f.write(f"SILVER$, {SILVER_ASA_ID}, {circulating_supply}, {round_time}\n")
