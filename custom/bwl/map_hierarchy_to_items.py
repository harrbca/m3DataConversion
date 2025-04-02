from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import numpy as np
import sqlite3
import concurrent.futures
from functools import partial
from tqdm import tqdm

def load_xref():
    df = pd.read_excel("c:\\infor_migration\\spreadsheets\\BWL_WANKE_COMBINED_H3.xlsx")
    return df

def find_best_match(
    df: pd.DataFrame,
    price_class: str,
    product_line: str,
    item_class1: str,
    item_class2: str,
    manufacturer: str,
    weights: dict = None
):
    """
    Given a DataFrame `df` with columns:
      - MFGR
      - IC1, IC2
      - PL1, PL2, PL3
      - PC1..PC64
      - H1, H2, H3, H4  (among others)

    Assign "points" for each match:
      - If row has the `price_class` in any PC column => add weights["price_class"]
      - If row has product_line in PL1 or PL2 or PL3 => add weights["product_line"]
      - If row's IC2 == item_class2 => add weights["item_class2"]
      - If row's IC1 == item_class1 => add weights["item_class1"]
      - If row's MFGR == manufacturer => add weights["manufacturer"]

    The row with the highest total "score" wins.
    Returns (best_row, best_score).
    If no rows or all zero scores, returns (None, 0).
    """

    # Replace NaN with "" to avoid comparison issues
    df_copy = df.copy()
    df_copy.replace(np.nan, "", inplace=True)

    # Default weights if not provided:
    if weights is None:
        weights = {
            "price_class":   5,  # highest priority
            "product_line":  4,
            "item_class2":   3,
            "item_class1":   2,
            "manufacturer":  1
        }

    # Identify all "PC" columns
    pc_cols = [c for c in df_copy.columns if c.startswith("PC")]

    best_score = 0
    best_row = None


    for idx, row in df_copy.iterrows():
        row_score = 0
        row_details = {"matches": [], "row_index": idx}

        # 1) Price class match (PC1..PC64)
        #    If the row has `price_class` in ANY of those columns => add points
        #    We'll see if `price_class` is in row[pc_cols].values
        if price_class in row[pc_cols].values:
            row_score += weights["price_class"]

        # 2) Product line match (PL1, PL2, PL3)
        if product_line in [row["PL1"], row["PL2"]]:
            row_score += weights["product_line"]

        # 3) Item class 2 match (IC2)
        if row["IC2"] == item_class2:
            row_score += weights["item_class2"]

        # 4) Item class 1 match (IC1)
        if row["IC1"] == item_class1:
            row_score += weights["item_class1"]

        # 5) Manufacturer match (MFGR)
        if row["MFGR"] == manufacturer:
            row_score += weights["manufacturer"]

        # If this row's score is better than the current best, update
        if row_score > best_score:
            best_score = row_score
            best_row = row


    # If best_score remains 0, that implies no row matched anything
    if best_row is None:
        return None, 0

    return best_row, best_score

def match_item(args):
    item, df_dict = args  # Unpack the tuple

    df = pd.DataFrame.from_dict(df_dict)

    product_line = item["IPRODL"].strip()
    manufacturer = item["IMFGR"].strip()
    item_class1 = item["ICLAS1"].strip()
    item_class2 = item["ICLAS2"].strip()
    price_class = item["IPRCCD"].strip()

    best_row, best_score = find_best_match(df, price_class, product_line, item_class1, item_class2, manufacturer)

    result = {
        "ITEMNUMBER": item["ITEMNUMBER"],
        "INAME": item["INAME"],
        "INAME2": item["INAME2"],
        "MFGR": item["IMFGR"],
        "PRODUCTLINE": product_line,
        "ITEMCLASS1": item_class1,
        "ITEMCLASS2": item_class2,
        "PRICECLASS": price_class,
        "Score": best_score
    }

    if best_row is not None:
        result.update({
            "H1": best_row["H1"],
            "H2": best_row["H2"],
            "H3": best_row["H3"],
            "H4": best_row["H4"],
            "H1Desc": best_row["H1Desc"],
            "H2Desc": best_row["H2Desc"],
            "H3Desc": best_row["H3Desc"],
            "H4Desc": best_row["H4Desc"]
        })
    else:
        result.update({
            "H1": None,
            "H2": None,
            "H3": None,
            "H4": None,
            "H1Desc": None,
            "H2Desc": None,
            "H3Desc": None,
            "H4Desc": None
        })

    return result

if __name__ == '__main__':
    print("🔄 Loading spreadsheet...")
    df = load_xref()

    print("🔄 Connecting to database...")
    conn = sqlite3.connect(r"c:\infor_migration\db\migration.db")
    query = "SELECT * FROM items WHERE iprodl != 'SAM' ORDER BY itemnumber"
    cursor = conn.cursor()
    rows = cursor.execute(query).fetchall()
    col_names = [desc[0].upper() for desc in cursor.description]
    items = [dict(zip(col_names, row)) for row in rows]
    conn.close()

    print(f"📦 Loaded {len(items)} items from database.")
    print("🚀 Beginning parallel match processing...")

    # Serialize df to make it safe for multiprocessing
    df_dict = df.to_dict(orient='list')

    # Combine items and df_dict into a single iterable of tuples
    args_list = [(item, df_dict) for item in items]

    # Run in parallel
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(match_item, args_list), total=len(items)))

    print("💾 Writing output to Excel...")
    results_df = pd.DataFrame(results)
    results_df.to_excel(r"c:\infor_migration\spreadsheets\map_hierarchy_to_items.xlsx", index=False)

    print("✅ Done! Results saved.")
