from paignion.exception import PaignionException


class PaignionItem(object):
    def __init__(
        self, name, description, amount=1, visible=True, effect=None, used_with=None
    ):
        self.name = name
        self.description = description
        self.amount = amount
        self.visible = visible
        self.effect = effect
        self.used_with = used_with

        self.verify_attributes()

    def verify_attributes(self):
        # Amount should be 1 by default
        self.amount = 1 if not self.amount else self.amount
        # Item should be visible by default
        self.visible = True if self.visible == None else self.visible
        # Used with should be an empty list by default
        self.used_with = [] if not self.used_with else self.used_with

        # Item name is mandatory
        if not self.name:
            raise PaignionException("Name missing for item")

        # Item description is mandatory
        if self.visible and not self.description:
            raise PaignionException(f"Description missing for item `{self.name}`")

    def dump(self):
        return {
            "name": self.name,
            "description": self.description,
            "amount": self.amount,
            "visible": self.visible,
            "effect": self.effect,
            "used_with": [i.dump() for i in self.used_with],
        }

    def __str__(self):
        return json.dumps(self.dump(), indent=4)
