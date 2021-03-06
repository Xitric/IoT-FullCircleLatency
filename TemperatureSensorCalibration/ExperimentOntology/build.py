from rdflib import Literal

from wrapper import *

g = model()

ESP32 = IOT5['/esp32/1']
water1 = IOT5['/water/1']
thermistor1 = IOT5['/thermistor/1']
thermometerReal = IOT5['/thermometer/real']
thermometerSimMin = IOT5['/thermometerSim/min']
thermometerSimMax = IOT5['/thermometerSim/max']
thermometerSimAvg = IOT5['/thermometerSim/avg']
functionMin = IOT5['/function/min']
functionMax = IOT5['/function/max']
functionAvg = IOT5['/function/avg']

g.add((ESP32, RDF.type, IOT5.ESP32))
g.add((ESP32, IOT5.connectedTo, thermistor1))

g.add((thermistor1, RDF.type, IOT5.Thermistor))
g.add((thermistor1, FRAME.hasMeasurement, water1))

g.add((thermometerReal, RDF.type, IOT5.Water))
g.add((thermometerReal, FRAME.hasMeasurement, water1))

g.add((functionMin, RDF.type, IOT5.Function))
g.add((functionMin, IOT5.hasType, IOT5.LinearFunction))
g.add((functionMin, FRAME.hasInput, thermistor1))
g.add((functionMin, IOT5.a, Literal(0.836, datatype=XSD.float)))
g.add((functionMin, IOT5.b, Literal(3.2044, datatype=XSD.float)))

g.add((functionMax, RDF.type, IOT5.Function))
g.add((functionMax, IOT5.hasType, IOT5.LinearFunction))
g.add((functionMax, FRAME.hasInput, thermistor1))
g.add((functionMax, IOT5.a, Literal(0.7984, datatype=XSD.float)))
g.add((functionMax, IOT5.b, Literal(10.237, datatype=XSD.float)))

g.add((functionAvg, RDF.type, IOT5.Function))
g.add((functionAvg, IOT5.hasType, IOT5.LinearFunction))
g.add((functionAvg, FRAME.hasInput, thermistor1))
g.add((functionAvg, IOT5.a, Literal(0.8278, datatype=XSD.float)))
g.add((functionAvg, IOT5.b, Literal(5.9526, datatype=XSD.float)))

g.add((functionMin, FRAME.hasOutput, thermometerSimMin))
g.add((functionMax, FRAME.hasOutput, thermometerSimMax))
g.add((functionAvg, FRAME.hasOutput, thermometerSimAvg))

g.serialize("ontology.ttl", 'turtle')


def query(g, q):
    r = g.query(q)
    return list(map(lambda row: list(row), r))


# thermistor to the 3 functions
q_function_info = '''
    SELECT DISTINCT ?a ?b ?function_type ?function
    WHERE {
        ?thermistor     rdf:type/rdf:subClassOf*    iot5:Thermistor .
        ?function       frame:hasInput              ?thermistor .
        ?function       rdf:type                    iot5:Function .
        ?function       iot5:a                      ?a .
        ?function       iot5:b                      ?b .
        ?function       iot5:hasType                ?function_type . 
    }
    '''

print(query(g, q_function_info))
