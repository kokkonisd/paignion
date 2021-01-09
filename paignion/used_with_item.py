import json

from paignion.exceptions import PaignionUsedWithItemException
from paignion.action_compiler import ActionCompiler


class PaignionUsedWithItem(object):
    """Describe a Paignion `used_with` item.

    This is not an item type, but rather an object describing an interaction of two
    Paignion items.
    """

    def __init__(
        self,
        name,
        effect_message,
        consumes_subject=False,
        consumes_object=False,
        actions=None,
    ):
        """Construct a new instance of PaignionUsedWithItem.

        :param name: the target item's name (`use X with <target>`)
        :type name: str
        :param effect_message: the message to be produced by this interaction
        :type effect_message: str
        :param consumes_subject: True if subject should be consumed, False otherwise
        :type consumes_subject: bool
        :param consumes_object: True if object should be consumed, False otherwise
        :type consumes_object: bool
        :param actions: a list of actions to be executed during the interaction
        :type actions: list
        """
        self.name = name
        self.effect_message = effect_message
        self.consumes_subject = consumes_subject
        self.consumes_object = consumes_object
        self.actions = actions

        self.verify_attributes()

        # Compile actions
        action_compiler = ActionCompiler()
        self.actions = "".join(
            [action_compiler.compile_action(a) for a in self.actions]
        )

    def verify_attributes(self):
        """Verify the attributes of the PaignionUsedWithItem object."""
        # Subject should not be consumed by default
        self.consumes_subject = False if not self.consumes_subject else True
        # Object should not be consumed by default
        self.consumes_object = False if not self.consumes_object else True
        # Actions should contain a list of actions
        self.actions = [] if not self.actions else self.actions

        # Item name is mandatory
        if not self.name:
            raise PaignionUsedWithItemException("Name missing for used_with item")

        # Effect message is mandatory
        if not self.effect_message:
            raise PaignionUsedWithItemException(
                f"Effect message missing for used_with item `{self.name}`"
            )

        # Actions should be a list
        if type(self.actions) != list:
            raise PaignionUsedWithItemException(
                f"Actions should be a list for used_with item `{self.name}`"
            )

        # All actions should be strings
        self.actions = [str(a) for a in self.actions]

    def dump(self):
        """Dump a dictionary containing all of the data of the `used_with` item.

        :return: a dictionary containing the `used_with` item's data
        """
        return {
            "name": self.name,
            "effect_message": self.effect_message,
            "consumes_subject": self.consumes_subject,
            "consumes_object": self.consumes_object,
            "actions": self.actions,
        }

    def __str__(self):
        return json.dumps(self.dump(), indent=4, sort_keys=True)
