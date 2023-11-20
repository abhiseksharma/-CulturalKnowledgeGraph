# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 01:17:01 2023

@author: abhis
"""

'''


input: Source and target country
output: List of suggesions based on the value difference between the values of 
        dimensions of both the countries.
        
    steps:
        1. I'll check the values of both the countries.
        2. Compare them the values. (See NOTE:)
        3. if they both are above 50 or below then the suggestion will be to 
            stay as they are but maybe more or less
        4. if they are opposite of each other then suggestions will be like 
            they need to learn the ways of the other side of the spectrum
        NOTE: In all the cases the difference between those values must be 
            greater than 20 (tentative). If the difference is less then no need to change. 
        
        
'''
from rdflib import Graph


# Input
SourceCountry = input("Enter source country")
TargetCountry = input("Enter target country")

# Fetching values of dimensions corresponding to the country
SourceCountryDict = {}
TargetCountryDict = {}

g = Graph()
g.parse("CulturalKnowledgeGraph.owl")

sourceValueQuery = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
prefix my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
SELECT ?d ?value
	WHERE { my:""" + SourceCountry + """?d ?value . 
		?d rdf:type owl:DatatypeProperty}
"""

targetValueQuery = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
prefix my: <http://www.semanticweb.org/abhis/CulturalKnowledgeGraph#>
SELECT ?d ?value
	WHERE { my:""" + TargetCountry + """?d ?value . 
		?d rdf:type owl:DatatypeProperty}
"""


qres = g.query(sourceValueQuery)
for row in qres:
    SourceCountryDict[row.d.split('#')[1]] = int(row.value)

qres = g.query(targetValueQuery)
for row in qres:
    TargetCountryDict[row.d.split('#')[1]] = int(row.value)


# Comparing values and giving suggestions
# noOfDimensions = 6


# A file containing all the responces will be used for the suggesions as of now.

'''
Example template
Power Distance Index (low versus high)
a) < 50 meaning 
	dimensionName = low power distance
b) > 50 meaning
	dimensionName = high power distance

1. source > target value on the same side (<50):
Although [source] and [target] follows [dimensionName] values but [source] should diel it up a bit to cater for the [target] culture.

2. source < target value on the same side (<50):
Although [source] and [target] follows [dimensionName] values but [source] should diel it down a bit to cater for the [target] culture.

3. source > target value on the same side (>50):
Although [source] and [target] follows [dimensionName] values but [source] should diel it down a bit to cater for the [target] culture.

4. source < target value on the same side (>50):
Although [source] and [target] follows [dimensionName] values but [source] should diel it up a bit to cater for the [target] culture.

5. source and target value on different sides:
if target > 50:
	dimensionName = high power distance
if target < 50:
	dimensionName = low power distance
[source] and [target] follows different values. So, [source] should learn the ways of [dimensionName] culture.

'''



def DimensionNameFetching(key):
    lessThan50 = ""
    moreThen50 = ""
    if key == "individualismVersusCollectivismValue":
        lessThan50 = "Individualism"
        moreThen50 = "Collectivism"
    if key == "indulgenceVersusRestraintValue":
        lessThan50 = "Indulgence"
        moreThen50 = "Restraint"
    if key == "longtermVersusShorttermOrientationValue":
        lessThan50 = "Short-Term Orientation"
        moreThen50 = "Long-Term Orientation"
    if key == "masculinityVersusFemininityValue":
        lessThan50 = "Masculinity"
        moreThen50 = "Femininity"
    if key == "powerDistanceValue":
        lessThan50 = "Low Power Distance"
        moreThen50 = "High Power Distance"
    if key == "uncertainityAvoidanceValue":
        lessThan50 = "Low Uncertainty Avoidance tendency"
        moreThen50 = "High Uncertainty Avoidance tendency"
    return (lessThan50, moreThen50)

for key in SourceCountryDict.keys():
    dimensionName = key
    print("For " + key + "dimension, ", end="")
    if abs(SourceCountryDict[key] - TargetCountryDict[key]) > 20:
        if SourceCountryDict[key] > 50 and TargetCountryDict[key] > 50:
            dimensionName = DimensionNameFetching(key)[1]
            if SourceCountryDict[key] > TargetCountryDict[key]:
                print("Although " + SourceCountry + " and " + TargetCountry + " follows " + dimensionName + " values but " + SourceCountry + " should diel it down a bit to cater for the " + TargetCountry + " culture.")
            else:
                print("Although " + SourceCountry + " and " + TargetCountry + " follows " + dimensionName + " values but " + SourceCountry + " should diel it up a bit to cater for the " + TargetCountry + " culture.")
        elif SourceCountryDict[key] <= 50 and TargetCountryDict[key] <= 50:
            dimensionName = DimensionNameFetching(key)[0]
            if SourceCountryDict[key] < TargetCountryDict[key]:
                print("Although " + SourceCountry + " and " + TargetCountry + " follows " + dimensionName + " values but " + SourceCountry + " should diel it down a bit to cater for the " + TargetCountry + " culture.")
            else:
                print("Although " + SourceCountry + " and " + TargetCountry + " follows " + dimensionName + " values but " + SourceCountry + " should diel it up a bit to cater for the " + TargetCountry + " culture.")
        else:
            dimensionNameTuple = DimensionNameFetching(key)
            dimensionName = dimensionNameTuple[1]
            print(SourceCountry + " and " + TargetCountry + " has different values. So, " + SourceCountry + " should learn the ways of " + dimensionName + " culture.")
    else:
        print("Person from " + SourceCountry + " need not change much for " + dimensionName + " dimension as there is not much difference in the culture present for the dimension")


