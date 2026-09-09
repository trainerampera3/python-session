import pandas as pd


def clean_data(
    payment,
    time,
    store,
    item,
    customer,
    fact,
):


    customer = customer.rename(
        columns={
            "coustomer_key": "customer_key"
        }
    )

    fact = fact.rename(
        columns={
            "coustomer_key": "customer_key"
        }
    )


    payment["bank_name"] = payment["bank_name"].fillna(
        "No Bank / Cash"
    )

    item["unit"] = item["unit"].fillna(
        "Unknown"
    )

    customer["name"] = customer["name"].fillna(
        "Unknown Customer"
    )

    fact["unit"] = fact["unit"].fillna(
        "Unknown"
    )


    fact["quantity"] = pd.to_numeric(
        fact["quantity"],
        errors="coerce"
    )

    fact["unit_price"] = pd.to_numeric(
        fact["unit_price"],
        errors="coerce"
    )

    fact["total_price"] = pd.to_numeric(
        fact["total_price"],
        errors="coerce"
    )

    item["unit_price"] = pd.to_numeric(
        item["unit_price"],
        errors="coerce"
    )


    time["date"] = pd.to_datetime(
        time["date"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    return (
        payment,
        time,
        store,
        item,
        customer,
        fact,
    )