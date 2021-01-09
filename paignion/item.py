from paignion.exceptions import PaignionItemException


class PaignionItem(object):
    """Describe a Paignion item."""

    def __init__(
        self, name, description, amount=1, visible=True, effect=None, used_with=None
    ):
        """Construct a new instance of PaignionItem.

        :param name: the name of the item
        :type name: str
        :param description: the description of the item
        :type description: str
        :param amount: the amount of the item
        :type amount: int
        :param visible: True if item is visible to `look` commands, False otherwise
        :type visible: bool
        :param effect: the effect of the item
        :type effect: str
        :param used_with: a list of PaignionUsedWithItems that this item can be used with
        :type used_with: list
        :return: an instance of PaignionItem
        """
        self.name = name
        self.description = description
        self.amount = amount
        self.visible = visible
        self.effect = effect
        self.used_with = used_with

        self.verify_attributes()

    def verify_attributes(self):
        """Verify the attributes of the PaignionItem object."""
        # Amount should be 1 by default
        self.amount = 1 if not self.amount else self.amount
        # Item should be visible by default
        self.visible = True if self.visible == None else self.visible
        # Used with should be an empty list by default
        self.used_with = [] if not self.used_with else self.used_with

        # Item name is mandatory
        if not self.name:
            raise PaignionItemException("Name missing for item")

        # Item description is mandatory
        if self.visible and not self.description:
            raise PaignionItemException(f"Description missing for item `{self.name}`")

    def dump(self):
        """Dump a dictionary containing all of the data of the item.

        :return: a dictionary containing the item's data
        """
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
