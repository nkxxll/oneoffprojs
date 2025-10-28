/** @import {Model, Command, Message, BoxChars} from "./types.d.ts" */

import { saveFixture } from "../fixtures";

/** @type {BoxChars} */
const BOX_CHARS = {
  topRight: "+",
  topLeft: "+",
  bottomLeft: "+",
  bottomRight: "+",
  horizontal: "-",
  vertical: "|",
};

/**
 * horizontal renders two string
 * @param {string} top - right side
 * @param {string} bottom - left side
 * @returns {string} horizontal rendered string
 */
export function renderHorizontal(top, bottom) {
  return top + "\n" + bottom;
}

/**
 * vertically renders two string
 * @param {string} right - right side
 * @param {string} left - left side
 * @returns {string} vertically rendered string
 */
export function renderVertical(right, left) {
  const [rightWidth, rightHeight] = stringMeasures(right);
  const [leftWidth, leftHeight] = stringMeasures(left);
  const rightSplit = right.split("\n");
  const leftSplit = left.split("\n");
  let output = "";
  if (rightHeight > leftHeight) {
    for (let i = 0; i < rightHeight; i++) {
      const rl = rightSplit[i];
      let ll = "";
      if (i < leftHeight) {
        ll = leftSplit[i];
      }
      output += rl.padEnd(rightWidth, " ") + ll.padEnd(leftWidth, " ") + "\n";
    }
  } else {
    for (let i = 0; i < leftHeight; i++) {
      const ll = leftSplit[i];
      let rl = "";
      if (i < rightHeight) {
        rl = rightSplit[i];
      }
      output += rl.padEnd(leftWidth, " ") + ll.padEnd(rightWidth, " ") + "\n";
    }
  }
  return output;
}

/**
 * returns the max width and the height of a string
 * @param {string} str - input content
 * @returns {[number, number]} - width
 */
export function stringMeasures(str) {
  const split = str.split("\n");
  const height = split.length;
  let width = 0;
  for (let i = 0; i < split.length; i++) {
    const line = split[i];
    width = line.length > width ? line.length : width;
  }
  return [width, height];
}

/**
 * render a box with some content in it
 * @param {BoxChars} boxChars - characters that form the border
 * @param {number} width - width of the content
 * @param {number} height - height of the content
 * @param {string} content - content of the box
 */
export function renderBox(boxChars, width, height, content) {
  const lines = content.split("\n");
  let result = "";

  // Top border
  result +=
    boxChars.topLeft +
    boxChars.horizontal.repeat(width) +
    boxChars.topRight +
    "\n";

  // Content lines
  for (let i = 0; i < height; i++) {
    const line = lines[i] || "";
    const paddedLine = line.padEnd(width, " ");
    result += boxChars.vertical + paddedLine + boxChars.vertical + "\n";
  }

  // Bottom border
  result +=
    boxChars.bottomLeft +
    boxChars.horizontal.repeat(width) +
    boxChars.bottomRight;

  return result;
}

/**
 * Initializes the TUI model with the given items, all folded by default.
 * @param {Item[]} initialItems - The initial array of items without folded state
 * @returns {[Model, Command]} The initial model and optional command
 */
export function init(initialItems) {
  const model = {
    items: initialItems.map((item) => ({
      ...item,
      folded: true,
    })),
    selectedIndex: 0,
    terminalWidth: process.stdout.columns,
    terminalHeight: process.stdout.rows,
    mode: "list",
    input: {
      text: "",
      cursor: 0,
    },
  };
  model.update = (msg) => update(model, msg);
  model.view = () => view(model);
  return [model, null];
}

/**
 * Updates the model based on the given message.
 * @param {Model} model - The current model state
 * @param {Message} msg - The message to process
 * @returns {[Model, Command]} The updated model and optional command
 */
export function update(model, msg) {
  switch (msg.type) {
    case "save_fixture":
      const currentItem = model.items[model.selectedIndex];
      const name = currentItem.runName;
      const idx = currentItem.testIndex;
      const response = currentItem.test.response;
      saveFixture(name, idx, response);
      return [model, null];
    case "move_up":
      if (model.selectedIndex > 0) {
        model.selectedIndex--;
      }
      return [model, null];
    case "move_down":
      if (model.selectedIndex < model.items.length - 1) {
        model.selectedIndex++;
      }
      return [model, null];
    case "toggle_fold":
      const item = model.items[model.selectedIndex];
      item.folded = !item.folded;
      return [model, null];
    case "resize":
      model.terminalWidth = msg.width;
      model.terminalHeight = msg.height;
      return [model, null];
    case "enter_input":
      model.mode = "input";
      return [model, null];
    case "exit_input":
      model.mode = "list";
      model.input.text = "";
      model.input.cursor = 0;
      return [model, null];
    case "input_char":
      if (model.mode === "input") {
        model.input.text =
          model.input.text.slice(0, model.input.cursor) +
          msg.char +
          model.input.text.slice(model.input.cursor);
        model.input.cursor++;
      }
      return [model, null];
    case "backspace":
      if (model.mode === "input" && model.input.cursor > 0) {
        model.input.text =
          model.input.text.slice(0, model.input.cursor - 1) +
          model.input.text.slice(model.input.cursor);
        model.cursor--;
      }
      return [model, null];
    case "submit":
      if (model.mode === "input") {
        // For now, just exit input mode
        model.mode = "list";
      }
      return [model, null];
    case "quit":
      return [model, null];
    default:
      return [model, null];
  }
}

