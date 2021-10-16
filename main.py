from collections import defaultdict



class Graph:
    def __init__(self):
        #nmid = skuespillerid
        #ttid = filmid

        #ttid -> set(nmid)
        self._tt_graph = dict()

        #nmid -> set(ttid)
        self._nm_graph = defaultdict(set)

        #nmid -> name
        self._names = dict()

        #ttid -> tuple(tittel, rating)
        self._film_info = dict()

    def legg_til_kanter_nm(self, key: str, name: str, tt_ids: set[str]):
        known = lambda x: x in self._tt_graph
        self._nm_graph[key] = self._nm_graph[key].union(filter(known, tt_ids))
        for tt_id in filter(known, tt_ids):
            self._tt_graph[tt_id].add(key)
        self._names[key] = name

    def legg_til_filmer(self, key: str, tittel: str, rating: float):
        self._tt_graph[key] = set()
        self._film_info[key] = (tittel, rating)

    def antall_noder(self):
        return len(self._nm_graph)

    def antall_kanter(self):
        return int(sum(map(lambda x: len(x)*(len(x)-1)/2, self._tt_graph.values())))


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
                    for nabo in self._tt_graph[film]:
                        if nabo in not_visitet:
                            count += 1
                            not_visitet.discard(nabo)
                            queue.add(nabo)
            results[count] += 1
        return results










if __name__ == "__main__":
    graph = Graph()
    with open("movies.tsv", "r", encoding="UTF-8") as movies:
        for line in movies:
            line_split = line.strip().split("\t")
            graph.legg_til_filmer(line_split[0], line_split[1], float(line_split[2]))


    with open("actors.tsv", "r", encoding="UTF-8") as actors:
        for line in actors:
            line_split = line.strip().split("\t")
            graph.legg_til_kanter_nm(line_split[0], line_split[1], set(line_split[2:]))

    print(f"Nodes: {graph.antall_noder()}")
    print(f"Edges: {graph.antall_kanter()}")

    result = graph.komponenter()

    for key in result:
        print(f"There are {result[key]} components of size {key}")

    summ = 0
    for key in result:
        summ  += key*result[key]
    print(summ)

