class EMLAssistant:

    def __init__(self):
        self.name = "EML Sentinel AI"


    def analyze(self, data):

        response = {
            "market": "Analyzing market conditions...",
            "risk": "Calculating risk exposure...",
            "community": "Scanning opportunities..."
        }

        return response


    def greeting(self, user):

        return f"""
        Good morning {user}.

        I am {self.name}.
        Your intelligence system is online.
        """
