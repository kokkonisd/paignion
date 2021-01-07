/** -------------------------------------------------------------------------------------------------------------------
 * Paignion front-end engine.
 * Written by Dimitri Kokkonis (@kokkonisd)
 * --------------------------------------------------------------------------------------------------------------------
 */


// Room description text (shown first on the webpage)
let roomDescriptionText = "";
// Action feedback text (shown below the room description text on the webpage) to inform the user on the effects of
// their actions
let actionFeedbackText = "";

// <div> element holding all the room description text
let roomDescriptionElement;
// <div> element holding all the action feedback text
let actionFeedbackElement;

// Text input field
let input;
// Button to submit input
let button;

// Global parser for user input & commands (encoded in the game object itself)
let parser;

// Variable to hold the room the user is currently in
let currentRoom;
// Array to hold the user's inventory
let inventory = [];


function setup ()
{
    noCanvas();

    roomDescriptionElement = createElement("div", " ").class("room-description");
    actionFeedbackElement = createElement("div", " ").class("action-feedback");

    let userControls = createDiv().class("user-controls");
    input = createInput().parent(userControls);
    button = createButton("submit").parent(userControls);

    button.mousePressed(handleInput);

    currentRoom = getRoom("origin");

    input.elt.focus();

    parser = new Parser();
}


function draw ()
{
    background('black');
    roomDescriptionText = currentRoom.description;

    roomDescriptionElement.html(roomDescriptionText);
    actionFeedbackElement.html(actionFeedbackText);
}


function getRoom (room)
{
    return GAME_DATA[room];
}


function handleInput ()
{
    // Parse sentence
    let parsedSentence = parser.parseUserInput(input.value());
    // Clear input field
    input.value("");

    if (parsedSentence.sentence === "invalid") {
        switch (parsedSentence.reason) {
            case "incomplete":
                actionFeedbackText = p(parsedSentence.response);
                break;

            default:
            case "unknown_action":
                actionFeedbackText = p("I don't understand that.");
                break;
        }
    } else {
        switch (parsedSentence.action) {
            case "go":
                handleGoAction(parsedSentence);
                break;


            case "take":
                handleTakeAction(parsedSentence);
                break;


            case "look":
                handleLookAction(parsedSentence);
                break;


            case "use":
                handleUseAction(parsedSentence);
                break;


            case "inventory":
            case "examine":
                handleInventoryAction(parsedSentence);
                break;


            default:
                throw Error("[paignion:frontend] Invalid action \"" + parsedSentence.action + "\"");
                break;
        }
    }
}


function handleGoAction (parsedSentence)
{
    let direction = parsedSentence.direction;

    if (currentRoom[direction]) {
        // Change room
        currentRoom = getRoom(currentRoom[direction]);
        // Clear feedback text
        actionFeedbackText = p("");
    } else {
        actionFeedbackText = p("You cannot go " + direction + ".");
    }
}


function handleTakeAction (parsedSentence)
{
    let itemName = parsedSentence.subject;

    if (getItemFromRoom(currentRoom, "tangible", itemName)) {
        let item = getItemFromRoom(currentRoom, "tangible", itemName);
        
        if (item.amount === "inf" || item.amount > 0) {
            if (getItemFromInventory(item.name)) {
                // Item already in inventory, increase its amount
                getItemFromInventory(item.name).amount++;
            } else {
                // Copy item in inventory
                inventory.push(JSON.parse(JSON.stringify(item)));
                getItemFromInventory(item.name).amount = 1;
            }

            // Decrease number of items
            item.amount = item.amount === "inf" ? "inf" : item.amount - 1;
            if (item.amount === 0) {
                // Remove item from room
                currentRoom.items.tangible = currentRoom.items.tangible.filter(i => {
                    return i != item;
                });
            }

            // Give the user some feedback, letting them know that they have successfully picked up the
            // item
            let appropriateWord = "the";
            if (item.amount === "inf" || item.amount > 0) {
                appropriateWord = parser.startsWithVowelSound(item.name) ? "an" : "a";
            }
            actionFeedbackText = p("You've taken " + appropriateWord + " " + item.name + ".");

        } else {
            actionFeedbackText = p("There are no more " + item.name + "s in this room you can take.");
        }
    } else if (getItemFromRoom(currentRoom, "intangible", itemName)) {
        actionFeedbackText = p("You cannot take that.");
    } else {
        actionFeedbackText = p("There aren't any " + itemName + "s in this room.");

        let allItems = currentRoom.items.tangible.concat(currentRoom.items.intangible);
        let tentativeApproximation = parser.canApproximateItemName(allItems, itemName);
        if (tentativeApproximation) {
            actionFeedbackText = p("Did you mean to say \"take " + tentativeApproximation + "\"?")
        }
    }
}


