import networkx as nx
import matplotlib.pyplot as plt
from pymongo import MongoClient
import numpy as np
#Imports para tagcloud
import os
import sys
import webbrowser
import json
from cgi import escape
from math import log

class Report():
         #Grafica la entidad y la informacion que le mandan
    def graph_entities(self,query):
        G = nx.Graph()
        client = MongoClient('localhost',27017)
        db = client.test_database
        entities = db.entities
        entitie_info = db.entitie_info
        for e in entities.find({'entitie':query}): #Buscar todas las entidades identificadas en el analizador
            print 'Entidad: '
            print e
            for entity in entitie_info.find({'entitie':e['entitie']}): #Buscar toda la informacion relacionada con esta entidad
                print 'Info Entidad'
                print entity['name']
                #G.add_node(entity['text'])
                G.add_edge(entity['name'],entity['entitie'])
        nx.draw(G)
        plt.show()
    #Graficas las entidades encontradas con su repeticion
    def graph_rept(self):
        client = MongoClient('localhost',27017)
        db = client.test_database
        entities = db.entities
        N = 0
        entities_list = []
        entities_count = []
        sum = 0
        for e in entities.find():
            N = N + 1
            sum = sum + e['count']
         
        avarage = sum / N
        n_ent = 0
        max = 0
        for e in entities.find().sort('count',-1).limit(10):
            n_ent = n_ent + 1
            if e['count'] > max : max = e['count'] 
            entities_list.append(e['entitie'])
            entities_count.append(e['count'])
        width = 0.15       # the width of the bars: can also be len(x) sequence
        ind = np.arange(n_ent)
        plt.bar(ind,entities_count, width, color='r')
        plt.title('Top 10 Entities')
        plt.xticks(ind+width/2,entities_list)
        plt.yticks(np.arange(0,max +1,1))
        plt.show()
    
    def graph_test(self):
        print 'Graph Test'
        G1 = nx.Graph()
        G1.add_edge('Gameplay of Pokemon','Pokemon')
        G1.add_edge('Pokemon Red and Blue','Pokemon')
        G1.add_edge('Pokemon Diamond and Perl','Pokemon')
        
        G2 = nx.Graph()
        G2.add_edge('Nintendo Entreteinment System','Nintendo')
        G2.add_edge('Video Games','Nintendo')
        G2.add_edge('Super Nintendo Entertainment System','Nintendo')
        G2.add_edge('Wii','Nintendo')
        
        G3 = nx.Graph()
        G3.add_edge('Video Games','Game freak')
        G3.add_edge('Game Developer','Game freak')
        G3.add_edge('Pokemon','Game freak')
        #G3.add_edge('Organization','Game freak')
        #G3.add_edge('Business','Game freak')
        G4 = nx.Graph()
        G4.graph['network'] = 'Twitter'
        G4.add_node('Pokemon')
        G4.add_edge('Pokemon','Video Games')
        G4.add_edge('Video Games','Pokemon')
        G4.add_edge('Pokemon','Pikachu')
        G4.add_node('Nintendo')
        G4.add_edge('Video Games','Nintendo')
        
        nx.draw(G4)
        plt.show()
    
    def entity_cloud(self):
        MIN_FREQUENCY = 2
        HTML_TEMPLATE = './wp_cumulus/tagcloud_template.html'
        MIN_FONT_SIZE = 3
        MAX_FONT_SIZE = 20
        
        client = MongoClient('localhost',27017)
        db = client.test_database
        posts = db.analisys_data
        
        def entityCountMapper(doc):
            if not doc.get('entities'):
                import twitter_text
        
                def getEntities(tweet):
        
                    # Now extract various entities from it and build up a familiar structure
        
                    extractor = twitter_text.Extractor(tweet['text'])
        
                    # Note that the production Twitter API contains a few additional fields in
                    # the entities hash that would require additional API calls to resolve
        
                    entities = {}
                    entities['user_mentions'] = []
                    for um in extractor.extract_mentioned_screen_names_with_indices():
                        entities['user_mentions'].append(um)
        
                    entities['hashtags'] = []
                    for ht in extractor.extract_hashtags_with_indices():
        
                        # massage field name to match production twitter api
        
                        ht['text'] = ht['hashtag']
                        del ht['hashtag']
                        entities['hashtags'].append(ht)
        
                    entities['urls'] = []
                    for url in extractor.extract_urls_with_indices():
                        entities['urls'].append(url)
        
                    return entities
        
                doc['entities'] = getEntities(doc)
        
            if doc['entities'].get('user_mentions'):
                for user_mention in doc['entities']['user_mentions']:
                    yield ('@' + user_mention['screen_name'].lower(), [doc['_id'], doc['id']])
            if doc['entities'].get('hashtags'):
                for hashtag in doc['entities']['hashtags']:
                    yield ('#' + hashtag['text'], [doc['_id'], doc['id']])
            
            def summingReducer(keys, values, rereduce):
                if rereduce:
                    return sum(values)
                else:
                    return len(values)
            
            
            #view = ViewDefinition('index', 'entity_count_by_doc', entityCountMapper,
            #                      reduce_fun=summingReducer, language='python')
            #view = ""
            #view.sync(db)
            
            for entity in posts.find():
                entityCountMapper(entity['text'])
                
            entities_freqs = [(row.key, row.value) for row in posts.find()]
            
            # Create output for the WP-Cumulus tag cloud and sort terms by freq along the way
            
            raw_output = sorted([[escape(term), '', freq] for (term, freq) in entities_freqs
                                if freq > MIN_FREQUENCY], key=lambda x: x[2])
            
            # Implementation adapted from 
            # http://help.com/post/383276-anyone-knows-the-formula-for-font-s
            
            min_freq = raw_output[0][2]
            max_freq = raw_output[-1][2]
            
            def weightTermByFreq(f):
                return (f - min_freq) * (MAX_FONT_SIZE - MIN_FONT_SIZE) / (max_freq
                        - min_freq) + MIN_FONT_SIZE
            
            
            weighted_output = [[i[0], i[1], weightTermByFreq(i[2])] for i in raw_output]
            
            # Substitute the JSON data structure into the template
            
            html_page = open(HTML_TEMPLATE).read() % \
                             (json.dumps(weighted_output),)
            
            if not os.path.isdir('out'):
                os.mkdir('out')
            
            f = open(os.path.join('out', os.path.basename(HTML_TEMPLATE)), 'w')
            f.write(html_page)
            f.close()
            
            print 'Tagcloud stored in: %s' % f.name
            
            # Open up the web page in your browser
            
            webbrowser.open("file://" + os.path.join(os.getcwd(), 'out', os.path.basename(HTML_TEMPLATE)))
            
r = Report()
#r.graph_rept()
r.graph_entities('pokemon')