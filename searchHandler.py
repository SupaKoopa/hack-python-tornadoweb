
__author__ = 'mario'
import tornado.web
import tornado.template
import elasticsearch
import models.searchItem
import json


class searchHandler(tornado.web.RequestHandler):

    def searchElastic(self, query, pageNumber):
        es = elasticsearch.Elasticsearch()

        startingIndex = (pageNumber - 1) * 3

        elasticBody=None
        if query != None and bool(query.strip()):
            elasticBody = {"query": {"match": {"_all": query}}}


        result = es.search(index='product', body=elasticBody, params={"from": startingIndex, 'size': 3}) # , q=q)
        print json.dumps(result, indent=4)

        AllResultsTotal = 0
        hits = result['hits']['hits']
        if hits:
            AllResultsTotal = result["hits"]["total"]

        return result, AllResultsTotal

    def buildSearchItems(self, elasticSearchResult):
        hits = elasticSearchResult['hits']['hits']
        searchItems = []
        total = 0

        if not hits:
            print 'No matches found'
        else:
            for hit in hits:
                item = models.searchItem.searchItem()
                item.name = hit['_source']['title']
                item.imageUrl = "http://images.kalahari.net" + hit["_source"]["imageUrl"]
                searchItems.append(item)

        return searchItems

    def get(self, *args, **kwargs):
        #self.write("Hello world from search page")

        #loader = tornado.template.Loader("templates/")

        query = self.get_argument("q", None)
        page_str = self.get_query_argument("page", -1)
        page = 1
        if page_str != -1:
            page = int(page_str)

        searchResult = self.searchElastic(query=query, pageNumber=page)

        searchItems = self.buildSearchItems(searchResult[0])
        total = searchResult[1]

        self.render('search.html', query=query, current_page=page, total=total, items=searchItems)
        #print loader.load("search.html").generate(items=searchItems)

    def post(self, *args, **kwargs):

        query = self.get_argument("q", None)
        page = 1

        searchResult = self.searchElastic(query=query, pageNumber=page)
        total = searchResult[1]
        searchItems = self.buildSearchItems(searchResult[0])


        self.render('search.html', query=query, current_page=page, total=total, items=searchItems)




