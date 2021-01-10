import re

from paignion.exceptions import PaignionActionCompilerException
from paignion.tools import markdownify


class ActionToken(object):
    """Describe a Paignion Action token.

    This class is used to represent tokens as they are parsed from Paignion Actions.
    """

    def __init__(self, type, value):
        """Constructs a new instance of ActionToken.

        :param type: the type of the token
        :type type: str
        :param value: the value of the token
        :type value: str or int
        :return: an instance of ActionToken
        """
        self.type = type
        self.value = value

    def __str__(self):
        return f"{self.type.upper()}_TOKEN(`{self.value}`)"

    def __repr__(self):
        return self.__str__()


class ActionNode(object):
    """Describe a generic ActionNode."""

    def __init__(self, key, value, element):
        """Construct a new instance of ActionNode."""
        self.key = key
        self.value = value
        self.element = element

    def action(self):
        raise PaignionActionCompilerException("Invalid use of generic ActionNode")

    def __str__(self):
        return f"{self.action().upper()}_NODE({self.key}, {self.value}, {self.element})"


class ActionSetNode(ActionNode):
    """Describe an ActionNode for the Set action."""

    def action(self):
        """Return the action performed by the node.

        :return: the string "set"
        """
        return "set"


class ActionAddNode(ActionNode):
    """Describe an ActionNode for the Add (or append) action."""

    def action(self):
        """Return the action performed by the node.

        :return: the string "add"
        """
        return "add"


class ActionSubNode(ActionNode):
    """Describe an ActionNode for the Sub (subtraction) action."""

    def action(self):
        """Return the action performed by the node.

        :return: the string "sub"
        """
        return "sub"


class ActionMulNode(ActionNode):
    """Describe an ActionNode for the Mul (multiplication) action."""

    def action(self):
        """Return the action performed by the node.

        :return: the string "mul"
        """
        return "mul"


class ActionDivNode(ActionNode):
    """Describe an ActionNode for the Div (division) action."""

    def action(self):
        """Return the action performed by the node.

        :return: the string "div"
        """
        return "div"


