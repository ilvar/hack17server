from bottle import route, run, template, request, response
from neo4j.v1 import GraphDatabase, basic_auth
from random import *

driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("neo4j", "password"))

def get_db():
    return driver.session()

@route('/graph/<article>')
def get_graph(article):
    db = get_db()
    query = 'MATCH (p:Page {title:"%s"})<-[:Link]-(o:Page),(o) <-[:Link]-(q:Page) With o,count(q) as rel_count RETURN o.title as link_title, rel_count Limit 100' % article.replace("_"," ")
#    query = 'MATCH (p:Page {title:"%s"})<-[:Link]-(o:Page) RETURN o.title as link' % article.replace("_"," ")
    results = db.run(query)
    nodes = []
    rels = []
    i = 0
    for record in results:
        nodes.append({"title": record["link_title"], "url": generateUrl(record["link_title"]), "rel_count": record["rel_count"],"rev_link": is_backlinking(article, record["link_title"])})
        target = i
        i += 1
    response.set_header('Access-Control-Allow-Origin', '*')
    return dict(pages=nodes)

def is_backlinking(parent, child):
	return "true"
	#db = get_db()
	#query = 'MATCH (p:Page {title:"%s"})<-[:Link]-(o:Page) Where o.title = "%s" RETURN true LIMIT 1' % (child.replace("_"," "), parent.replace("_"," "))
	#if db.run(query):
	#	return "true"
	#else:
	#	return "false"


def generateUrl(title):
    url_root = "https://en.wikipedia.org/wiki/"
    return url_root+title.replace(" ","_")

run(host='localhost', port=8080)