/**
 * Renders the current model state as a string for terminal output.
 * @param {Model} model - The model to render
 * @returns {string} The rendered output string
 */
export function view(model) {
  let output = "";
  for (let i = 0; i < model.items.length; i++) {
    const item = model.items[i];
    const prefix = i === model.selectedIndex ? "> " : "  ";
    const foldIndicator = item.folded ? "▶ " : "▼ ";
    const content = item.folded ? item.foldedContent : item.content;
    const line = prefix + foldIndicator + content + "\n";
    output += line;
  }
  const line =
    "Use ↑↓ to navigate, space to toggle fold, i to input, q to quit";
  const [usageWidth, usageHeight] = stringMeasures(line);
  output += renderBox(BOX_CHARS, usageWidth, usageHeight, line);

  const message = "welcome to the\nbest tool ever";
  const [mw, mh] = stringMeasures(message);

  const inputDisplay =
    "Input: " +
    model.input.text.slice(0, model.input.cursor) +
    "|" +
    model.input.text.slice(model.input.cursor);
  const [iw, ih] = stringMeasures(inputDisplay);

  const [width, height] = stringMeasures(output);
  const leftContent = renderVertical(
    renderBox(BOX_CHARS, width, height, output),
    renderBox(BOX_CHARS, mw, mh, message),
  );
  const fullContent = renderVertical(
    leftContent,
    renderBox(BOX_CHARS, iw, ih, inputDisplay),
  );
  return renderBox(
    BOX_CHARS,
    model.terminalWidth - 2,
    model.terminalHeight - 2,
    fullContent,
  );
}

/**
 * Runs the TUI application loop, handling user input and rendering.
 * @param {Model} initialModel - The starting model state
 * @param {function(Model, Message): [Model, Command]} updateFn - The update function
 * @param {function(Model): string} viewFn - The view function
 */
export function run(initialModel, updateFn, viewFn) {
  let model = initialModel;
  let quit = false;

  // Handle SIGTERM and SIGINT for graceful exit
  const cleanup = () => {
    process.stdout.write("\u001b[2J\u001b[0;0H"); // Clear screen
    process.stdin.setRawMode(false);
    process.stdin.pause();
    process.exit(0);
  };

  process.on("SIGTERM", cleanup);
  process.on("SIGINT", cleanup);

  process.stdin.setRawMode(true);
  process.stdin.resume();

  // Initial render
  process.stdout.write("\u001b[2J\u001b[0;0H"); // Clear screen
  process.stdout.write(viewFn(model));

  // Handle resize
  process.stdout.on("resize", () => {
    const msg = {
      type: "resize",
      width: process.stdout.columns,
      height: process.stdout.rows,
    };
    const [newModel, _command] = updateFn(model, msg);
    model = newModel;
    process.stdout.write("\u001b[2J\u001b[0;0H");
    process.stdout.write(viewFn(model));
  });

  process.stdin.on("data", (key) => {
    if (quit) return;

    let msg;
    if (model.mode === "input") {
      if (key.length === 1) {
        if (key[0] === 13) {
          // Enter
          msg = { type: "submit" };
        } else if (key[0] === 127) {
          // Backspace
          msg = { type: "backspace" };
        } else if (key[0] === 27) {
          // Escape
          msg = { type: "exit_input" };
        } else if (key[0] >= 32 && key[0] <= 126) {
          // Printable chars
          msg = { type: "input_char", char: String.fromCharCode(key[0]) };
        }
      }
    } else {
      // list mode
      // arrow keys have a special utf-16 representation
      if (key.length === 3 && key[0] === 27 && key[1] === 91) {
        if (key[2] === 65) {
          // Up arrow
          msg = { type: "move_up" };
        } else if (key[2] === 66) {
          // Down arrow
          msg = { type: "move_down" };
        }
      } else if (key[0] === "s".charCodeAt(0)) {
        msg = { type: "save_fixture" };
      } else if (key[0] === "j".charCodeAt(0)) {
        msg = { type: "move_down" };
      } else if (key[0] === "k".charCodeAt(0)) {
        msg = { type: "move_up" };
      } else if (key[0] === 32 || key[0] === "l".charCodeAt(0)) {
        // Space
        msg = { type: "toggle_fold" };
      } else if (key[0] === "i".charCodeAt(0)) {
        msg = { type: "enter_input" };
      } else if (key[0] === 113 || key[0] === 81 || key[0] === 3) {
        // 'q' or 'Q' or <ctrl-c>
        msg = { type: "quit" };
        quit = true;
      } else {
        return; // Ignore other keys
      }
    }

    if (msg) {
      const [newModel, command] = updateFn(model, msg);
      model = newModel;
      if (command) {
        // Handle command if present (not implemented yet)
      }

      if (!quit) {
        process.stdout.write("\u001b[2J\u001b[0;0H"); // Clear screen
        process.stdout.write(viewFn(model));
      } else {
        process.stdout.write("\u001b[2J\u001b[0;0H"); // Clear screen
        process.stdin.setRawMode(false);
        process.stdin.pause();
      }
    }
  });
}
