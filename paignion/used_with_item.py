from paignion.exception import PaignionException


class PaignionUsedWithItem(object):
    def __init__(
        self,
        name,
        effect_message,
        consumes_subject=True,
        consumes_object=True,
        actions=None,
    ):
        self.name = name
        self.effect_message = effect_message
        self.consumes_subject = consumes_subject
        self.consumes_object = consumes_object
        self.actions = actions

        self.verify_attributes()

    def verify_attributes(self):
        # Subject should not be consumed by default
        self.consumes_subject = False if not self.consumes_subject else True
        # Object should not be consumed by default
        self.consumes_object = False if not self.consumes_object else True

        # Item name is mandatory
        if not self.name:
            raise PaignionException("Name missing for used_with item")

        # Effect message is mandatory
        if not self.effect_message:
            raise PaignionException(
                f"Effect message missing for used_with item `{self.name}`"
            )

        # TODO verify actions

    def dump(self):
        return {
            "name": self.name,
            "effect_message": self.effect_message,
            "consumes_subject": self.consumes_subject,
            "consumes_object": self.consumes_object,
            "actions": self.actions,
        }

    def __str__(self):
        return json.dumps(self.dump(), indent=4)
