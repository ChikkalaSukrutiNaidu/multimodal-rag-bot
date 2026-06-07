def correct_company_names(text):

    text = text.lower()

    corrections = {

        # TCS
        "tisius": "tcs",
        "tcs company": "tcs",
        "t c s": "tcs",
        "tata consultancy services": "tcs",
        "tisiyus": "tcs",
        "tcs ceo": "tcs ceo",

        # Infosys
        "infosis": "infosys",
        "info sys": "infosys",
        "infosis": "infosys",

        # Wipro
        "vipro": "wipro",
        "wepro": "wipro",
        "vipro": "wipro"
    }

    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    return text