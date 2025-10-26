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

/**
 * Save a fixture to the fixture path
 * @param {string} runName - name of the run
 * @param {number} testIndex - index of the test
 * @param {object} response - response object of the run
 */
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
