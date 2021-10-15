import random
from collections import defaultdict



class Graph:
    def __init__(self):
        #nmid = skuespillerid
        #ttid = filmid

        #ttid -> set(nmid)
        self._tt_graph = defaultdict(set)

        #nmid -> set(ttid)
        self._nm_graph = defaultdict(set)

        #nmid -> name
        self._names = dict()

        #ttid -> tuple(tittel, rating)
        self._film_info = dict()

    def legg_til_kanter_nm(self, key: str, name: str, tt_ids: set):
        known = lambda x: x in self._tt_graph
        self._nm_graph[key] = self._nm_graph[key].union(filter(known, tt_ids))
        for tt_id in filter(known, tt_ids):
            self._tt_graph[tt_id].add(key)
        self._names[key] = name


    def legg_til_filmer(self, key, tittel, rating):
        self._tt_graph[key]
        self._film_info[key] = (tittel, float(rating))

    def antall_noder(self):
        return len(self._nm_graph)

    def antall_kanter(self):
        return sum(map(lambda x: (n := len(x))*(n-1)/2, self._nm_graph.items()))


    def komponenter(self):
        not_visitet = set(self._nm_graph.keys())
        results = defaultdict(lambda: 0)
        while not_visitet:
            queue = set()
            queue.add(not_visitet.pop())
            count = 1
            while queue:
                skuespiller = queue.pop()
                for film in self._nm_graph[skuespiller]:
                    for skuespiller in self._tt_graph[film]:
                        if skuespiller in not_visitet:
                            count += 1
                            not_visitet.remove(skuespiller)
                            queue.add(skuespiller)
                results[count] += 1
        return results










if __name__ == "__main__":
    graph = Graph()
    with open("movies.tsv", "r", encoding="UTF-8") as movies:
        for line in movies:
            line_split = line.split("\t")
            graph.legg_til_filmer(line_split[0], line_split[1], line_split[2])


    with open("actors.tsv", "r", encoding="UTF-8") as actors:
        for line in actors:
            line_split = line.split("\t")
            graph.legg_til_kanter_nm(line_split[0], line_split[1], set(line_split[2:]))

    print(graph.antall_noder())
    print(graph.antall_kanter())

    result = graph.komponenter()

    for key in result:
        print(f"There are {result[key]} components of size {key}")

    print(sum(result.keys()))



