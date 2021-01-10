---
items:
    tangible:
        - name: key
          description: A rusty key. Looks like it could still work though.
    intangible:
        - name: door
          description: A classic wooden door.
          used_with:
            - name: key
              effect_message: The key unlocks the door.
              consumes_subject: true
              actions:
                - set(west, "other_room", full_items_room)
        - name: bathtub
          description: An old bathtub full of acid.
          used_with:
            - name: key
              actions:
                - set(description, m"A cleaned-up key. Some rust marks are still visible, where the acid didn't get to eat away at the rust.", key)
              effect_message: You plunge the key into the acid bath, cleaning it somewhat.
---

description
