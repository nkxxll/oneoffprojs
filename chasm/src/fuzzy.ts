import type { Command } from "./subcommand";

export function fuzzySearch(query: string, commands: Command[]): Command[] {
  const results: { command: Command; score: number }[] = [];

  for (const command of commands) {
    const score = fuzzyScore(query, command.title, command.aliases);

    if (score > 0) {
      results.push({ command, score });
    }
  }

  return results
    .sort((a, b) => b.score - a.score)
    .map(({ command }) => command);
}

function levenshteinDistance(a: string, b: string): number {
  const matrix = Array.from({ length: a.length + 1 }, () =>
    Array(b.length + 1).fill(0),
  );

  for (let i = 0; i <= a.length; i++) matrix[i]![0] = i;
  for (let j = 0; j <= b.length; j++) matrix[0]![j] = j;

  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i]![j] = Math.min(
        matrix[i - 1]![j] + 1, // deletion
        matrix[i]![j - 1] + 1, // insertion
        matrix[i - 1]![j - 1] + cost, // substitution
      );
    }
  }

  return matrix[a.length]![b.length];
}

function fuzzyScore(query: string, title: string, aliases: string[]): number {
  const titleDist = levenshteinDistance(
    query.toLowerCase(),
    title.toLowerCase(),
  );
  let minDist = titleDist;
  let isTitle = true;

  for (const alias of aliases) {
    const d = levenshteinDistance(query.toLowerCase(), alias.toLowerCase());
    if (d < minDist) {
      minDist = d;
      isTitle = false;
    }
  }

  let score = 1 / (1 + minDist);
  if (!isTitle) score *= 0.8;

  return score;
}
