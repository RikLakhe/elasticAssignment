from elasticsearch import Elasticsearch, RequestsHttpConnection
import json
import hashlib
import time

import hidden

secrets = hidden.elastic()


class ElasticBook:

    def __init__(self) -> None:
        self.filename = ""
        self.fhand = None
        self.es = Elasticsearch(
            [secrets['host']],
            http_auth=(secrets['user'],
                       secrets['pass']),
            url_prefix=secrets['prefix'],
            scheme=secrets['scheme'],
            port=secrets['port'],
            connection_class=RequestsHttpConnection,
        )
        self.indexname = secrets['user']

    def start_bookfile_process(self):
        bookfile = self.__get_input("Enter book file (i.e. pg18866.txt): ");
        if bookfile == '':
            self.filename = "pg18866.txt"
        else:
            self.filename = bookfile
        self.__open_bookfile()
        self.__clean_index()
        self.__process_file()
        self.__recompute_index()

    def __process_file(self):
        para = ""
        chars = 0
        count = 0
        pcount = 0
        for line in self.fhand:
            count = count + 1
            line = line.strip()
            chars = chars + len(line)
            if line == '' and para == '': continue
            if line == '':
                pcount = pcount + 1
                doc = {
                    'offset': pcount,
                    'content': para
                }
                m = hashlib.sha256()
                m.update(json.dumps(doc).encode())
                pkey = m.hexdigest()

                res = self.es.index(index=self.indexname, id=pkey, body=doc)
                print('Added document', pkey)
                if pcount % 100 == 0:
                    print(pcount, 'loaded...')
                    time.sleep(1)

                para = ''
                continue
            para = para + " "+line


    def get_filename(self):
        return self.filename

    def check_elasticsearch_connection(self):
        try:
            self.es.ping()
            return True
        except Exception as e:
            print(e)
            return False

    def check_bookfile_opened(self):
        if self.fhand is not None:
            return True
        return False

    def clean_up(self):
        self.fhand = None
        self.es = None
        pass

    @staticmethod
    def __get_input(text):
        return input(text)

    def __open_bookfile(self):
        try:
            fhand = open("./sources/" + self.filename)
            self.fhand = fhand
        except FileNotFoundError as e:
            print("Error:", e)
            self.start_bookfile_process()

    def __clean_index(self):
        res = self.es.indices.delete(index=self.indexname, ignore=[400, 404])
        print("Dropped index", self.indexname)
        print(res)

        res = self.es.indices.create(index=self.indexname)
        print("Created the index...")
        print(res)

    def __recompute_index(self):
        res = self.es.indices.refresh(index=self.indexname)
        print("Index refreshed", self.indexname)
        print(res)

    def search(self, param):
        body = json.dumps({"query": {"query_string": {"query": param}}})
        return self.es.search(index=self.indexname, body=body)

if __name__ == '__main__':
    elasticbook = ElasticBook()
    elasticbook.start_bookfile_process()
