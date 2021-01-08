---
west: origin
items:
    intangible:
        - name: sink
          description: "A rusty, leaky sink. Doesn't look safe to drink from."
          used_with:
            - name: book
              actions:
                - set(effect, "wet", book)
              effect_message: "The book is now soaking wet. _Nice_."
            - name: coin
              actions:
                - set(effect, "wet", coin)
              effect_message: "Wet coins? Did you _really_ need wet coins?"
---

This is the kitchen of the cabin. Pretty nice, I guess.
