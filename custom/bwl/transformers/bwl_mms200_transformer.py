from transformers.mms200_transformer import MMS200Transformer

class BWLMMS200Transformer(MMS200Transformer):
    """
    Custom transformer class that overrides the MMS200Transformer.
    """

    def get_responsible(self):
        return "KFEHR"