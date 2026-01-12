/** Lib for interacting with GitHub Api */

import { getTokenByGithubId, getSession, type Session } from "./db";
import { writeFile, mkdir } from "fs/promises";
import { join } from "path";

export interface GitHubSearchResponse {
  total_count: number;
  incomplete_results: boolean;
  items: GitHubFileItem[];
}

export interface GitHubFileItem {
  name: string;
  path: string;
  sha: string;
  url: string;
  git_url: string;
  html_url: string;
  repository: GitHubRepository;
  score: number;
}

export interface GitHubRepository {
  id: number;
  node_id: string;
  name: string;
  full_name: string;
  private: boolean;
  owner: GitHubOwner;
  html_url: string;
  description: string | null;
  fork: boolean;
  url: string;
  forks_url: string;
  keys_url: string;
  collaborators_url: string;
  teams_url: string;
  hooks_url: string;
  issue_events_url: string;
  events_url: string;
  assignees_url: string;
  branches_url: string;
  tags_url: string;
  blobs_url: string;
  git_tags_url: string;
  git_refs_url: string;
  trees_url: string;
  statuses_url: string;
  languages_url: string;
  stargazers_url: string;
  contributors_url: string;
  subscribers_url: string;
  subscription_url: string;
  commits_url: string;
  git_commits_url: string;
  comments_url: string;
  issue_comment_url: string;
  contents_url: string;
  compare_url: string;
  merges_url: string;
  archive_url: string;
  downloads_url: string;
  issues_url: string;
  pulls_url: string;
  milestones_url: string;
  notifications_url: string;
  labels_url: string;
  releases_url: string;
  deployments_url: string;
}

export interface GitHubOwner {
  login: string;
  id: number;
  node_id: string;
  avatar_url: string;
  gravatar_id: string;
  url: string;
  html_url: string;
  followers_url: string;
  following_url: string;
  gists_url: string;
  starred_url: string;
  subscriptions_url: string;
  organizations_url: string;
  repos_url: string;
  events_url: string;
  received_events_url: string;
  type: string;
  user_view_type: string;
  site_admin: boolean;
}

export async function getUserInfo(githubId: number) {
  const tokenData = getTokenByGithubId(githubId);
  if (!tokenData) {
    throw new Error("No token found for user");
  }
  const response = await fetch("https://api.github.com/user", {
    headers: {
      Authorization: `Bearer ${tokenData.access_token}`,
      Accept: "application/vnd.github.v3+json",
    },
  });
  if (!response.ok) {
    throw new Error(`GitHub API error: ${response.status}`);
  }
  return await response.json();
}

export async function handleQuerySearch(
  request: Request,
  session: Session,
): Promise<Response> {
  const { query, per_page, page } = await request.json();
  if (!query) {
    return Response.json({ error: "Invalid query", status: 400 });
  }

  const tokenData = getTokenByGithubId(session.github_id);
  if (!tokenData) {
    return Response.json({ error: "Couldn't find token", status: 400 });
  }

  const params = new URLSearchParams({ q: query });
  if (per_page !== undefined) {
    params.append("per_page", String(per_page));
  }
  if (page !== undefined) {
    params.append("page", String(page));
  }

  const response = await fetch(
    `https://api.github.com/search/code?${params.toString()}`,
    {
      headers: {
        Authorization: `Bearer ${tokenData.access_token}`,
        Accept: "application/vnd.github.v3+json",
      },
    },
  );
  if (!response.ok) {
    return Response.json({
      error: `GitHub API error: ${response.status}, status: ${response.status}`,
    });
  }
  return Response.json(await response.json());
}

export async function handleSaveQuery(
  request: Request,
  session: Session,
): Promise<Response> {
  if (request.method !== "POST") {
    return Response.json({ error: "Method not allowed" }, { status: 405 });
  }

  try {
    const { query, results } = await request.json();
    if (!query || !results) {
      return Response.json({ error: "Invalid data" }, { status: 400 });
    }

    const savesDir = join(process.cwd(), "saves");
    await mkdir(savesDir, { recursive: true });

    const filename = `query_${Date.now()}.json`;
    const filepath = join(savesDir, filename);

    await writeFile(
      filepath,
      JSON.stringify(
        { query, results, timestamp: new Date().toISOString() },
        null,
        2,
      ),
    );

    return Response.json({ success: true, filename });
  } catch (error) {
    console.error("Error saving query:", error);
    return Response.json({ error: "Internal server error" }, { status: 500 });
  }
}
