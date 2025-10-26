import { parseArgs as bunParseArgs } from "util";

export function parseArgs(argv) {
  const options = {
    help: { type: 'boolean', short: 'h' },
    verbose: { type: 'boolean', short: 'v' },
    quiet: { type: 'boolean', short: 'q' }
  };

  try {
    const { values, positionals } = bunParseArgs({
      args: argv,
      options,
      allowPositionals: true
    });

    return {
      help: values.help || false,
      verbose: values.verbose || false,
      quiet: values.quiet || false,
      configFile: positionals[0] || null
    };
  } catch (error) {
    throw new Error(`Argument parsing error: ${error.message}`);
  }
}