function handleLookAction (parsedSentence)
{
    let itemName = parsedSentence.subject;

    if (itemName === "inventory") {
        handleInventoryAction({ "action": "inventory" });
        return;
    } else if (itemName === "room") {
        // List items in the room
        let itemList = currentRoom.items.tangible.concat(currentRoom.items.intangible);

        // Get only visible items
        itemList = itemList.filter(i => {
            return i.visible;
        });
        
        if (itemList.length > 0) {
            // Get item names and amounts
            let itemNames = itemList.map(i => {
                if (i.amount === "inf") {
                    let res = "a lot of " + i.name + "s";
                    if (i.effect) res += " (" + i.effect + ")";
                    return res;
                }

                let res = i.amount === 1 ? "1 " + i.name : i.amount + " " + i.name + "s";
                if (i.effect) res += " (" + i.effect + ")";
                return res;
            });

            let itemString = itemNames.join(", ");
            itemString = itemString[0].toUpperCase() + itemString.slice(1) + ".";

            actionFeedbackText = p("You can see the following items in the room:") + p(itemString);
        } else {
            actionFeedbackText = p("There are no items you can interact with in this room.");
        }

        return;
    }

    let roomItem = getItemFromRoom(currentRoom, "tangible", itemName);
    if (!roomItem) roomItem = getItemFromRoom(currentRoom, "intangible", itemName);

    if (!roomItem) {
        // There is no such item
        actionFeedbackText = p("There are no " + itemName + "s in this room.");

        // Search for similar item names
        let allItems = currentRoom.items.tangible.concat(currentRoom.items.intangible);
        let tentativeApproximation = parser.canApproximateItemName(allItems, itemName);
        if (tentativeApproximation) {
            actionFeedbackText = p("Did you mean to say \"look at " + tentativeApproximation + "\"?");
        }
    } else {
        actionFeedbackText = roomItem.description;
    }
}


function handleUseAction (parsedSentence)
{
    let subjectName = parsedSentence.subject;
    let objectName = parsedSentence.object;

    if (!getItemFromInventory(subjectName) && getItemFromRoom(currentRoom, "tangible", subjectName)) {
        actionFeedbackText = p("You have to take that first in order to use it.");
        return;
    }

    if (!getItemFromInventory(subjectName)) {
        actionFeedbackText = p("You don't have such an item.");
        return;
    }

    if (!getItemFromInventory(objectName) && getItemFromRoom(currentRoom, "tangible", objectName)) {
        actionFeedbackText = p("You have to take that first in order to use items with/on it.");
        return;
    }

    if (!getItemFromRoom(currentRoom, "tangible", objectName) &&
        !getItemFromRoom(currentRoom, "intangible", objectName)) {
        actionFeedbackText = p("There is no such thing in this room.");
        return;
    }


    // Get subject from inventory
    let subject = getItemFromInventory(subjectName);
    
    // Object is either in inventory or in the room
    let object = getItemFromInventory(objectName);
    let objectComesFromInventory = true;

    if (!object) {
        object = getItemFromRoom(currentRoom, "intangible", objectName);
        objectComesFromInventory = false;
    }

    // Attempt to fetch "used_with" key from object first
    let useActions = isXUsedWithY(subject, object);
    // If again not found on the subject or if it is not associated to the object, the two items cannot be used
    // together
    if (!useActions) useActions = isXUsedWithY(object, subject);

    if (!useActions) {
        actionFeedbackText = p("You cannot use these items together.");
        return;
    }


    // Items can now be used together!

    // Apply actions
    if (useActions.actions) applyCommands(useActions.actions);

    // Update feedback text
    actionFeedbackText = useActions.effect_message;

    // Remove subject & object if necessary
    if (useActions.consumes_subject) {
        // Decrease subject amount
        subject.amount = subject.amount === "inf" ? "inf" : subject.amount - 1;

        if (subject.amount === 0) {
            inventory = inventory.filter(i => {
                return i !== subject;
            });
        }
    }

    if (useActions.consumes_object) {
        // Decrease object amount
        object.amount = object.amount === "inf" ? "inf" : object.amount - 1;

        if (object.amount === 0) {
            if (objectComesFromInventory) {
                inventory = inventory.filter(i => {
                    return i !== object;
                });
            } else {
                currentRoom.items.intangible = currentRoom.items.intangible.filter(i => {
                    return i !== object;
                });
            }
        }
    }
}


