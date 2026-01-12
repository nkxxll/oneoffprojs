/** this is a component that references the github api */

const ITEMS = [
  { title: "GitHub API", url: "https://docs.github.com/en/rest" },
  { title: "GitHub GraphQL API", url: "https://docs.github.com/en/graphql" },
  {
    title: "Constructing a search query",
    url: "https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#constructing-a-search-query",
  },
  {
    title: "Searching Code (legacy)",
    url: "https://docs.github.com/en/search-github/searching-on-github/searching-code",
  },
];

interface Item {
  title: string;
  url: string;
}

function renderItem(item: Item) {
  return (
    <li key={item.url} className="mb-2">
      <a
        href={item.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-primary hover:text-primary/80 underline"
      >
        {item.title}
      </a>
    </li>
  );
}

export function Docs() {
  return (
    <div className="max-w-2xl mx-auto p-6 bg-card rounded-lg shadow-md">
      <div className="flex">
        <h1 className="text-2xl font-bold mb-4 text-foreground">
          Documentation Links
        </h1>
        <h3 className="text-sm text-gray-500">
          <a href="/">query</a>
        </h3>
      </div>
      <ul className="list-disc list-inside space-y-2">
        {ITEMS.map(renderItem)}
      </ul>
    </div>
  );
}
