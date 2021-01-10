import pytest

from paignion.action_compiler import ActionCompiler
from paignion.exceptions import PaignionActionCompilerException


class TestActionCompiler:
    def test_random_commands(self):
        ac = ActionCompiler()

        # Pure whitespace should pass, but should compile to nothing
        res = ac.compile_action("  \t\t\t\t     \t   ")
        assert res == ""

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            ac.compile_action('write "haha" in description')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            ac.compile_action("agdsjakgdjh")

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            ac.compile_action('m"_test"')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            ac.compile_action("137")

    def test_normal_set_command(self):
        ac = ActionCompiler()

        res = ac.compile_action('set(west, "hidden room", origin)')
        assert res == 'getRoomOrItem("origin")["west"] = "hidden room";'

        # Whitespace should not matter
        res = ac.compile_action('set ( west,"hidden room",         \t\t      origin )')
        assert res == 'getRoomOrItem("origin")["west"] = "hidden room";'

        # Quotes should not matter for keys and objects (amount and book case in this
        # case)
        res = ac.compile_action('set("amount", "inf", "book case")')
        assert res == 'getRoomOrItem("book case")["amount"] = "inf";'

        res = ac.compile_action('set(amount, 15, "book case")')
        assert res == 'getRoomOrItem("book case")["amount"] = 15;'

        # Markdown strings should render correctly
        res = ac.compile_action(
            'set(description, m"Very, _very_ **broken**", "old door")'
        )
        assert (
            res == 'getRoomOrItem("old door")["description"] = "<p>Very, <em>very</em> '
            '<strong>broken</strong></p>";'
        )

    def test_failed_set_command(self):
        ac = ActionCompiler()

        # Test typo in set keyword
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            ac.compile_action('st(west, "hidden room", origin)')

        # Test missing one argument
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('set(west, "hidden room")')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('set(west, "hidden room",)')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("set(west, , origin)")

        # Test missing two arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("set(west)")

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("set(west,)")

        # Test missing all arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("set(   )")

        # Test missing parentheses
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('set west to "hidden room" for origin')

        # Test missing closing parenthesis
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but there are no more tokens",
        ):
            ac.compile_action('set(west, "hidden room", origin')

        # Test no commas
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('set(description m"This is now the _hidden_ room" origin')

    def test_normal_add_command(self):
        ac = ActionCompiler()

        res = ac.compile_action('add("The door is now unlocked.", description, origin)')
        assert (
            res
            == 'getRoomOrItem("origin")["description"] += "The door is now unlocked.";'
        )

        # Whitespace should not matter
        res = ac.compile_action(
            'add (  "The door is now unlocked.",description ,  \t\t     origin)'
        )
        assert (
            res
            == 'getRoomOrItem("origin")["description"] += "The door is now unlocked.";'
        )

        # Quotes should not matter for keys and objects (amount and book case in this
        # case)
        res = ac.compile_action('add(" It also smells bad.", "description", "sock")')
        assert res == 'getRoomOrItem("sock")["description"] += " It also smells bad.";'

        res = ac.compile_action('add(241, amount, "book case")')
        assert res == 'getRoomOrItem("book case")["amount"] += 241;'

        # Markdown strings should render correctly
        res = ac.compile_action(
            'add(m" Very, _very_ **broken**.", description, "old door")'
        )
        assert (
            res
            == 'getRoomOrItem("old door")["description"] += "<p>Very, <em>very</em> '
            '<strong>broken</strong>.</p>";'
        )

        # Negative integers should also work
        res = ac.compile_action("add(-10, amount, coin)")
        assert res == 'getRoomOrItem("coin")["amount"] += -10;'

    def test_failed_add_command(self):
        ac = ActionCompiler()

        # Test typo in add keyword
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            res = ac.compile_action('ad(241, amount, "book case")')

        # Test missing one argument
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('add("west", "description")')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('add("west", "description",)')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('add("west", ,origin)')

        # Test missing two arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('add("west")')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('add("west",)')

        # Test missing all arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("add(   )")

        # Test missing parentheses
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('add m" _west_" to "description" for origin')

        # Test missing closing parenthesis
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but there are no more tokens",
        ):
            ac.compile_action('add("west", description, origin')

        # Test no commas
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('add(m"This is now the _hidden_ room" description origin')

        # Test missing quotes for string
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("add(This is now the hidden room, description, origin")

    def test_normal_sub_command(self):
        ac = ActionCompiler()

        res = ac.compile_action('sub(10, amount, "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] -= 10;'

        # Whitespace should not matter
        res = ac.compile_action('sub (  10,amount ,  \t\t     "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] -= 10;'

        # Negative numbers should pass
        res = ac.compile_action('sub(-2, "amount", "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] -= -2;'

        # Zero should also pass
        res = ac.compile_action('sub(-0, amount, "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] -= 0;'

    def test_failed_sub_command(self):
        ac = ActionCompiler()

        # Test typo in sub keyword
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            ac.compile_action('sb(10, amount, "health points")')

        # Test missing one argument
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("sub(10, amount)")

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("sub(10, amount,)")

        # Test missing two arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("sub(10)")

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("sub(10, )")

        # Test missing all arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("sub(  )")

        # Test missing parentheses
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("sub 10 from amount for coin")

        # Test missing closing parenthesis
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but there are no more tokens",
        ):
            ac.compile_action("sub(10, amount, coin")

        # Test passing Markdown string or normal string instead of integer
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('sub("aaa", description, origin)')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('sub(m"_aaa_", description, origin)')

        # Test passing invalid integer
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined token `.+` in `.+`, in action `.+`",
        ):
            ac.compile_action("sub(10f, description, origin)")

    def test_normal_mul_command(self):
        ac = ActionCompiler()

        res = ac.compile_action('mul(10, amount, "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] *= 10;'

        # Whitespace should not matter
        res = ac.compile_action('mul (  10,amount ,  \t\t     "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] *= 10;'

        # Negative numbers should pass
        res = ac.compile_action('mul(-2, amount, "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] *= -2;'

        # Zero should also pass
        res = ac.compile_action('mul(-0, "amount", "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] *= 0;'

    def test_failed_mul_command(self):
        ac = ActionCompiler()

        # Test typo in sub keyword
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            ac.compile_action('ml(10, amount, "health points")')

        # Test missing one argument
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("mul(10, amount)")

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("mul(10, amount,)")

        # Test missing two arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("mul(10)")

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("mul(10, )")

        # Test missing all arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("mul(  )")

        # Test missing parentheses
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("mul 10 from amount for coin")

        # Test missing closing parenthesis
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but there are no more tokens",
        ):
            ac.compile_action("mul(10, amount, coin")

        # Test passing Markdown string or normal string instead of integer
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('mul("aaa", description, origin)')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('mul(m"_aaa_", description, origin)')

        # Test passing invalid integer
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined token `.+` in `.+`, in action `.+`",
        ):
            ac.compile_action("mul(10f, description, origin)")

    def test_normal_div_command(self):
        ac = ActionCompiler()

        res = ac.compile_action('div(10, "amount", "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] /= 10;'

        # Whitespace should not matter
        res = ac.compile_action('div (  10,amount ,  \t\t     "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] /= 10;'

        # Negative numbers should pass
        res = ac.compile_action('div(-2, amount, "health points")')
        assert res == 'getRoomOrItem("health points")["amount"] /= -2;'

    def test_failed_div_command(self):
        ac = ActionCompiler()

        # Test division by zero
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"div\(\) action with 0 detected, cannot divide by 0",
        ):
            ac.compile_action('div(0, amount, "health points")')

        # Test typo in sub keyword
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined structure starting with `.+` for action `.+`",
        ):
            ac.compile_action('dv(10, amount, "health points")')

        # Test missing one argument
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("div(10, amount)")

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("div(10, amount,)")

        # Test missing two arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("div(10)")

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("div(10, )")

        # Test missing all arguments
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("div(  )")

        # Test missing parentheses
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action("div 10 from amount for coin")

        # Test missing closing parenthesis
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but there are no more tokens",
        ):
            ac.compile_action("div(10, amount, coin")

        # Test passing Markdown string or normal string instead of integer
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('div("aaa", description, origin)')

        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Expected token type `.+` but got `.+`",
        ):
            ac.compile_action('div(m"_aaa_", description, origin)')

        # Test passing invalid integer
        with pytest.raises(
            PaignionActionCompilerException,
            match=r"Undefined token `.+` in `.+`, in action `.+`",
        ):
            ac.compile_action("div(10f, description, origin)")
