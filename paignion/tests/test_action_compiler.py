import unittest

from paignion.action_compiler import ActionCompiler
from paignion.exceptions import PaignionActionCompilerException


class TestActionCompiler(unittest.TestCase):
    def test_random_commands(self):
        ac = ActionCompiler()

        # Pure whitespace should pass, but should compile to nothing
        res = ac.compile_action("  \t\t\t\t     \t   ")
        self.assertEqual(res, "")

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('write "haha" in description')

        self.assertEqual(
            str(err.exception),
            "Undefined structure starting with `IDENTIFIER_TOKEN(`write`)` for action "
            '`write "haha" in description`',
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action("agdsjakgdjh")

        self.assertEqual(
            str(err.exception),
            "Undefined structure starting with `IDENTIFIER_TOKEN(`agdsjakgdjh`)` for "
            "action `agdsjakgdjh`",
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('m"_test"')

        self.assertEqual(
            str(err.exception),
            'Undefined structure starting with `MD_STRING_TOKEN(`m"_test"`)` for '
            'action `m"_test"`',
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action("137")

        self.assertEqual(
            str(err.exception),
            "Undefined structure starting with `INTEGER_TOKEN(`137`)` for action `137`",
        )

    def test_normal_set_command(self):
        ac = ActionCompiler()

        res = ac.compile_action('set(west, "hidden room", origin)')
        self.assertEqual(res, 'getRoomOrItem("origin")["west"] = "hidden room";')

        # Whitespace should not matter
        res = ac.compile_action('set ( west,"hidden room",         \t\t      origin )')
        self.assertEqual(res, 'getRoomOrItem("origin")["west"] = "hidden room";')

        # Quotes should not matter for keys and objects (amount and book case in this
        # case)
        res = ac.compile_action('set("amount", "inf", "book case")')
        self.assertEqual(res, 'getRoomOrItem("book case")["amount"] = "inf";')

        res = ac.compile_action('set(amount, 15, "book case")')
        self.assertEqual(res, 'getRoomOrItem("book case")["amount"] = 15;')

        # Markdown strings should render correctly
        res = ac.compile_action(
            'set(description, m"Very, _very_ **broken**", "old door")'
        )
        self.assertEqual(
            res,
            'getRoomOrItem("old door")["description"] = "<p>Very, <em>very</em> '
            '<strong>broken</strong></p>";',
        )

    def test_failed_set_command(self):
        ac = ActionCompiler()

        # Test typo in set keyword
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('st(west, "hidden room", origin)')

        self.assertEqual(
            str(err.exception),
            "Undefined structure starting with `IDENTIFIER_TOKEN(`st`)` for action "
            '`st(west, "hidden room", origin)`',
        )

        # Test missing one argument
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('set(west, "hidden room")')

        self.assertEqual(
            str(err.exception), "Expected token type `comma` but got `cparen`"
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('set(west, "hidden room",)')

        self.assertEqual(
            str(err.exception), "Expected token type `identifier` but got `cparen`"
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action("set(west, , origin)")

        self.assertEqual(
            str(err.exception), "Expected token type `string` but got `comma`"
        )

        # Test missing two arguments
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action("set(west)")

        self.assertEqual(
            str(err.exception), "Expected token type `comma` but got `cparen`"
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action("set(west,)")

        self.assertEqual(
            str(err.exception), "Expected token type `string` but got `cparen`"
        )

        # Test missing all arguments
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action("set(   )")

        self.assertEqual(
            str(err.exception), "Expected token type `identifier` but got `cparen`"
        )

        # Test missing parentheses
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('set west to "hidden room" for origin')

        self.assertEqual(
            str(err.exception), "Expected token type `oparen` but got `identifier`"
        )

        # Test missing closing parenthesis
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('set(west, "hidden room", origin')

        self.assertEqual(
            str(err.exception),
            "Expected token type `cparen` but there are no more tokens",
        )

        # Test no commas
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('set(description m"This is now the _hidden_ room" origin')

        self.assertEqual(
            str(err.exception),
            "Expected token type `comma` but got `md_string`",
        )

    def test_normal_add_command(self):
        ac = ActionCompiler()

        res = ac.compile_action('add("The door is now unlocked.", description, origin)')
        self.assertEqual(
            res,
            'getRoomOrItem("origin")["description"] += "The door is now unlocked.";',
        )

        # Whitespace should not matter
        res = ac.compile_action(
            'add (  "The door is now unlocked.",description ,  \t\t     origin)'
        )
        self.assertEqual(
            res,
            'getRoomOrItem("origin")["description"] += "The door is now unlocked.";',
        )

        # Quotes should not matter for keys and objects (amount and book case in this
        # case)
        res = ac.compile_action('add(" It also smells bad.", "description", "sock")')
        self.assertEqual(
            res, 'getRoomOrItem("sock")["description"] += " It also smells bad.";'
        )

        res = ac.compile_action('add(241, amount, "book case")')
        self.assertEqual(res, 'getRoomOrItem("book case")["amount"] += 241;')

        # Markdown strings should render correctly
        res = ac.compile_action(
            'add(m" Very, _very_ **broken**.", description, "old door")'
        )
        self.assertEqual(
            res,
            'getRoomOrItem("old door")["description"] += "<p>Very, <em>very</em> '
            '<strong>broken</strong>.</p>";',
        )

    def test_failed_add_command(self):
        ac = ActionCompiler()

        # Test typo in add keyword
        with self.assertRaises(PaignionActionCompilerException) as err:
            res = ac.compile_action('ad(241, amount, "book case")')

        self.assertEqual(
            str(err.exception),
            "Undefined structure starting with `IDENTIFIER_TOKEN(`ad`)` for action "
            '`ad(241, amount, "book case")`',
        )

        # Test missing one argument
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('add("west", "description")')

        self.assertEqual(
            str(err.exception), "Expected token type `comma` but got `cparen`"
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('add("west", "description",)')

        self.assertEqual(
            str(err.exception), "Expected token type `identifier` but got `cparen`"
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('add("west", ,origin)')

        self.assertEqual(
            str(err.exception), "Expected token type `identifier` but got `comma`"
        )

        # Test missing two arguments
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('add("west")')

        self.assertEqual(
            str(err.exception), "Expected token type `comma` but got `cparen`"
        )

        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('add("west",)')

        self.assertEqual(
            str(err.exception), "Expected token type `identifier` but got `cparen`"
        )

        # Test missing all arguments
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action("add(   )")

        self.assertEqual(
            str(err.exception), "Expected token type `string` but got `cparen`"
        )

        # Test missing parentheses
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('add m" _west_" to "description" for origin')

        self.assertEqual(
            str(err.exception), "Expected token type `oparen` but got `md_string`"
        )

        # Test missing closing parenthesis
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('add("west", description, origin')

        self.assertEqual(
            str(err.exception),
            "Expected token type `cparen` but there are no more tokens",
        )

        # Test no commas
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action('add(m"This is now the _hidden_ room" description origin')

        self.assertEqual(
            str(err.exception),
            "Expected token type `comma` but got `identifier`",
        )

        # Test missing quotes for string
        with self.assertRaises(PaignionActionCompilerException) as err:
            ac.compile_action("add(This is now the hidden room, description, origin")

        self.assertEqual(
            str(err.exception),
            "Expected token type `string` but got `identifier`",
        )

    def test_normal_sub_command(self):
        pass  # TODO

    def test_failed_sub_command(self):
        pass  # TODO

    def test_normal_mul_command(self):
        pass  # TODO

    def test_failed_mul_command(self):
        pass  # TODO

    def test_normal_div_command(self):
        pass  # TODO

    def test_failed_div_command(self):
        pass  # TODO
