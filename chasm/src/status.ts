export interface StatusFile {
  file: string;
  staged: string;
  unstaged: string;
}

export interface StatusGroups {
  staged: StatusFile[];
  unstaged: StatusFile[];
  untracked: StatusFile[];
}

export function parseGitStatus(status: string): StatusFile[] {
  const lines = status.trim().split('\n');
  if (lines.length === 1 && lines[0] === '') return [];

  return lines.map(line => {
    const match = line.match(/^(.)(.) (.+)$/);
    if (!match) return null;
    const [, staged, unstaged, file] = match;
    return { file, staged, unstaged };
  }).filter(Boolean) as StatusFile[];
}

export function groupStatusFiles(statusFiles: StatusFile[]): {
  staged: StatusFile[];
  unstaged: StatusFile[];
  untracked: StatusFile[];
} {
  const staged: StatusFile[] = [];
  const unstaged: StatusFile[] = [];
  const untracked: StatusFile[] = [];

  for (const sf of statusFiles) {
    if (sf.staged !== ' ' && sf.staged !== '?') {
      staged.push(sf);
    }
    if (sf.unstaged !== ' ' && sf.unstaged !== '?') {
      unstaged.push(sf);
    }
    if (sf.staged === '?' && sf.unstaged === '?') {
      untracked.push(sf);
    }
  }

  return { staged, unstaged, untracked };
}
