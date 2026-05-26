class Reranker:

    def rerank(self, docs):

        unique = []
        seen = set()

        for d in docs:

            if d.page_content not in seen:
                seen.add(d.page_content)
                unique.append(d)

        return unique