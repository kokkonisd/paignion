import pytest

from paignion.used_with_item import PaignionUsedWithItem
from paignion.exceptions import PaignionUsedWithItemException


EXPECTED_DEFAULT_USED_WITH_ITEM_DUMP = """\
{
    "actions": "",
    "consumes_object": false,
    "consumes_subject": false,
    "effect_message": "test effect message",
    "name": "test name"
}\
"""


class TestUsedWithItemObject:
    def test_used_with_item_defaults(self):
        uw_item = PaignionUsedWithItem(
            name="test name", effect_message="test effect message"
        )

        assert uw_item.name == "test name"
        assert uw_item.effect_message == "test effect message"
        assert uw_item.consumes_subject == False
        assert uw_item.consumes_object == False
        assert uw_item.actions == ""

    def test_missing_name_and_effect_message(self):
        with pytest.raises(
            TypeError,
            match=r".+ missing 2 required positional arguments: 'name' and "
            r"'effect_message'",
        ):
            uw_item = PaignionUsedWithItem()

        with pytest.raises(
            TypeError,
            match=r".+ missing 1 required positional argument: 'effect_message'",
        ):
            uw_item = PaignionUsedWithItem(name="test name")

        with pytest.raises(
            TypeError, match=r".+ missing 1 required positional argument: 'name'"
        ):
            uw_item = PaignionUsedWithItem(effect_message="test effect message")

        with pytest.raises(
            PaignionUsedWithItemException, match=r"Name missing for used_with item"
        ):
            uw_item = PaignionUsedWithItem(
                name=None, effect_message="test effect message"
            )

        with pytest.raises(
            PaignionUsedWithItemException,
            match=r"Effect message missing for used_with item `test name`",
        ):
            uw_item = PaignionUsedWithItem(name="test name", effect_message=None)

        with pytest.raises(
            PaignionUsedWithItemException, match=r"Name missing for used_with item"
        ):
            uw_item = PaignionUsedWithItem(name=None, effect_message=None)

    def test_accepts_correct_consume_flags(self):
        uw_item = PaignionUsedWithItem(
            name="test name",
            effect_message="test effect message",
            consumes_subject=False,
            consumes_object=False,
        )
        assert uw_item.consumes_subject == False
        assert uw_item.consumes_object == False

        uw_item = PaignionUsedWithItem(
            name="test name",
            effect_message="test effect message",
            consumes_subject=False,
            consumes_object=True,
        )
        assert uw_item.consumes_subject == False
        assert uw_item.consumes_object == True

        uw_item = PaignionUsedWithItem(
            name="test name",
            effect_message="test effect message",
            consumes_subject=True,
            consumes_object=False,
        )
        assert uw_item.consumes_subject == True
        assert uw_item.consumes_object == False

        uw_item = PaignionUsedWithItem(
            name="test name",
            effect_message="test effect message",
            consumes_subject=True,
            consumes_object=True,
        )
        assert uw_item.consumes_subject == True
        assert uw_item.consumes_object == True

    def test_passing_nonlist_values_to_actions(self):
        with pytest.raises(
            PaignionUsedWithItemException,
            match=r"Actions should be a list for used_with item `test name`",
        ):
            uw_item = PaignionUsedWithItem(
                name="test name", effect_message="test effect message", actions=1
            )

        with pytest.raises(
            PaignionUsedWithItemException,
            match=r"Actions should be a list for used_with item `test name`",
        ):
            uw_item = PaignionUsedWithItem(
                name="test name",
                effect_message="test effect message",
                actions='set(west, "hidden_room", origin)',
            )

    def test_dump(self):
        self.maxDiff = None

        uw_item = PaignionUsedWithItem(
            name="test name", effect_message="test effect message"
        )

        assert str(uw_item) == EXPECTED_DEFAULT_USED_WITH_ITEM_DUMP
