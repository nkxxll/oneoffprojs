export interface StatusFile {
  file: string;
  staged: string;
  unstaged: string;
}

export interface BranchInfo {
  branch: string;
  ahead: number;
  behind: number;
}

export interface StatusGroups {
  branch: BranchInfo;
  staged: StatusFile[];
  unstaged: StatusFile[];
  untracked: StatusFile[];
}

export function parseGitStatus(status: string): { branchInfo: BranchInfo; statusFiles: StatusFile[] } {
  const lines = status.split("\n");
  let branchInfo: BranchInfo = { branch: "", ahead: 0, behind: 0 };
  const statusLines: string[] = [];

  for (const line of lines) {
    if (line.startsWith("## ")) {
      // Parse branch info: ## branch...remote [ahead N, behind M]
      const match = line.match(/^## (.+?)\\.\\.(.+?) \\[(.+)\\]$/);
      if (match) {
        const [, branch, , status] = match;
        const aheadMatch = status.match(/ahead (\d+)/);
        const behindMatch = status.match(/behind (\d+)/);
        branchInfo = {
          branch,
          ahead: aheadMatch ? parseInt(aheadMatch[1]) : 0,
          behind: behindMatch ? parseInt(behindMatch[1]) : 0,
        };
      } else {
        // No ahead/behind
        const match2 = line.match(/^## (.+)$/);
        if (match2) {
          branchInfo.branch = match2[1];
        }
      }
    } else if (line.trim()) {
      statusLines.push(line);
    }
  }

  const statusFiles = statusLines
    .map((line) => {
      const match = line.match(/^(.)(.) (.+)$/);
      if (!match) return null;
      const [, staged, unstaged, file] = match;
      return { file, staged, unstaged };
    })
    .filter(Boolean) as StatusFile[];

  return { branchInfo, statusFiles };
}

export function groupStatusFiles({ branchInfo, statusFiles }: { branchInfo: BranchInfo; statusFiles: StatusFile[] }): StatusGroups {
  const staged: StatusFile[] = [];
  const unstaged: StatusFile[] = [];
  const untracked: StatusFile[] = [];

  for (let i = 0; i < statusFiles.length; i++) {
    const sf = statusFiles[i]!;
    if (sf.staged !== " " && sf.staged !== "?") {
      staged.push(sf);
    }
    if (sf.unstaged !== " " && sf.unstaged !== "?") {
      unstaged.push(sf);
    }
    if (sf.staged === "?" && sf.unstaged === "?") {
      untracked.push(sf);
    }
  }

  return { branch: branchInfo, staged, unstaged, untracked };
}
