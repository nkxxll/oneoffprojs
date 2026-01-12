import { useState } from "react";
import type { GitHubSearchResponse } from "../server/github";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import toast from "react-hot-toast";

export interface RenderResultsProps {
  results: GitHubSearchResponse | undefined;
  onSave: (result: GitHubSearchResponse) => Promise<void>;
}

export function RenderResults({ results, onSave }: RenderResultsProps) {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSave = async () => {
    try {
      if (!results) {
        toast.error("Result is undefined and cannot be saved");
        return;
      }
      await onSave(results);
      toast.success("Query saved successfully!");
    } catch (error) {
      toast.error("Failed to save query: " + (error as Error).message);
    }
  };

  console.log("results", results);
  const filteredItems =
    results?.items.filter(
      (item) =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.path.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.repository.full_name
          .toLowerCase()
          .includes(searchTerm.toLowerCase()),
    ) || [];

  return (
    <>
      {results ? (
        <div className="bg-card p-6 rounded-lg border shadow-sm">
          <div className="mb-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <p className="text-sm text-muted-foreground">
                Total results: {results.total_count}
                {results.incomplete_results && " (incomplete results)"}
              </p>
              <p className="text-sm text-muted-foreground">
                Showing: {filteredItems.length} / {results.items.length}
              </p>
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="Filter results..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-64"
              />
              <Button onClick={handleSave}>Save Query</Button>
            </div>
          </div>
          <div className="max-h-96 overflow-y-auto border rounded">
            <table className="min-w-full border-collapse">
              <thead className="bg-muted sticky top-0">
                <tr>
                  <th className="border-b px-4 py-2 text-left">Name</th>
                  <th className="border-b px-4 py-2 text-left">Path</th>
                  <th className="border-b px-4 py-2 text-left">Repository</th>
                  <th className="border-b px-4 py-2 text-left">Score</th>
                  <th className="border-b px-4 py-2 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredItems.map((item, index) => (
                  <tr key={index} className="hover:bg-muted/50">
                    <td className="border-b px-4 py-2">{item.name}</td>
                    <td className="border-b px-4 py-2">{item.path}</td>
                    <td className="border-b px-4 py-2">
                      {item.repository.full_name}
                    </td>
                    <td className="border-b px-4 py-2">
                      {item.score.toFixed(2)}
                    </td>
                    <td className="border-b px-4 py-2">
                      <a
                        href={item.html_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary hover:underline"
                      >
                        View
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="text-center text-muted-foreground">
          No search results...
        </div>
      )}
    </>
  );
}
