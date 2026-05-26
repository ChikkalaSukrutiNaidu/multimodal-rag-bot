class ConflictDetector:

    def detect(self, docs):

        values = set()

        for d in docs:
            values.add(d.page_content)

        return len(values) > 1