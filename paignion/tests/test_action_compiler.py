import unittest

from paignion.action_compiler import ActionCompiler
from paignion.exceptions import PaignionActionCompilerException


class TestActionCompiler(unittest.TestCase):
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
