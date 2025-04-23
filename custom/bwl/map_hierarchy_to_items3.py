import os
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
import sqlite3
from functools import partial
from tqdm import tqdm
import swifter
import dask.dataframe as dd


def load_xref():
    df = pd.read_excel("c:\\infor_migration\\spreadsheets\\BWL_WANKE_COMBINED_H3.xlsx")

    # Pre-process DataFrame once to avoid repeated operations during matching
    df_clean = df.copy()
    df_clean.replace(np.nan, "", inplace=True)

    # Create additional lookup dictionaries for faster matching
    df_clean['price_class_match'] = df_clean.apply(
        lambda row: any(row[c] == row[c] and row[c] != "" for c in [c for c in df.columns if c.startswith("PC")]),
        axis=1
    )

    return df_clean


def find_best_match_vectorized(df, items_batch, weights=None):
    """
    Vectorized version of find_best_match that processes multiple items at once
    """
    if weights is None:
        weights = {
            "price_class": 5,  # highest priority
            "product_line": 4,
            "item_class2": 3,
            "item_class1": 2,
            "manufacturer": 1
        }

    # Identify all "PC" columns once
    pc_cols = [c for c in df.columns if c.startswith("PC")]

    results = []

    # Process items in batch for better performance
    for item in items_batch:
        product_line = item["IPRODL"].strip()
        manufacturer = item["IMFGR"].strip()
        item_class1 = item["ICLAS1"].strip()
        item_class2 = item["ICLAS2"].strip()
        price_class = item["IPRCCD"].strip()

        # Initialize scores DataFrame
        scores = pd.Series(0, index=df.index)

        # 1) Price class match - Vectorized across all PC columns
        price_matches = df[pc_cols].eq(price_class).any(axis=1)
        scores = scores.add(price_matches * weights["price_class"])

        # 2) Product line match - Vectorized
        pl_matches = df[["PL1", "PL2"]].eq(product_line).any(axis=1)
        scores = scores.add(pl_matches * weights["product_line"])

        # 3) Item class 2 match - Vectorized
        ic2_matches = df["IC2"] == item_class2
        scores = scores.add(ic2_matches * weights["item_class2"])

        # 4) Item class 1 match - Vectorized
        ic1_matches = df["IC1"] == item_class1
        scores = scores.add(ic1_matches * weights["item_class1"])

        # 5) Manufacturer match - Vectorized
        mfgr_matches = df["MFGR"] == manufacturer
        scores = scores.add(mfgr_matches * weights["manufacturer"])

        # Find best score and corresponding row
        if scores.max() > 0:
            best_idx = scores.idxmax()
            best_row = df.iloc[best_idx]
            best_score = scores[best_idx]
        else:
            best_row = None
            best_score = 0

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

        results.append(result)

    return results


def process_batch(batch, df):
    """Process a batch of items using the vectorized approach"""
    return find_best_match_vectorized(df, batch)


if __name__ == '__main__':
    print("🔄 Loading spreadsheet...")
    df = load_xref()

    print("🔄 Connecting to database...")
    conn = sqlite3.connect(r"c:\infor_migration\db\migration.db")

    # Use a more efficient query with specific columns selection
    query = """
    SELECT ITEMNUMBER, INAME, INAME2, IMFGR, IPRODL, ICLAS1, ICLAS2, IPRCCD
    FROM items 
    WHERE iprodl != 'SAM' 
    ORDER BY itemnumber
    """

    cursor = conn.cursor()
    rows = cursor.execute(query).fetchall()
    col_names = [desc[0].upper() for desc in cursor.description]
    items = [dict(zip(col_names, row)) for row in rows]
    conn.close()

    print(f"📦 Loaded {len(items)} items from database.")
    print("🚀 Beginning batch processing...")

    # Process in batches for better performance
    BATCH_SIZE = 1000  # Adjust based on your system memory and CPU

    all_results = []
    num_batches = (len(items) + BATCH_SIZE - 1) // BATCH_SIZE

    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count())) as executor:
        # Create batches
        item_batches = [items[i:i + BATCH_SIZE] for i in range(0, len(items), BATCH_SIZE)]

        # Process batches in parallel
        process_batch_with_df = partial(process_batch, df=df)
        batch_results = list(tqdm(executor.map(process_batch_with_df, item_batches), total=num_batches))

        # Flatten results
        for batch in batch_results:
            all_results.extend(batch)

    print("💾 Writing output to Excel...")
    results_df = pd.DataFrame(all_results)

    # Use engine='openpyxl' for better performance with large datasets
    results_df.to_excel(r"c:\infor_migration\spreadsheets\map_hierarchy_to_items-20.xlsx", index=False, engine='openpyxl')

    print("✅ Done! Results saved.")