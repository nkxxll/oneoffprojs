import {Item} from "../../src/types";

interface BoxChars {
  topLeft: string;
  topRight: string;
  bottomLeft: string;
  bottomRight: string;
  horizontal: string;
  vertical: string;
}

interface Message {
    type: string;
    width?: number;
    height?: number;
    char?: string;
}

type Command = null | Promise<Message>;

interface Model {
    items: Item[];
    selectedIndex: number;
    terminalWidth: number;
    terminalHeight: number;
    mode: "list" | "input";
    input: string;
    cursor: number;
    update: function(Message): [Model, Command];
    view: function(): string;
}
