import requests


# ======================================================
# CURRENCY CONVERTER AGENT
# ======================================================

def convert_currency(amount, from_currency, to_currency):
    """
    Convert currency using Frankfurter API.
    """

    url = "https://api.frankfurter.app/latest"

    params = {
        "amount": amount,
        "from": from_currency.upper(),
        "to": to_currency.upper()
    }

    try:

        response = requests.get(url, params=params)

        if response.status_code != 200:
            return "Unable to convert currency. Please check the currency codes."

        data = response.json()

        converted_amount = list(data["rates"].values())[0]

        return (
            f"💱 Currency Conversion\n\n"
            f"💵 {amount} {from_currency.upper()}\n"
            f"⬇️\n"
            f"💰 {converted_amount:.2f} {to_currency.upper()}"
        )

    except Exception as e:
        return f"Currency Error: {e}"