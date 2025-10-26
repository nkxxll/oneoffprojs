import { readFile, writeFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import path from 'path';

const FIXTURES_DIR = '.hermes/fixtures';

export async function loadFixture(runName, testIndex) {
  const filePath = getFixturePath(runName, testIndex);
  if (!existsSync(filePath)) return null;
  try {
    const content = await readFile(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    return null;
  }
}

export async function saveFixture(runName, testIndex, response) {
  await mkdir(FIXTURES_DIR, { recursive: true });
  const filePath = getFixturePath(runName, testIndex);
  await writeFile(filePath, JSON.stringify(response, null, 2));
}

export function compareFixture(actual, expected) {
  return JSON.stringify(actual) === JSON.stringify(expected);
}

function getFixturePath(runName, testIndex) {
  const safeName = runName.replace(/[^a-zA-Z0-9]/g, '_');
  return path.join(FIXTURES_DIR, `${safeName}_${testIndex}.json`);
}