function handleInventoryAction (parsedSentence)
{
    // Examine specific inventory item
    if (parsedSentence.action === "examine") {
        let itemName = parsedSentence.subject;

        let item = getItemFromInventory(itemName);

        if (!item) {
            actionFeedbackText = p("There is no such item in your inventory.");

            // Try to suggest similarly named items
            let tentativeApproximation = parser.canApproximateItemName(inventory, itemName);
            if (tentativeApproximation) {
                actionFeedbackText = p("Did you mean to say \"examine " + tentativeApproximation + "\"?");
            }
        } else {
            // Item found, examine it
            actionFeedbackText = item.description;
            if (item.effect) actionFeedbackText += p("Effect: " + item.effect);
        }

    // Simply list inventory items
    } else {
        if (inventory.length > 0) {
            let itemNames = inventory.map(i => {
                let res = i.amount === 1 ? "1 " + i.name : i.amount + " " + i.name + "s";
                if (i.effect) res += " (" + i.effect + ")";
                return res;
            });


            let itemString = itemNames.join(", ") + ".";
            itemString = itemString[0].toUpperCase() + itemString.slice(1);

            actionFeedbackText = p("You have the following items in your inventory:") + p(itemString) +
                                 p("You can get more information on an item by saying \"examine &lt;item name&gt;\".");
        } else {
            actionFeedbackText = p("Your inventory is empty.");
        }
    }
}


function keyPressed ()
{
    if (keyCode === ENTER) {
        handleInput();
    }
}


function p (string)
{
    return "<p>" + string + "</p>";
}


function isXUsedWithY (x, y)
{
    if (!y.used_with) return null;

    let usedWithItemNames = y.used_with.filter(i => {
        return i.name === x.name;
    });

    if (usedWithItemNames.length == 0) return null;

    return usedWithItemNames[0];
}


function getItemFromRoom (room, type, itemName)
{
    if (type === "tangible") {
        return currentRoom.items.tangible.find(i => {
            return i.name === itemName;
        });
    } else {
        return currentRoom.items.intangible.find(i => {
            return i.name === itemName;
        });
    }
}


function getItemFromInventory (itemName)
{
    return inventory.find(i => {
        return i.name === itemName;
    });
}


function getRoomOrItem (element)
{
    // First, try to get a room name
    let result = getRoom(element);

    // Second, try to get an item from the inventory
    if (!result) result = getItemFromInventory(element);

    // Third, try to get an (intangible) item from the current room
    if (!result) result = getItemFromRoom(currentRoom, "intangible", element);

    // Fourth, try to get an (intangible) item from the other rooms
    if (!result) {
        let otherRooms = Object.keys(GAME_DATA).filter(r => {
            return r != currentRoom;
        });

        for (let i = 0; i < otherRooms.length; i++) {
            result = getItemFromRoom(otherRooms[i], "intangible", element);
            if (result) break;
        }
    }

    return result;
}


function applyCommands (sentence)
{
    let commands = parser.parseCommands(sentence);

    for (let i = 0; i < commands.length; i++) {
        switch (commands[i].command) {
            case "set":
                commands[i].element[commands[i].key] = commands[i].value;
                break;

            case "add":
                commands[i].element[commands[i].key] += commands[i].value;
                break;

            default:
                throw Error("[paignion:frontend] Unknown command \"" + commands[i].command + "\"");
        }
    }
}



class Parser {
    constructor ()
    {
        this.stopWords = [
            "to",
            "the",
            "towards",
            "on",
            "at",
            "out",
            "around",
            "with",
            "into",
            "in"
        ];
    }

    parseUserInput (sentence)
    {
        let tokens = this.getInputTokens(sentence);

        if (!tokens.action) {
            return {
                "sentence": "invalid",
                "reason": "no_action"
            };
        }

        switch (tokens.action) {
            case "go":
            case "move":
            case "walk":
            case "run":
                if (!tokens.subject) {
                    return {
                        "sentence": "invalid",
                        "reason": "incomplete",
                        "response": tokens.action[0].toUpperCase() + tokens.action.slice(1) + " where?"
                    };
                }
                
                return {
                    "sentence": "valid",
                    "action": "go",
                    "direction": tokens.subject
                };


            case "take":
            case "pick":
            case "get":
                if (!tokens.subject) {
                    return {
                        "sentence": "invalid",
                        "reason": "incomplete",
                        "response": tokens.action[0].toUpperCase() + tokens.action.slice(1) + " what?"
                    };
                }
                return {
                    "action": "take",
                    "subject": tokens.subject
                };


            case "look":
            case "check":
                if (!tokens.subject) {
                    return {
                        "sentence": "invalid",
                        "reason": "incomplete",
                        "response": tokens.action[0].toUpperCase() + tokens.action.slice(1) +
                                    (tokens.action === "look" ? " at what?" : " out what?")
                    };
                }

                return {
                    "action": "look",
                    "subject": tokens.subject
                };


            case "use":
            case "combine":
            case "insert":
            case "put":
                if (!tokens.subject || !tokens.object) {
                    let subjectPlaceholder = tokens.subject ? tokens.subject : "what";
                    let objectPlaceholder = tokens.object ? tokens.object : "what";
                    
                    let middleWord = " on ";
                    if (tokens.action == "combine") middleWord = " with ";
                    if (tokens.action == "insert") middleWord = " into ";

                    return {
                        "sentence": "invalid",
                        "reason": "incomplete",
                        "response": tokens.action[0].toUpperCase() + tokens.action.slice(1) +
                                    " " + subjectPlaceholder + middleWord + objectPlaceholder + "?"
                    };
                }

                return {
                    "action": "use",
                    "subject": tokens.subject,
                    "object": tokens.object
                };


            case "inventory":
                return {
                    "action": "inventory"
                };


            case "examine":
                if (!tokens.subject) {
                    return {
                        "sentence": "invalid",
                        "reason": "incomplete",
                        "response": "Examine what?"
                    };
                }

                return {
                    "action": "examine",
                    "subject": tokens.subject
                };


            default:
                return {
                    "sentence": "invalid",
                    "reason": "unknown_action"
                };
        }
    }


