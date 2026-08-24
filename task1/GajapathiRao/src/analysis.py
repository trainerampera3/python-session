import pandas as pd


# def create_master_dataframe(
#     payment,
#     time,
#     store,
#     item,
#     customer,
#     fact,
# ):
#     df = fact.merge(
#         payment,
#         on="payment_key",
#         how="left",
#     )

#     df = df.merge(
#         customer,
#         on="customer_key",
#         how="left",
#     )

#     df = df.merge(
#         time,
#         on="time_key",
#         how="left",
#     )

#     df = df.merge(
#         item,
#         on="item_key",
#         how="left",
#         suffixes=("_fact", "_item"),
#     )

#     df = df.merge(
#         store,
#         on="store_key",
#         how="left",
#     )

#     return df

def create_master_dataframe(
    payment,
    time,
    store,
    item,
    customer,
    fact,
):
    master = fact.merge(
        payment,
        on="payment_key",
        how="left",
    )

    master = master.merge(
        customer,
        on="customer_key",
        how="left",
    )

    master = master.merge(
        time,
        on="time_key",
        how="left",
    )

    master = master.merge(
        item,
        on="item_key",
        how="left",
        suffixes=("_fact", "_item"),
    )

    master = master.merge(
        store,
        on="store_key",
        how="left",
    )

    return master