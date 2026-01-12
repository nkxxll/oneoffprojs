import { readableStreamToText } from "bun";
import { createReadStream, createWriteStream } from "fs";

async function getTTY() {
  const tty = await new Response(
    Bun.spawn({ cmd: ["tty"], stdin: "inherit", stdout: "pipe" }).stdout,
  ).text();
  return tty;
}

const ESC = "\x1b";
const BEL = "\x07";

interface ColorResponse {
  index: number;
  hex: string;
}

function initialParse(chunk: string[]): ColorResponse {
  const index = chunk[1] ? parseInt(chunk[1]) : -1;
  const rgb = chunk[2]
    ?.slice(4)
    .split("/")
    .map((v) => v.slice(2)) ?? ["00", "00", "00"];

  return { index: index, hex: `#${rgb[0]}${rgb[1]}${rgb[2]}` };
}

function parseColorResponse(chunk: string): ColorResponse | null {
  const parts = chunk.split(";");
  if (parts.length !== 3) {
    console.warn(`this shoudl be three parts ${chunk} split by ;`);
    return null;
  }

  return initialParse(parts);
}
async function main() {
  // const tty = await getTTY();
  // const ttyIn = createReadStream(tty.trim());
  // const ttyOut = createWriteStream(tty.trim());

  let buffer = Buffer.alloc(0);

  process.stdin.on("data", (chunk: Buffer) => {
    buffer = Buffer.concat([buffer, chunk]);
    let start = 0;
    while (true) {
      const belIndex = buffer.indexOf(BEL.charCodeAt(0), start);
      if (belIndex === -1) break;
      const responseBuffer = buffer.subarray(start, belIndex);
      const response = responseBuffer.toString("utf16le");
      if (response.startsWith("]4;")) {
        const parsed = parseColorResponse(response);
        if (parsed) {
          process.stdout.write(`color ${parsed.index}: ${parsed.hex}\n`);
        }
      }
      start = belIndex + 1;
    }
    buffer = buffer.subarray(start);
  });

  const indices = Array.from({ length: 16 }, (_, i) => i);
  for (const i of indices) {
    process.stdout.write(`${ESC}]4;${i};?${BEL}`);
  }
}

process.stdin.setRawMode(true);
process.stdin.resume();
main()
  .catch(console.error)
  .then((_) => {
    process.stdin.setRawMode(false);
  });
