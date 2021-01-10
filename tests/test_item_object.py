import pytest

from paignion.item import PaignionItem
from paignion.used_with_item import PaignionUsedWithItem
from paignion.exceptions import PaignionItemException


EXPECTED_DEFAULT_ITEM_DUMP = """\
{
    "amount": 1,
    "description": "test description",
    "effect": null,
    "name": "test name",
    "used_with": [],
    "visible": true
}\
"""


class TestItemObject:
    def test_item_defaults(self):
        item = PaignionItem(name="test name", description="test description")

        assert item.name == "test name"
        assert item.description == "test description"
        assert item.amount == 1
        assert item.visible == True
        assert item.effect == None
        assert item.used_with == []

    def test_missing_name_and_description(self):
        with pytest.raises(
            TypeError,
            match=r".+ missing 2 required positional arguments: 'name' and "
            r"'description'",
        ):
            item = PaignionItem()

        with pytest.raises(
            TypeError,
            match=r".+ missing 1 required positional argument: 'description'",
        ):
            item = PaignionItem(name="test name")

        with pytest.raises(
            TypeError, match=r".+ missing 1 required positional argument: 'name'"
        ):
            item = PaignionItem(description="test description")

        with pytest.raises(PaignionItemException, match=r"Name missing for item"):
            item = PaignionItem(name=None, description="test description")

        with pytest.raises(
            PaignionItemException, match=r"Description missing for item `test name`"
        ):
            item = PaignionItem(name="test name", description=None)

        with pytest.raises(PaignionItemException, match=r"Name missing for item"):
            item = PaignionItem(name=None, description=None)

    def test_accepts_integer_or_inf_amount(self):
        item = PaignionItem(name="test name", description="test description", amount=1)
        item = PaignionItem(name="test name", description="test description", amount=92)
        item = PaignionItem(
            name="test name", description="test description", amount=23.2
        )
        item = PaignionItem(
            name="test name", description="test description", amount="inf"
        )

    def test_rejects_invalid_amount(self):
        with pytest.raises(
            ValueError, match=r"invalid literal for int\(\) with base 10: 'abc'"
        ):
            item = PaignionItem(
                name="test name", description="test description", amount="abc"
            )

        with pytest.raises(
            ValueError, match=r"invalid literal for int\(\) with base 10: '10f'"
        ):
            item = PaignionItem(
                name="test name", description="test description", amount="10f"
            )

        with pytest.raises(
            PaignionItemException, match=r"Negative or zero amount for item `test name`"
        ):
            item = PaignionItem(
                name="test name", description="test description", amount=0
            )

        with pytest.raises(
            PaignionItemException, match=r"Negative or zero amount for item `test name`"
        ):
            item = PaignionItem(
                name="test name", description="test description", amount=-10
            )

    def test_accepts_correct_visible_flag(self):
        item = PaignionItem(
            name="test name", description="test description", visible=True
        )

        assert item.visible == True

        item = PaignionItem(
            name="test name", description="test description", visible=False
        )

        assert item.visible == False

    def test_passing_nonlist_values_to_used_with(self):
        with pytest.raises(
            PaignionItemException,
            match=r"used_with items should be a list for item `test name`",
        ):
            room = PaignionItem(
                name="test name", description="test description", used_with=1
            )

        with pytest.raises(
            PaignionItemException,
            match=r"used_with items should be a list for item `test name`",
        ):
            room = PaignionItem(
                name="test name",
                description="test description",
                used_with=PaignionUsedWithItem(
                    name="test used_with item",
                    effect_message="test used_with effect message",
                ),
            )

    def test_passing_lists_of_wrong_type_to_used_with(self):
        with pytest.raises(
            PaignionItemException,
            match=r"used_with item `1` has incorrect type for item `test name`",
        ):
            room = PaignionItem(
                name="test name", description="test description", used_with=[1, 2, 3]
            )

        with pytest.raises(
            PaignionItemException,
            match=r"used_with item `abc` has incorrect type for item `test name`",
        ):
            room = PaignionItem(
                name="test name",
                description="test description",
                used_with=["abc", "def", "ghi"],
            )

    def test_dump(self):
        self.maxDiff = None

        item = PaignionItem(name="test name", description="test description")

        assert str(item) == EXPECTED_DEFAULT_ITEM_DUMP
