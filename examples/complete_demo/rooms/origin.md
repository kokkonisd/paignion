---
east: kitchen
items:
    intangible:
        - name: painting
          description: A beautiful painting of a cabin in the woods.
        - name: ceiling
          visible: false
        - name: book display
          description: "An old book display. Reads: _insert book here_."
          used_with:
            - name: book
              consumes_subject: true
              consumes_object: true
              actions:
                - set(down, "basement", origin)
                - append("There is a stairwell going down to the basement.", description, origin)
              effect_message: "The book display accepts the book and _sinks into the floor_, revealing a stairwell which fades into the dark of the basement."
    tangible:
        - name: book
          description: An old, dusty book.
        - name: coin
          description: A **gold** coin.
          amount: 3
---

You find yourself in the living room of a cozy little cabin in the woods. On the wall
you can see a painting of the cabin, and on the floor besides the door rests an old,
dusty book.

There is a book display in the middle of the room, probably used to display a very
special book back when this place was more... lively.
