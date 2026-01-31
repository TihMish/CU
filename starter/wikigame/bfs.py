from collections import deque
from typing import Optional, List


class SearchResult:
    def __init__(self, path: List[str], visited_pages: int):
        self.path = path
        self.visited_pages = visited_pages


class LinkProvider:
    def get_links(self, title: str) -> List[str]:
        raise NotImplementedError()


def find_path_bfs(
    start: str,
    goal: str,
    link_provider: LinkProvider,
    max_depth: int = 4,
    max_pages: int = 300,
) -> Optional[SearchResult]:

    if start == goal:
        return SearchResult([start], 0)

    queue = deque([(start, 0)])
    parents: dict[str, Optional[str]] = {start: None}
    visited_pages = 0

    while queue:
        current, depth = queue.popleft()
        visited_pages += 1

        if visited_pages > max_pages:
            return None

        if depth >= max_depth:
            continue

        try:
            links = link_provider.get_links(current)
        except Exception:
            continue

        for link in links:
            if link in parents:
                continue

            parents[link] = current

            if link == goal:
                path = []
                node = goal
                while node is not None:
                    path.append(node)
                    node = parents[node]
                return SearchResult(path[::-1], visited_pages)

            queue.append((link, depth + 1))

    return None


bfs = find_path_bfs
