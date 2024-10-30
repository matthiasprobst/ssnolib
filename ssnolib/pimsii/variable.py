from ontolutils import Thing, namespaces, urirefs


@namespaces(pims="http://www.molmod.info/semantics/pims-ii.ttl#")
@urirefs(Variable='pims:Variable')
class Variable(Thing):
    pass
