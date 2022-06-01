# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:47:56 2022

Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
Type "copyright", "credits" or "license" for more information.

IPython 7.8.0 -- An enhanced Interactive Python.

@author: Abhisek
"""

import pandas as pd
import rdflib

df = pd.read_csv("Hofstede dimension values.csv", encoding='latin-1')
df = df.loc[:, ['country', 'pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']]

graph = rdflib.Graph()
graph.parse('CulturalKnowledgeGraph.owl')


""" 
country
pdi = Power Distance
idv = Individualism
mas = Masculinity
uai = Uncertainity Avaoidance
ltowvs = Long Term Orientation
ivr = Indulgence
 """


for i in df.index:
#    print(df.loc[i]['country'])
    
    country = (df.loc[i]['country']).replace(' ', '').replace('.', '')
    
    queryCountry = """
    PREFIX my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
    INSERT DATA
    { 
      my:"""+ country + """ a my:Country .
    }"""
    
     
    querypdi = """
    PREFIX my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
    INSERT DATA
    { 
      my:"""+ country + """ my:powerDistanceValue """+ (df.loc[i]['pdi']) +""" .
    }"""

    queryidv = """
    PREFIX my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
    INSERT DATA
    { 
      my:"""+ country + """ my:individualismVersusCollectivismValue """ + (df.loc[i]['idv']) +""" .
    }"""

    querymas = """
    PREFIX my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
    INSERT DATA
    { 
      my:"""+ country + """ my:masculinityVersusFemininityValue """ + (df.loc[i]['mas']) +""" .
    }"""

    queryuai = """
    PREFIX my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
    INSERT DATA
    { 
      my:"""+ country + """ my:uncertainityAvoidanceValue """ + (df.loc[i]['uai']) +""" .
    }"""

    queryltowvs = """
    PREFIX my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
    INSERT DATA
    { 
      my:"""+ country + """ my:longtermVersusShorttermOrientationValue """ + (df.loc[i]['ltowvs']) +""" .
    }"""

    queryivr = """
    PREFIX my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
    INSERT DATA
    { 
      my:"""+ country + """ my:indulgenceVersusRestraintValue """ + (df.loc[i]['ivr']) +""" .
    }"""

    qres = graph.update(queryCountry)
    if (df.loc[i]['pdi']) != '#NULL!':
        qres = graph.update(querypdi)
    if (df.loc[i]['idv']) != '#NULL!':
        qres = graph.update(queryidv)
    if (df.loc[i]['mas']) != '#NULL!':    
        qres = graph.update(querymas)
    if (df.loc[i]['uai']) != '#NULL!':
        qres = graph.update(queryuai)
    if (df.loc[i]['ltowvs']) != '#NULL!':
        qres = graph.update(queryltowvs)
    if (df.loc[i]['ivr']) != '#NULL!':
        qres = graph.update(queryivr)
    
    
graph.serialize('CulturalKnowledgeGraph.owl', format='application/rdf+xml')