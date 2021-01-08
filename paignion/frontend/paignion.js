/** -------------------------------------------------------------------------------------------------------------------
 * Paignion front-end engine.
 * Written by Dimitri Kokkonis (@kokkonisd)
 * --------------------------------------------------------------------------------------------------------------------
 */

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


            case "help":
                return {
                    "action": "help"
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


window.onload = setup();


function setup ()
{
    parser = new Parser();
    currentRoom = getRoom("origin");

    roomDescriptionElement = document.createElement("div");
    roomDescriptionElement.id = "room-description";
    actionFeedbackElement = document.createElement("div");
    actionFeedbackElement.id = "action-feedback";

    let userControls = document.createElement("div");
    userControls.id = "user-controls";
    input = document.createElement("input");
    input.addEventListener("keydown", event => {
        // Avoid firefox bugs?
        if (event.isComposing || event.keyCode === 229) {
            return;
        }

        // If ENTER is pressed
        if (event.keyCode === 13) {
            handleInput();
        }
    });
    button = document.createElement("button")
    button.innerHTML = "submit";
    button.addEventListener("click", e => { handleInput(); });

    userControls.append(input, button);

    let mainElement = document.getElementsByTagName("main")[0];
    mainElement.append(roomDescriptionElement, actionFeedbackElement, userControls);

    setRoomDescription(currentRoom.description);
    input.focus();
}



function setRoomDescription (description)
{
    roomDescriptionElement.innerHTML = description;
}


function setActionFeedback (feedback)
{
    actionFeedbackElement.innerHTML = feedback;
}


function getRoom (room)
{
    return GAME_DATA[room];
}


function handleInput ()
{
    // Parse sentence
    let parsedSentence = parser.parseUserInput(input.value);
    // Clear input field
    input.value = "";

    if (parsedSentence.sentence === "invalid") {
        switch (parsedSentence.reason) {
            case "incomplete":
                setActionFeedback(p(parsedSentence.response));
                break;

            default:
            case "unknown_action":
                setActionFeedback(p("I don't understand that.") + p("If you're really lost, type 'help'."));
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


            case "help":
                help();
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
        // Change room description text
        setRoomDescription(currentRoom.description);
        // Clear feedback text
        setActionFeedback(p(""));
    } else {
        setActionFeedback(p("You cannot go " + direction + "."));
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
            setActionFeedback(p("You've taken " + appropriateWord + " " + item.name + "."));

        } else {
            setActionFeedback(p("There are no more " + item.name + "s in this room you can take."));
        }
    } else if (getItemFromRoom(currentRoom, "intangible", itemName)) {
        setActionFeedback(p("You cannot take that."));
    } else {
        setActionFeedback(p("There aren't any " + itemName + "s in this room."));

        let allItems = currentRoom.items.tangible.concat(currentRoom.items.intangible);
        let tentativeApproximation = parser.canApproximateItemName(allItems, itemName);
        if (tentativeApproximation) {
            setActionFeedback(p("Did you mean to say \"take " + tentativeApproximation + "\"?"));
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

            setActionFeedback(p("You can see the following items in the room:") + p(itemString));
        } else {
            setActionFeedback(p("There are no items you can interact with in this room."));
        }

        return;
    }

    let roomItem = getItemFromRoom(currentRoom, "tangible", itemName);
    if (!roomItem) roomItem = getItemFromRoom(currentRoom, "intangible", itemName);

    if (!roomItem) {
        // There is no such item
        setActionFeedback(p("There are no " + itemName + "s in this room."));

        // Search for similar item names
        let allItems = currentRoom.items.tangible.concat(currentRoom.items.intangible);
        let tentativeApproximation = parser.canApproximateItemName(allItems, itemName);
        if (tentativeApproximation) {
            setActionFeedback(p("Did you mean to say \"look at " + tentativeApproximation + "\"?"));
        }
    } else {
        setActionFeedback(roomItem.description);
    }
}


function handleUseAction (parsedSentence)
{
    let subjectName = parsedSentence.subject;
    let objectName = parsedSentence.object;

    if (!getItemFromInventory(subjectName) && getItemFromRoom(currentRoom, "tangible", subjectName)) {
        setActionFeedback(p("You have to take that first in order to use it."));
        return;
    }

    if (!getItemFromInventory(subjectName)) {
        setActionFeedback(p("You don't have such an item."));
        return;
    }

    if (!getItemFromInventory(objectName) && getItemFromRoom(currentRoom, "tangible", objectName)) {
        setActionFeedback(p("You have to take that first in order to use items with/on it."));
        return;
    }

    if (!getItemFromRoom(currentRoom, "tangible", objectName) &&
        !getItemFromRoom(currentRoom, "intangible", objectName)) {
        setActionFeedback(p("There is no such thing in this room."));
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
        setActionFeedback(p("You cannot use these items together."));
        return;
    }


    // Items can now be used together!

    // Apply actions
    if (useActions.actions) eval(useActions.actions);

    // Update feedback text
    setActionFeedback(useActions.effect_message);
    // Just in case the current room description was just updated, update it too
    setRoomDescription(currentRoom.description);

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
            setActionFeedback(p("There is no such item in your inventory."));

            // Try to suggest similarly named items
            let tentativeApproximation = parser.canApproximateItemName(inventory, itemName);
            if (tentativeApproximation) {
                setActionFeedback(p("Did you mean to say \"examine " + tentativeApproximation + "\"?"));
            }
        } else {
            // Item found, examine it
            let description = item.description;
            if (item.effect) description += p("Effect: " + item.effect);
            setActionFeedback(description);
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

            setActionFeedback(p("You have the following items in your inventory:") + p(itemString) +
                              p("You can get more information on an item by saying \"examine &lt;item name&gt;\"."));
        } else {
            setActionFeedback(p("Your inventory is empty."));
        }
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


function help ()
{
    // Commands: go, take, look, use, inventory, examine, help
    setActionFeedback(p("I see you're kinda lost. Here is a list of the things you can say:") +
                      p("go (north|east|south|west|up|down): move towards a given direction") +
                      p("take &lt;item&gt;: take a given item in the room and add it to your inventory") +
                      p("look (around room|at inventory|at &lt;item&gt;): look around the room, at your inventory or at a specific item") +
                      p("use &lt;item&gt; with &lt;other&gt;item>: use an item from your inventory with another item (from your inventory or the room)") +
                      p("inventory: look at your inventory") +
                      p("examine &lt;item&gt;: examine an item from your inventory") +
                      p("help: display this message"));
}