class ActionCompiler(object):
    """Describe a Paignion action compiler.

    This class is able to compile all valid Paignion actions, and to raise exceptions
    when it comes across invalid actions.
    """

    # A list of all the tokens recognized by the compiler
    TOKEN_TYPES = [
        ("set_func", r"set"),
        ("add_func", r"add"),
        ("sub_func", r"sub"),
        ("mul_func", r"mul"),
        ("div_func", r"div"),
        ("md_string", r'm"(([^"\\])|(\\"))*"'),
        ("string", r'"(([^"\\])|(\\"))*"'),
        ("integer", r"([+-]|\b)[0-9]+\b"),
        ("identifier", r"\b[a-zA-Z][a-zA-Z0-9_]*\b"),
        ("oparen", r"\("),
        ("cparen", r"\)"),
        ("comma", r","),
        ("whitespace", r"[ \t\r]"),
    ]

    def consume_token(self, action):
        """Consume a token given an action string.

        If there is a valid token at the front of the action string, then it will be
        removed from the string and returned. Otherwise, `None` will be returned as a
        token.

        :param action: an action string
        :type action: str
        :return: a tuple (ActionToken, str) containing the consumed action token and
            the remaining action string.
        """
        for token in self.TOKEN_TYPES:
            # Attempt to match token with action
            match = re.match(token[1], action)
            if match:
                # Consume token
                action = action[match.end(0) :]
                return ActionToken(token[0], match[0]), action

        # No token was found
        return None, action

    def tokenize_action(self, action, filter_out=None):
        """Tokenize an action string.

        Transform an action string into a list of tokens (or raise an exception if an
        invalid token is found).

        :param action: an action string
        :type action: str
        :param filter_out: a list of token types to filter out
        :type filter_out: list
        :return: a list of ActionTokens
        """
        token_list = []
        original_action = action

        # While the action string is not empty, consume tokens
        while action:
            token, action = self.consume_token(action)

            # If no token is found, raise an exception: it means that there is an
            # unknown token in the action string
            if not token:
                raise PaignionActionCompilerException(
                    f"Undefined token `{action[0]}` in `{action}`, in action"
                    f" `{original_action}`"
                )

            # Filter out unwanted tokens
            if token.type not in filter_out:
                token_list.append(token)

        return token_list

    def parse_action(self, action):
        """Parse an action string.

        Parse a given action string an return an ActionNode describing the action that
        needs to be carried out.

        :param action: an action string
        :type action: str
        :return: an ActionNode
        """
        original_action = action
        # Get tokens from action string
        token_list = self.tokenize_action(action, filter_out=["whitespace"])

        while token_list:
            # Call the appropriate parse function based on the first token
            if self.peek("set_func", token_list):
                return self.parse_set_func(token_list)
            elif self.peek("add_func", token_list):
                return self.parse_add_func(token_list)
            elif self.peek("sub_func", token_list):
                return self.parse_sub_func(token_list)
            elif self.peek("mul_func", token_list):
                return self.parse_mul_func(token_list)
            elif self.peek("div_func", token_list):
                return self.parse_div_func(token_list)

            # If we reach this line it means that there is an unrecognized token
            # structure in the action string
            raise PaignionActionCompilerException(
                f"Undefined structure starting with `{token_list[0]}` for action"
                f" `{original_action}`"
            )

    def compile_action(self, action):
        """Compile an action string into JavaScript code to be used in the frontend.

        Compile an action into JavaScript code that can be used by the frontend
        Paignion engine. The element the function will run upon will be determined by
        the function `getRoomOrItem()` implemented in the frontend engine.

        :param action: an action string
        :type action: str
        :return: JavaScript code (in the form of a string)
        """
        action_node = self.parse_action(action)

        if action_node == None:
            return ""

        if action_node.action() == "set":
            return (
                f'getRoomOrItem("{self.strip_quotes(action_node.element)}")'
                f'["{self.strip_quotes(action_node.key)}"] = '
                f"{action_node.value};"
            )
        elif action_node.action() == "add":
            return (
                f'getRoomOrItem("{self.strip_quotes(action_node.element)}")'
                f'["{self.strip_quotes(action_node.key)}"] += '
                f"{action_node.value};"
            )
        elif action_node.action() == "sub":
            return (
                f'getRoomOrItem("{self.strip_quotes(action_node.element)}")'
                f'["{self.strip_quotes(action_node.key)}"] -= '
                f"{action_node.value};"
            )
        elif action_node.action() == "mul":
            return (
                f'getRoomOrItem("{self.strip_quotes(action_node.element)}")'
                f'["{self.strip_quotes(action_node.key)}"] *= '
                f"{action_node.value};"
            )
        elif action_node.action() == "div":
            return (
                f'getRoomOrItem("{self.strip_quotes(action_node.element)}")'
                f'["{self.strip_quotes(action_node.key)}"] /= '
                f"{action_node.value};"
            )

        # If we reach this line, we have come across an unrecognized ActionNode
        raise PaignionActionCompilerException(f"Undefined node: `{action_node}`")

    def parse_set_func(self, token_list):
        """Parse a call to the Paignion set() function from a list of tokens.

        The syntax of the Paignion set function has as follows:
        set(X, Y, Z)
        X: key to set (must be an identifier or a string)
        Y: value to set key to (must be a string or a Markdown string)
        Z: object to which key belongs (must be an identifier or a string)

        :param token_list: a list of tokens
        :type token_list: list
        :return: a populated instance of ActionSetNode
        """
        # Consume the set keyword and the opening parenthesis
        self.consume("set_func", token_list)
        self.consume("oparen", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        # Consume the first comma
        self.consume("comma", token_list)

        # Value, can be integer, Markdown string or simple string
        if self.peek("integer", token_list):
            value = self.parse_integer(token_list)
        elif self.peek("md_string", token_list):
            value = self.parse_md_string(token_list)
        else:
            value = self.parse_string(token_list)

        # Consume the second comma
        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        # Consume the closing parenthesis
        self.consume("cparen", token_list)

        # Return the populated ActionSetNode
        return ActionSetNode(key=key, value=value, element=element)

    def parse_add_func(self, token_list):
        """Parse a call to the Paignion add() function from a list of tokens.

        The syntax of the Paignion add function has as follows:
        add(X, Y, Z)
        X: value to add/append to key's existing value (must be a string or a Markdown
        string)
        Y: key to add/append to (must be an identifier or a string)
        Z: object to which key belongs (must be an identifier or a string)

        :param token_list: a list of tokens
        :type token_list: list
        :return: a populated instance of ActionAddNode
        """
        # Consume the add keyword and the opening parenthesis
        self.consume("add_func", token_list)
        self.consume("oparen", token_list)

        # Value, must be either integer, Markdown string or string
        if self.peek("integer", token_list):
            value = self.parse_integer(token_list)
        elif self.peek("md_string", token_list):
            value = self.parse_md_string(token_list)
        else:
            value = self.parse_string(token_list)

        # Consume the first comma
        self.consume("comma", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        # Consume the second comma
        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        # Consume the closing parenthesis
        self.consume("cparen", token_list)

        # Return the populated ActionAddNode
        return ActionAddNode(key=key, value=value, element=element)

    def parse_sub_func(self, token_list):
        """Parse a call to the Paignion sub() function from a list of tokens.

        The syntax of the Paignion sub function has as follows:
        sub(X, Y, Z)
        X: value to subtract from key's existing value (must be an integer)
        Y: key to subtract from (must be an identifier or a string)
        Z: object to which key belongs (must be an identifier or a string)

        :param token_list: a list of tokens
        :type token_list: list
        :return: a populated instance of ActionSubNode
        """
        # Consume the sub keyword and the opening parenthesis
        self.consume("sub_func", token_list)
        self.consume("oparen", token_list)

        # Value, must be integer
        value = self.parse_integer(token_list)

        # Consume the first comma
        self.consume("comma", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        # Consume the second comma
        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        # Consume the first comma
        self.consume("cparen", token_list)

        # Return the populated ActionSubNode
        return ActionSubNode(key=key, value=value, element=element)

    def parse_mul_func(self, token_list):
        """Parse a call to the Paignion mul() function from a list of tokens.

        The syntax of the Paignion mul function has as follows:
        mul(X, Y, Z)
        X: value to multiply with key's existing value (must be an integer)
        Y: key to multiply with (must be an identifier or a string)
        Z: object to which key belongs (must be an identifier or a string)

        :param token_list: a list of tokens
        :type token_list: list
        :return: a populated instance of ActionMulNode
        """
        # Consume the mul keyword and the opening parenthesis
        self.consume("mul_func", token_list)
        self.consume("oparen", token_list)

        # Value, must be integer
        value = self.parse_integer(token_list)

        # Consume the first comma
        self.consume("comma", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        # Consume the second comma
        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        # Consume the closing parenthesis
        self.consume("cparen", token_list)

        # Return the populated ActionMulNode
        return ActionMulNode(key=key, value=value, element=element)

    def parse_div_func(self, token_list):
        """Parse a call to the Paignion div() function from a list of tokens.

        The syntax of the Paignion div function has as follows:
        div(X, Y, Z)
        X: value to divide with key's existing value (must be an integer)
        Y: key to divide with (must be an identifier or a string)
        Z: object to which key belongs (must be an identifier or a string)

        :param token_list: a list of tokens
        :type token_list: list
        :return: a populated instance of ActionMulNode
        """
        # Consume the div keyword and the opening parenthesis
        self.consume("div_func", token_list)
        self.consume("oparen", token_list)

        # Value, must be integer
        value = self.parse_integer(token_list)

        # Check that value is non-zero
        if value == 0:
            raise PaignionActionCompilerException(
                "div() action with 0 detected, cannot divide by 0"
            )

        # Consume the first comma
        self.consume("comma", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        # Consume the second comma
        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        # Consume the closing parenthesis
        self.consume("cparen", token_list)

        # Return the populated ActionDivNode
        return ActionDivNode(key=key, value=value, element=element)

    def parse_md_string(self, token_list):
        """Parse a Markdown string.

        :param token_list: a list of tokens
        :type token_list: list
        :return: a markdownified (HTML) string with quotes around it
        """
        # Keep the quotes!
        return f'"{markdownify(self.consume("md_string", token_list).value[2:-1])}"'

    def parse_string(self, token_list):
        """Parse a (normal) string.

        :param token_list: a list of tokens
        :type token_list: list
        :return: the string with quotes around it
        """
        # Keep the quotes!
        return str(self.consume("string", token_list).value)

    def parse_identifier(self, token_list):
        """Parse an identifier.

        :param token_list: a list of tokens
        :type token_list: list
        :return: the identifier in string form
        """
        return str(self.consume("identifier", token_list).value)

    def parse_integer(self, token_list):
        """Parse an integer.

        :param token_list: a list of tokens
        :type token_list: list
        :return: the integer (in int form of course)
        """
        return int(self.consume("integer", token_list).value)

    def consume(self, expected_type, token_list):
        """Consume a token of an expected type from a token list.

        If the type of the first token of the token list does not match the expected
        type, raise an exception.

        :param expected_type: the expected token type
        :type expected_type: str
        :param token_list: a list of tokens
        :type token_list: list
        :return: the consumed token
        """
        # If the token list is empty, there's a problem
        if not token_list:
            raise PaignionActionCompilerException(
                f"Expected token type `{expected_type}` but there are no more tokens"
            )

        token = token_list.pop(0)

        if token.type == expected_type:
            return token

        raise PaignionActionCompilerException(
            f"Expected token type `{expected_type}` but got `{token.type}`"
        )

    def peek(self, expected_type, token_list, index=0):
        """Peek into the type of a token in a given token list.

        The type of the i-th token in the token list is compared to the expected type.
        The `i` of course in this case is `index`.

        :param expected_type: the expected token type
        :type expected_type: str
        :param token_list: a list of tokens
        :type token_list: list
        :param index: the index to use in the token list
        :type index: int
        :return: True if the types match, False otherwise
        """
        return token_list[index].type == expected_type

    def strip_quotes(self, string):
        """Strip the quotes off of a string if it has any.

        :param string: a string
        :type string: str
        :return: the same string, but without quotes
        """

        if string[0] in ('"', "'") or string[-1] in ('"', "'"):
            # If there are quotes only on one end, raise an exception
            if not (string[0] in ('"', "'") and string[-1] in ('"', "'")):
                raise PaignionActionCompilerException(
                    f"String `{string}` only has quotes on one side"
                )

            return string[1:-1]

        return string