    getInputTokens (sentence)
    {
        let words = sentence.split(" ");
        // Filter out empty words
        words = words.filter(w => {
            return w.length > 0;
        });

        let tokens = { "action": null, "subject": null, "object": null };
        let i = 0;

        // First word should be the action to perform
        tokens.action = words[0];

        // Skip any stop words
        i = 1;
        while (this.stopWords.indexOf(words[i]) >= 0 && i < words.length) i++;

        // All the following words contain the subject
        let subjectWords = []
        while (this.stopWords.indexOf(words[i]) < 0 && i < words.length) {
            subjectWords.push(words[i]);
            i++;
        }
        if (subjectWords.length > 0) tokens.subject = subjectWords.join(" ");

        // There may be more stop words
        while (this.stopWords.indexOf(words[i]) >= 0 && i < words.length) i++;

        // All the following words contain the object
        let objectWords = []
        while (this.stopWords.indexOf(words[i]) < 0 && i < words.length) {
            objectWords.push(words[i]);
            i++;
        }
        if (objectWords.length > 0) tokens.object = objectWords.join(" ");

        return tokens;
    }


    parseCommands (sentence)
    {
        let commands = sentence.split(";");
        // Filter out empty commands
        commands = commands.filter(c => {
            return c.length > 0;
        });

        let commandTokens = [];

        for (let i = 0; i < commands.length; i++) {
            let words = commands[i].split(" ");
            // Filter out empty words
            words = words.filter(w => {
                return w.length > 0;
            });

            // Possible commands:
            // set <key> to <value> for <room/item>
            // add <value> to <key> for <room/item>

            switch (words[0]) {
                case "set":
                    if (words.length < 6 || words[2] !== "to" || words[words.length - 2] !== "for") {
                        throw Error("[paignion:frontend] Syntax error for set command: " + commands[i]);
                    }

                    commandTokens.push({
                        "command": "set",
                        "element": getRoomOrItem(words[words.length - 1]),
                        "key": words[1],
                        "value": words.slice(3, words.length - 2).join(" ")
                    });
                    break;


                case "add":
                    if (words.length < 6 || words[words.length - 4] !== "to" || words[words.length - 2] !== "for") {
                        throw Error("[paignion:frontend] Syntax error for add command: " + commands[i]);
                    }

                    commandTokens.push({
                        "command": "add",
                        "element": getRoomOrItem(words[words.length - 1]),
                        "key": words[words.length - 3],
                        "value": words.slice(1, words.length - 4).join(" ")
                    });
                    break;


                default:
                    throw Error("[paignion:frontend] Unknown command \"" + words[0] + "\"");
            }
        }

        return commandTokens;
    }


    startsWithVowelSound (string)
    {
        let letter = string[0];

        let lowerVowels = ['a', 'e', 'i', 'o', 'u'];
        let upperVowels = ['A', 'E', 'H', 'I', 'L', 'M', 'N', 'O', 'R', 'S', 'X'];

        if (lowerVowels.indexOf(letter) >= 0) {
            return true;
        }

        if (string === string.toUpperCase()) {
            // String is an acronym
            if (upperVowels.indexOf(letter) >= 0) {
                return true;
            }
        }


        return false;
    }


    canApproximateItemName(itemList, itemName)
    {
        // Get all possible items whose name might overlap with the item the user has specified
        let approximateItems = itemList.filter(i => {
            return i.name.indexOf(itemName) >= 0 || itemName.indexOf(i.name) >= 0;
        });

        // If there are any, return their names
        if (approximateItems.length > 0) {
            return approximateItems.map(i => { return i.name; }).join("/");
        } else {
            return null;
        }
    }
}
