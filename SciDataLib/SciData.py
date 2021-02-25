"""Python library for writing SciData JSON-LD files"""
from collections import defaultdict
from itertools import count
from datetime import datetime


class SciData:
    """This class is used to generate and populate a SciData object to be
    output as a SciData JSON-LD document

    A SciData object is generated by calling the SciData class.
    The meta variable defines the keys that make up the
    backbone structure of the document.
    The class methods are called to populate the meta variable keys

    ie. SciDataObject = SciData(<identifier>)
    """

    def __init__(self, uid: str):
        """Initialize the instance using a unique id"""

        self.meta['@graph']['uid'] = uid

    meta = {
        "@context": [],
        "@id": "",
        "generatedAt": "",
        "version": "",
        "@graph": {
            "@id": "",
            "@type": "sdo:scidataFramework",
            "uid": "",
            "title": "",
            "author": [],
            "description": "",
            "publisher": "",
            "version": "",
            "keywords": [],
            "startTime": "",
            "permalink": "",
            "related": [],
            "toc": [],
            "ids": [],
            "scidata": {
                "@id": "scidata/",
                "@type": "sdo:scientificData",
                "discipline": "",
                "subdiscipline": "",
                "methodology": {
                    "@id": "methodology/",
                    "@type": "sdo:methodology",
                    "aspects": []},
                "system": {
                    "@id": "system/",
                    "@type": "sdo:system",
                    "facets": []},
                "dataset": {
                    "@id": "dataset/",
                    "@type": "sdo:dataset"
                },
            },
            "sources": [],
            "rights": []
        }
    }

    contexts = ['https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
    nspaces = {
        "sci": "https://stuchalk.github.io/scidata/ontology/scidata.owl#",
        "sub": "https://stuchalk.github.io/scidata/ontology/substance.owl#",
        "chm": "https://stuchalk.github.io/scidata/ontology/chemical.owl#",
        "w3i": "https://w3id.org/skgo/modsci#",
        "qudt": "http://qudt.org/vocab/unit/",
        "obo": "http://purl.obolibrary.org/obo/",
        "dc": "http://purl.org/dc/terms/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    }
    base = {}

    def context(self, context: list) -> dict:
        """Used to create or replace the list of external context files

        When called, the content of the @context key of the meta variable will
        be replaced with the supplied list of context files
        ie. SciDataObject.context(
            ['https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
        )
        """

        self.contexts = []
        self.contexts = context
        self.make_context()
        return self.meta

    def add_context(self, context: str) -> dict:
        """Used to add to the list of external context files

        When called, the supplied list of context files will be appended
        to the list of any context files already present in the @context
        key of the meta variable
        """

        self.contexts.append(context)
        self.make_context()
        return self.meta

    def namespace(self, namespace: dict) -> dict:
        """Used to create or replace dictionary of namespaces within @context

        When called, the dictionary of namespaces within the @context key
        of the meta variable will be replaced with the supplied dictionary
        of namespaces

        ie. SciDataObject.namespace(
            {"sci": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"}
        )
        """

        self.nspaces = namespace
        self.make_context()
        return self.meta

    def add_namespace(self, namespace: dict) -> dict:
        """Used to add to the dictionary of namespaces within @context

        When called, the supplied dictionary of namespaces will be added to the
        dictionary of namespaces within the @context key of the meta variable
        """

        self.nspaces.update(namespace)
        self.make_context()
        return self.meta

    def add_base(self, base: str) -> dict:
        """
        Make or replace the JSON-LD base URL
        https://www.w3.org/TR/json-ld/#base-iri
        :param base base URL for a JSON-LD file
        """

        if base == "":
            self.base = {
                "@base": "https://scidata.unf.edu/update_your_base_URL"
            }
        else:
            self.base = {"@base": base}
        self.make_context()
        return self.meta

    def make_context(self) -> dict:
        """
        Recreates the context when something is added to contexts,
        namespaces or base

        This method is called automatically by the contexts,
        namespaces or base methods and does not
        need to be accessed manually under normal circumstances
        """

        c = self.contexts
        n = self.nspaces
        b = self.base
        con = c + [n, b]
        self.meta["@context"] = con
        return self.meta

    # TODO May be unneccesary if always an empty string that is populated later
    def doc_id(self, i: str) -> dict:
        """Used to create or replace meta variable base level @id value"""

        self.meta['@id'] = i
        return self.meta

    def generatedat(self, i: str) -> dict:
        """Used to populate the generatedAt meta variable with a timestamp

        ie. SciDataObject.generatedAt(str(datetime.datetime.now()))
        """

        if i != '':
            self.meta['generatedAt'] = i
        else:
            dt = datetime.now()
            self.meta['generatedAt'] = dt.strftime("%m-%d-%y %H:%M:%S")
        return self.meta

    def version(self, i: str) -> dict:
        """Create or replace the sourcecode for the graph"""

        self.meta['version'] = i
        return self.meta

    def graph_id(self, i: str) -> dict:
        """Used to create or replace the @id within the @graph of meta variable

        ie. SciDataObject.graph_id(
            "https://scidata.unf.edu/<uniqueidentifier>/"
        )
        """

        self.meta['@graph']['@id'] = i
        return self.meta

    # TODO May be unneccesary if always "sdo:scidataFramework" as defined
    #      in meta
    def graph_type(self, i: str) -> dict:
        """Create or replace the graph type"""

        self.meta['@graph']['@type'] = i
        return self.meta

    def graph_uid(self, i: str) -> dict:
        """Used to create or replace the uid within the @graph of meta variable

        ie. SciDataObject.graph_uid("<uniqueidentifier>
        """

        self.meta['@graph']['uid'] = i
        return self.meta

    def author(self, author: list) -> dict:
        """Used to create or replace the list of authors within the
        author key of the meta variable

        Expects either:
         1) a list of dictionaries where each dictionary contains a minimum of
            a key that is 'name'

            Example:
            [
                {'name': 'George Washington', 'ORCID': 1},
                {'name': 'John Adams', 'ORCID': 2}
            ]

         2) a list of strings which are author names
            Example: ['George Washington', 'John Adams']
        """

        a = []
        if isinstance(author, list):
            for c, au in enumerate(author):
                if type(au) is dict:
                    if 'name' in au:
                        auth = {'@id': ('author/' + str(c + 1) + '/')}
                        auth.update({'@type': 'dc:creator'})
                        auth.update(au)
                        a.append(auth)
                if type(au) is str:
                    # print(au)
                    auth = {'@id': ('author/' + str(c + 1) + '/')}
                    auth.update({'@type': 'dc:creator'})
                    auth.update({'name': au})
                    a.append(auth)
            self.meta['@graph']['author'] = a
        return self.meta

    def title(self, title: str) -> dict:
        """Used to create or replace title key within @graph of meta variable

        For a data source such as a journal article, this would typically be
        the title of the article
        ie. SciDataObject.title("The Hitchhiker's Guide to the Galaxy")
        """

        self.meta['@graph']['title'] = title
        return self.meta

    def description(self, description: str) -> dict:
        """Used to create or replace the description key within @graph of
        meta variable

        Used as a brief description of the type of data. For a journal article,
        this could potentially house the abstract
        ie. SciDataObject.description(<briefdescription>)
        """

        self.meta['@graph']['description'] = description
        return self.meta

    def publisher(self, publisher: str) -> dict:
        """Used to create or replace the publisher key within @graph of
        meta variable

        ie. SciDataObject.publisher(<publishername>)
        """

        self.meta['@graph']['publisher'] = publisher
        return self.meta

    def graphversion(self, version: str) -> dict:
        """Create or replace the document version"""

        self.meta['@graph']['version'] = version
        return self.meta

    def keywords(self, keywords: str or list) -> dict:
        """Create or replace the keywords of the instance"""

        keys = self.meta['@graph']['keywords']
        if isinstance(keywords, str):
            keys = [keywords]
        elif isinstance(keywords, list):
            keys = keywords
        keys.sort()
        self.meta['@graph']['keywords'] = keys
        return self.meta

    def add_keyword(self, keyword: str) -> dict:
        """Add keyword(s)"""

        keys = self.meta['@graph']['keywords']
        if isinstance(keyword, str) and keyword not in keys:
            keys.append(keyword)
        elif isinstance(keyword, list):
            for k in keyword:
                if k not in keys:
                    keys.append(k)
        return self.meta

    def starttime(self, st: str) -> dict:
        """initiate the start time"""

        self.meta['@graph']['startTime'] = st
        return self.meta

    def permalink(self, link: str) -> dict:
        """Create or replace the document permanent link"""

        self.meta['@graph']['permalink'] = link
        return self.meta

    def related(self, related: str) -> dict:
        """Create or replace the related URIs (adds to array)"""

        self.meta['@graph']['related'] = related
        return self.meta

    def add_related(self, related: str) -> dict:
        """Create or replace the related URIs (adds to array)"""

        self.meta['@graph']['related'].append(related)
        return self.meta

    def ids(self, ids: str) -> dict:
        """Create or replace the ids (adds to array)"""

        self.meta['@graph']['ids'] = sorted(set(ids))
        return self.meta

    def add_ids(self, ids: str) -> dict:
        """Create or replace the ids (adds to array)"""
        curr_ids = self.meta['@graph']['ids']
        curr_ids.append(ids)
        self.meta['@graph']['ids'] = sorted(set(curr_ids))
        return self.meta

    def discipline(self, disc: str) -> str:
        """
        Make or replace discipline
        :param disc: a discipline name or identifier (preferred)
            e.g. use the Modern Science Ontology https://w3id.org/skgo/modsci#
        :returns: str
        """
        self.meta['@graph']['scidata']['discipline'] = disc
        return self.meta['@graph']['scidata']['discipline']

    def subdiscipline(self, subdisc: str) -> str:
        """
        Make or replace subdiscipline
        :param subdisc: a subdiscipline name or identifier (preferred)
            e.g. use the Modern Science Ontology https://w3id.org/skgo/modsci#
        :returns: str
        """
        self.meta['@graph']['scidata']['subdiscipline'] = subdisc
        return self.meta['@graph']['scidata']['subdiscipline']

    def aspects(self, aspects: list) -> dict:
        """Create or replace the aspects of the file"""
        cnt_index = {}

        def iterateaspects(it, level):
            """ iterateaspects function """
            if '@id' in it:
                category = it['@id']
            else:
                category = 'undefined'
            if category in cnt_index:
                cnt_index[category] += 1
            else:
                cnt_index[category] = 1
            cat_index.update({level: category})
            uid = ''
            for cat in cat_index.values():
                uid += cat + '/' + str(cnt_index[category]) + '/'
            temp: dict = {'@id': uid, '@type': 'sdo:' + category}
            for k, v in it.items():
                if k != '@id':
                    temp[k] = v
            for k, v in temp.items():
                if isinstance(v, list):
                    level += 1
                    for i, y in enumerate(v):
                        v[i] = iterateaspects(y, level)
                    temp[k] = v
                    level -= 1
                elif isinstance(v, dict):
                    level += 1
                    temp[k] = iterateaspects(v, level)
                    level -= 1
            return temp

        scidata: dict = self.meta['@graph']['scidata']
        meth: dict = scidata['methodology']
        curr_aspects: list = meth['aspects']

        for item in aspects:
            cat_index = {}
            item = iterateaspects(item, 1)
            curr_aspects.append(item)

        meth['aspects'] = curr_aspects
        scidata['methodology'] = meth
        self.meta['@graph']['scidata'] = scidata
        return self.meta

    def facets(self, facets: list) -> dict:
        """Create or replace the facets of the instance"""
        cnt_index = {}

        def iteratefacets(it, level):
            """ iteratefacets function """
            if '@id' in it:
                category = it['@id']
            elif 'descriptors' in it or 'identifiers' in it:
                category = 'compound'
            else:
                category = 'undefined'
            if category in cnt_index:
                cnt_index[category] += 1
            else:
                cnt_index[category] = 1
            cat_index.update({level: category})
            uid = ''
            for cat in cat_index.values():
                uid += cat + '/' + str(cnt_index[cat]) + '/'
            temp: dict = {'@id': uid, '@type': 'sdo:' + category}
            for k, v in it.items():
                if k != '@id':
                    temp[k] = v
            for k, v in temp.items():
                if isinstance(v, list):
                    level += 1
                    for i, y in enumerate(v):
                        v[i] = iteratefacets(y, level)
                    temp[k] = v
                    level -= 1
                elif isinstance(v, dict):
                    level += 1
                    temp[k] = iteratefacets(v, level)
                    level -= 1
            del cat_index[level]
            return temp

        scidata: dict = self.meta['@graph']['scidata']
        system: dict = scidata['system']
        curr_facets: list = system['facets']

        for item in facets:
            cat_index = {}
            item = iteratefacets(item, 1)
            curr_facets.append(item)

        system['facets'] = curr_facets
        scidata['system'] = system
        self.meta['@graph']['scidata'] = scidata
        return self.meta

    def datapoint(self, points: list) -> dict:
        """Create or replace datapoints"""
        cnt_index = {}

        def iteratedatapoint(it, level):
            """ iteratedatapoint function """
            category = it['@id']
            if category in cnt_index:
                cnt_index[category] += 1
            else:
                cnt_index[category] = 1
            cat_index.update({level: category})
            uid = ''
            for cat in cat_index.values():
                uid += cat + '/' + str(cnt_index[cat]) + '/'
            temp: dict = {'@id': uid, '@type': 'sdo:' + category}
            for k, v in it.items():
                if k != '@id':
                    temp[k] = v
            for k, v in temp.items():
                if isinstance(v, list):
                    level += 1
                    for i, y in enumerate(v):
                        v[i] = iteratedatapoint(y, level)
                    temp[k] = v
                    level -= 1
                elif isinstance(v, dict):
                    level += 1
                    temp[k] = iteratedatapoint(v, level)
                    level -= 1
            del cat_index[level]
            return temp

        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']
        if 'datapoint' in dataset.keys():
            curr_points: list = dataset['datapoint']
        else:
            curr_points = []

        for item in points:
            cat_index = {}
            item = iteratedatapoint(item, 1)
            curr_points.append(item)

        dataset['datapoint'] = curr_points
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return self.meta

    def datagroup(self, datagroup: list) -> dict:
        """ create or replace the datagroup """
        count_index = defaultdict(lambda: count(1))
        data = []

        def iteratedatagroup(it):
            """ iteratedatagroup function """
            category = it['@id']
            index = next(count_index[category])
            it['@id'] = '{category}/{index}/'.format(
                category=category,
                index=index)
            pointlist = []
            for x in it['datapoints']:
                category = x
                index = next(count_index[category])
                pointlist.append(
                    '{category}/{index}/'.format(
                        category=category,
                        index=index))
            it['datapoints'] = pointlist
        for item in datagroup:
            iteratedatagroup(item)
            data.append(item)
            self.meta['@graph']['scidata']['dataset']['datagroup'] = data
        return self.meta

    def source(self, source: list) -> dict:
        """Create or replace the source list"""

        srcs = []
        for x in source:
            ld = {
                '@id': 'source/' + str(len(srcs) + 1) + '/',
                '@type': 'dc:source'
            }
            ld.update(x)
            srcs.append(ld)
        self.meta['@graph']['sources'] = srcs
        return self.meta

    def add_source(self, source: list) -> dict:
        """Add to the sources list"""

        srcs = self.meta['@graph']['sources']
        for x in source:
            ld = {
                '@id': 'source/' + str(len(srcs) + 1) + '/',
                '@type': 'dc:source'
            }
            ld.update(x)
            srcs.append(ld)
        self.meta['@graph']['sources'] = srcs
        return self.meta

    def rights(self, holder: str, license: str) -> dict:
        """Create or replace the rights section"""

        right = [{
            '@id': 'rights/1/',
            '@type': 'dc:rights',
            'holder': holder,
            'license': license,
        }]
        self.meta['@graph']['rights'] = right
        return self.meta

    def add_rights(self, holder: str, license: str) -> dict:
        """ add to the rights list """

        rights = self.meta['@graph']['rights']
        rights_length = len(self.meta['@graph']['rights'])
        rights.append({
            '@id': 'rights/{}/'.format(rights_length + 1),
            '@type': 'dc:rights',
            'holder': holder,
            'license': license,
        })
        return self.meta

    def toc(self):
        """ toc function """
        def tocdict(a):
            """ tocdict function """
            for k, v in a.items():
                if k == '@type':
                    self.meta['@graph']['toc'].append(v)
                if isinstance(v, list):
                    toclist(v)
                if isinstance(v, dict):
                    tocdict(v)

        def toclist(a):
            """ toclist function """
            for x in a:
                if isinstance(x, dict):
                    tocdict(x)
                if isinstance(x, list):
                    toclist(x)
        for key, value in self.meta['@graph'].items():
            if key == '@type':
                self.meta['@graph']['toc'].append(value)
            if isinstance(value, dict):
                tocdict(value)
            if isinstance(value, list):
                toclist(value)
        self.meta['@graph']['toc'] = sorted(set(self.meta['@graph']['toc']))
        return self.meta

    @property
    def output(self) -> dict:
        """Generates Scidata JSON-LD File"""

        empty = []
        for key, value in self.meta['@graph'].items():
            if isinstance(value, str) and value == "":
                empty.append(key)
            elif isinstance(value, list) and value == []:
                empty.append(key)
        for key, value in self.meta['@graph']['scidata'].items():
            if isinstance(value, dict):
                for v in value.values():
                    if not v:
                        empty.append(key)
        for e in empty:
            if e in self.meta['@graph']['scidata'].keys():
                self.meta['@graph']['scidata'].pop(e)
            elif e in self.meta['@graph'].keys():
                self.meta['@graph'].pop(e)

        # temp = json.dumps(self.meta, indent=4, ensure_ascii=False)
        # print(temp)

        # print('complete: '+ str(self.meta['@graph']['uid']))
        return self.meta
