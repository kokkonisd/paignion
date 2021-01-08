import re

from paignion.exception import PaignionException
from paignion.tools import markdownify


class ActionToken(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"{self.type.upper()}_TOKEN (`{self.value}`)"

    def __repr__(self):
        return self.__str__()


class ActionSetNode(object):
    def __init__(self, key, value, element):
        self.key = key
        self.value = value
        self.element = element

    def action(self):
        return "set"

    def __str__(self):
        return f"{self.action().upper()}_NODE({self.key}, {self.value}, {self.element})"


class ActionAddNode(ActionSetNode):
    def action(self):
        return "add"


class ActionSubNode(ActionSetNode):
    def action(self):
        return "sub"


class ActionMulNode(ActionSetNode):
    def action(self):
        return "mul"


class ActionDivNode(ActionSetNode):
    def action(self):
        return "div"


class ActionCompiler(object):
    TOKEN_TYPES = [
        ("set_func", r"set"),
        ("add_func", r"add"),
        ("sub_func", r"sub"),
        ("mul_func", r"mul"),
        ("div_func", r"div"),
        ("md_string", r'm"(([^"\\])|(\\"))*"'),
        ("string", r'"(([^"\\])|(\\"))*"'),
        ("integer", r"[0-9]+"),
        ("identifier", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ("oparen", r"\("),
        ("cparen", r"\)"),
        ("comma", r","),
        ("whitespace", r"[ \t\r]"),
    ]

    def consume_token(self, action):
        for token in self.TOKEN_TYPES:
            # Attempt to match action
            match = re.match(token[1], action)
            if match:
                # Consume token
                action = action[match.end(0) :]
                return ActionToken(token[0], match[0]), action

        return None, action

    def tokenize_action(self, action, filter_out=None):
        token_list = []
        original_action = action

        while action:
            token, action = self.consume_token(action)

            if not token:
                raise PaignionException(
                    f"Undefined token `{action[0]}` in `{action}`, in action"
                    f" `{original_action}`"
                )

            if token.type not in filter_out:
                token_list.append(token)

        return token_list

    def parse_action(self, action):
        original_action = action
        token_list = self.tokenize_action(action, filter_out=["whitespace"])

        while token_list:
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

            raise PaignionException(
                f"Undefined structure starting with `{token_list[0]}` for action"
                f" `{original_action}`"
            )

    def compile_action(self, action):
        action_node = self.parse_action(action)

        if action_node.action() == "set":
            return (
                f'getRoomOrItem("{action_node.element}")["{action_node.key}"] = '
                f"{action_node.value};"
            )
        elif action_node.action() == "add":
            return (
                f'getRoomOrItem("{action_node.element}")["{action_node.key}"] += '
                f"{action_node.value};"
            )
        elif action_node.action() == "sub":
            return (
                f'getRoomOrItem("{action_node.element}")["{action_node.key}"] -= '
                f"{action_node.value};"
            )
        elif action_node.action() == "mul":
            return (
                f'getRoomOrItem("{action_node.element}")["{action_node.key}"] *= '
                f"{action_node.value};"
            )
        elif action_node.action() == "div":
            return (
                f'getRoomOrItem("{action_node.element}")["{action_node.key}"] /= '
                f"{action_node.value};"
            )

        raise PaignionException(f"Undefined node: `{action_node}`")

    def parse_set_func(self, token_list):
        self.consume("set_func", token_list)
        self.consume("oparen", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        self.consume("comma", token_list)

        # Value, can be integer, Markdown string or simple string
        if self.peek("integer", token_list):
            value = self.parse_integer(token_list)
        elif self.peek("md_string", token_list):
            value = self.parse_md_string(token_list)
        else:
            value = self.parse_string(token_list)

        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        self.consume("cparen", token_list)

        return ActionSetNode(key=key, value=value, element=element)

    def parse_add_func(self, token_list):
        self.consume("add_func", token_list)
        self.consume("oparen", token_list)

        # Value, must be either integer, Markdown string or string
        if self.peek("integer", token_list):
            value = self.parse_integer(token_list)
        elif self.peek("md_string", token_list):
            value = self.parse_md_string(token_list)
        else:
            value = self.parse_string(token_list)

        self.consume("comma", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        self.consume("cparen", token_list)

        return ActionAddNode(key=key, value=value, element=element)

    def parse_sub_func(self, token_list):
        self.consume("sub_func", token_list)
        self.consume("oparen", token_list)

        # Value, must be integer
        value = self.parse_integer(token_list)

        self.consume("comma", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        self.consume("cparen", token_list)

        return ActionSubNode(key=key, value=value, element=element)

    def parse_mul_func(self, token_list):
        self.consume("mul_func", token_list)
        self.consume("oparen", token_list)

        # Value, must be integer
        value = self.parse_integer(token_list)

        self.consume("comma", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        self.consume("cparen", token_list)

        return ActionMulNode(key=key, value=value, element=element)

    def parse_div_func(self, token_list):
        self.consume("div_func", token_list)
        self.consume("oparen", token_list)

        # Value, must be integer
        value = self.parse_integer(token_list)

        if value == 0:
            raise PaignionException("div() call with 0 detected, cannot divide by 0")

        self.consume("comma", token_list)

        # Key, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            key = self.parse_string(token_list)
        else:
            key = self.parse_identifier(token_list)

        self.consume("comma", token_list)

        # Element, can be string or identifier (based on if it has spaces or not)
        if self.peek("string", token_list):
            element = self.parse_string(token_list)
        else:
            element = self.parse_identifier(token_list)

        self.consume("cparen", token_list)

        return ActionDivNode(key=key, value=value, element=element)

    def parse_md_string(self, token_list):
        # Keep the quotes!
        return f'"{markdownify(self.consume("md_string", token_list).value[2:-1])}"'

    def parse_string(self, token_list):
        # Keep the quotes!
        return f'"{self.consume("string", token_list).value[1:-1]}"'

    def parse_identifier(self, token_list):
        return str(self.consume("identifier", token_list).value)

    def parse_integer(self, token_list):
        return int(self.consume("int", token_list).value)

    def consume(self, expected_type, token_list):
        token = token_list.pop(0)

        if token.type == expected_type:
            return token

        raise PaignionException(
            f"Expected token type `{expected_type}` but got `{token.type}`"
        )

    def peek(self, expected_type, token_list, index=0):
        return token_list[index].type == expected_type
