def recommendations(
    industry
):

    if industry=="Dairy":

        return [

            "Use SS316 piping",

            "Use hygienic heat exchanger",

            "Provide CIP integration"

        ]

    elif industry=="Textile":

        return [

            "Provide thermal buffer",

            "Use process heat exchanger"

        ]

    else:

        return [

            "Provide insulated piping"

        ]