import { useState } from "react";
import { Input } from "./ui/input";
import { RenderResults } from "./RenderResults";
import { Button } from "./ui/button";
import { type GitHubSearchResponse } from "../server/github";
import toast from "react-hot-toast";

function mergeGithubResults(
  results: GitHubSearchResponse[],
): GitHubSearchResponse {
  const total_count = results[0]?.total_count || 0;
  if (total_count === 0) {
    console.warn("this should not be with the total count of 0");
  }
  return {
    total_count,
    incomplete_results: results.some((result) => result.incomplete_results),
    items: results.flatMap((result) => result.items),
  };
}

async function handlePromiseSettled(
  allResultPromises: Promise<GitHubSearchResponse>[],
): Promise<[GitHubSearchResponse[], any[]]> {
  const all = await Promise.allSettled(allResultPromises);
  const succeeded: GitHubSearchResponse[] = all
    .filter((r) => r.status === "fulfilled")
    .map((r) => r.value);
  const rejected = all
    .filter((r) => r.status === "rejected")
    .map((r) => r.reason);
  return [succeeded, rejected];
}

async function callQueryApi(
  query: string,
  per_page: number,
  number_of_pages: number,
): Promise<{ results: GitHubSearchResponse[]; errors: any[] }> {
  const allResultPromises: Array<Promise<GitHubSearchResponse>> = Array.from(
    { length: number_of_pages },
    async (_, page) => {
      return fetch("/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query, per_page, page }),
        credentials: "include",
      }).then((res) => {
        if (!res.ok) {
          throw new Error(
            `HTTP error while fetching page: ${page}! status: ${res.status}`,
          );
        }

        return res.json();
      });
    },
  );

  const [allResults, rejectedResults] =
    await handlePromiseSettled(allResultPromises);
  const incomplete_results = allResults.some((r) => r.incomplete_results);

  return {
    results: allResults,
    errors: rejectedResults,
  };
}

async function saveQueryApi(
  query: string,
  results: GitHubSearchResponse,
): Promise<void> {
  const res = await fetch("/api/save-query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, results }),
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Failed to save query");
  }
}

export function QueryCode() {
  const [query, setQuery] = useState("");
  const [per_page, setPerPage] = useState(30);
  const [number_of_pages, setNumberOfPages] = useState(1);
  const [results, setResults] = useState<GitHubSearchResponse | undefined>(
    undefined,
  );
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) {
      toast.error("Please enter a query");
      return;
    }
    if (number_of_pages > 10) {
      toast("Fetching many pages may take time and hit rate limits", {
        icon: "⚠️",
      });
    }
    setLoading(true);
    try {
      const { results, errors } = await callQueryApi(
        query,
        per_page,
        number_of_pages,
      );
      if (errors.length > 0) {
        console.log("Search failed:", errors);
        toast.error("Search failed: " + errors.join(", "));
        return;
      }
      setResults(mergeGithubResults(results));
      toast.success("Search completed");
    } catch (error) {
      toast.error("Search failed: " + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-card p-6 rounded-lg border shadow-sm">
        <div className="flex">
          <h1 className="text-2xl font-bold mb-4 text-center">
            GitHub Code Search
          </h1>{" "}
          <h3 className="text-sm text-gray-500">
            <a href="/docs">docs</a>
          </h3>
        </div>
        <div className="flex flex-wrap gap-4 items-end justify-center">
          <div className="flex-1 min-w-64">
            <label className="block text-sm font-medium mb-1">Query</label>
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter search query"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Per Page</label>
            <Input
              type="number"
              value={per_page}
              onChange={(e) => setPerPage(Number(e.target.value))}
              min={1}
              max={100}
              className="w-24"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Pages</label>
            <Input
              type="number"
              value={number_of_pages}
              onChange={(e) => setNumberOfPages(Number(e.target.value))}
              min={1}
              max={34} // since 1000 results max / 30 per page ≈ 33.3
              className="w-24"
            />
          </div>
          <Button onClick={handleSearch} disabled={loading} className="px-6">
            {loading ? "Searching..." : "Search"}
          </Button>
        </div>
      </div>
      <RenderResults
        results={results}
        onSave={(results) => saveQueryApi(query, results)}
      />
    </div>
  );
}
