# Plan: Enhance TUI Filtering

## 1. Problem Analysis

The user reports that there is no filtering in the TUI. While the `bubbles/list` component has built-in filtering capabilities (triggered by `/`), it currently only filters on the prompt's `Name`. The filtering experience can be significantly improved by allowing users to filter by `Tags` as well.

## 2. Proposed Solution

The solution is to modify the `FilterValue()` method of the `item` struct in `tui.go`. This method is used by the `list` component to get the string to search against when filtering.

Currently, it is:
```go
func (i item) FilterValue() string { return i.name }
```

It will be updated to return a concatenation of the name and the tags. This will allow the filter to match text in either the name or the tags.

```go
func (i item) FilterValue() string {
	return i.name + " " + strings.Join(i.tags, " ")
}
```

## 3. Implementation Steps

1.  Modify the `item.FilterValue()` method in `tui.go` to include the tags in the filterable value as described above.
2.  To improve user experience and discoverability, the key for filtering will be added to the help menu displayed in the TUI. The default key is `/`.
