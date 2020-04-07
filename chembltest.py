from model import *
import os
import django
import ast

django.setup()
from scidata.chembldb26 import *
from scidata.crosswalks import *

path = r"/Users/n01448636/Documents/chembl django/scidata/JSON_dumps"
os.chdir(path)

dbname = 'default'
query_crosswalks_chembl = list(Chembl.objects.using('crosswalks').values())
query_crosswalks_ontterms = list(Ontterms.objects.using('crosswalks').values())
query_crosswalks_nspaces = list(Nspaces.objects.using('crosswalks').values())

Documents = set()
for x in Activities.objects.values().filter(herg=1):
    Documents.add(x['doc_id'])
# print(Documents)

# Documents = {36053, 5535, 5706, 6642, 6305} ###Remove this line to process all documents###
# print(Documents)
Documents = {51366}

# Documents = {61703, 61704, 73991, 90376, 49420, 47374, 47387, 53537, 108834, 65828, 61734, 98598, 61736, 65832, 82217, 53547, 55596, 57644, 98610, 57653, 65846, 31037, 53567, 20801, 57666, 92486, 61767, 90441, 61771, 72011, 61777, 82258, 74074, 65886, 65887, 55651, 92517, 92523, 92524, 90478, 45429, 49527, 31096, 92536, 104827, 57725, 45438, 104834, 98692, 72070, 57736, 37257, 57738, 61839, 65935, 65948, 31133, 65953, 104866, 37284, 49572, 57764, 20904, 47532, 51632, 92593, 49586, 92595, 55736, 61882, 90558, 90560, 51653, 55749, 82373, 74184, 74185, 90565, 39371, 72140, 90570, 51662, 98768, 31185, 66002, 31187, 39380, 57813, 61911, 57816, 72152, 72159, 76255, 72161, 106979, 45540, 106982, 55784, 20971, 74220, 98795, 98797, 35312, 31217, 6642, 61936, 66033, 72177, 72180, 74227, 39416, 92656, 57853, 55806, 104961, 76295, 104970, 76299, 31249, 109073, 61971, 104979, 107028, 92694, 72215, 76312, 98838, 104984, 74268, 82462, 109087, 76320, 57890, 98850, 98852, 98857, 45610, 31275, 90671, 105007, 37427, 55861, 109110, 49719, 72247, 37433, 37434, 72251, 109111, 109114, 72256, 62019, 74310, 107079, 109127, 72268, 39512, 37466, 16989, 49758, 92765, 98911, 105056, 47715, 62053, 92777, 47722, 105073, 105075, 51830, 76408, 37497, 31355, 47739, 51836, 31358, 90747, 92803, 17028, 37508, 62087, 74376, 53898, 74384, 101009, 72347, 90780, 72349, 62111, 109217, 107170, 105126, 109228, 72365, 98990, 105133, 74418, 109238, 49850, 49856, 107202, 45765, 101066, 45774, 101074, 99029, 58072, 60127, 51937, 109285, 53996, 62194, 54003, 49908, 60150, 54009, 72441, 49920, 31491, 54021, 31495, 62218, 31499, 62223, 99090, 99091, 107286, 47900, 54049, 47909, 92968, 99112, 45867, 43820, 52012, 35630, 99117, 45872, 105259, 62258, 54069, 45878, 54071, 47928, 90936, 74554, 60219, 90937, 45885, 101176, 90948, 52037, 62279, 105287, 74569, 54091, 90955, 90957, 43854, 62287, 101195, 107349, 76631, 62299, 45917, 109408, 72545, 99170, 101220, 101221, 105326, 45935, 93040, 105328, 58227, 37757, 93053, 35712, 37762, 91010, 31620, 58244, 50055, 93066, 58251, 72589, 37774, 37775, 48014, 45969, 91021, 48022, 48025, 50076, 99229, 58279, 105386, 72619, 60335, 74673, 48050, 105395, 93114, 43963, 48059, 48062, 93121, 46018, 99266, 99270, 99273, 48076, 60364, 107468, 99281, 107474, 52179, 101332, 109529, 43995, 109535, 60385, 66531, 62437, 99302, 99303, 109546, 44011, 109547, 52205, 66542, 48111, 91120, 99312, 48114, 109552, 99316, 44021, 76790, 107510, 50171, 93180, 60417, 46082, 60418, 91137, 105475, 99335, 46090, 50186, 60427, 91146, 101386, 66575, 52242, 50196, 66581, 44059, 105501, 46110, 37921, 74786, 93219, 109604, 72741, 99365, 52268, 105518, 76847, 107566, 58417, 93234, 93235, 31797, 66614, 46137, 54329, 21563, 66620, 66623, 93249, 97347, 37956, 93253, 97350, 58439, 76872, 66633, 97353, 62542, 93264, 66641, 74834, 97361, 31829, 107608, 48219, 66652, 83039, 66656, 107616, 50275, 107620, 83047, 46184, 101482, 89195, 83052, 31854, 42094, 31856, 66673, 48242, 91246, 97392, 107635, 74870, 109684, 97400, 101496, 72826, 101498, 74876, 83070, 101506, 66691, 89219, 99462, 52360, 83082, 48267, 66700, 101515, 58512, 58513, 35986, 89234, 93332, 99477, 101527, 52377, 97433, 105626, 93340, 72861, 101534, 107677, 74914, 91301, 107685, 66727, 76969, 91309, 99502, 44209, 97457, 46260, 52405, 89268, 109754, 76987, 103612, 91325, 83134, 97469, 58566, 109768, 91338, 58571, 89293, 36048, 93393, 109779, 97492, 36053, 66774, 105684, 77018, 77020, 52446, 60645, 66790, 89319, 52456, 91365, 62698, 91369, 66796, 107756, 60661, 36086, 66806, 66808, 74999, 60666, 75002, 91381, 62717, 77053, 105723, 58624, 60672, 60674, 77056, 105726, 60677, 89349, 38154, 58634, 58635, 107786, 58643, 60692, 52501, 44310, 105748, 107801, 62748, 97564, 105758, 108538, 54565, 58664, 83241, 36138, 54570, 77100, 89388, 97580, 101677, 105768, 66867, 50484, 77109, 93493, 97594, 83263, 48450, 77123, 105795, 109891, 50505, 109897, 66891, 62799, 93519, 50521, 54617, 91482, 46430, 91486, 91487, 89441, 105823, 107872, 66917, 99689, 54634, 101737, 44396, 58732, 30062, 46446, 62831, 91500, 46450, 103793, 109935, 77174, 103799, 48504, 48505, 38266, 48507, 46458, 91514, 38270, 36225, 54657, 64898, 77189, 105864, 105868, 103822, 75153, 46484, 105879, 44442, 64923, 89498, 105883, 66974, 5535, 60839, 64935, 103847, 93613, 44462, 97710, 50608, 54705, 64954, 75195, 93627, 50621, 91581, 54719, 50624, 93633, 38338, 101821, 46532, 58821, 48582, 75206, 89543, 97735, 67018, 44491, 107979, 62926, 38355, 44501, 62935, 38360, 105943, 50650, 101850, 58844, 30173, 58848, 103907, 54756, 91620, 38377, 52714, 67049, 93674, 50671, 54767, 110065, 105970, 48630, 54775, 67063, 50681, 50683, 101885, 54782, 58879, 110080, 62981, 62982, 93702, 108040, 108041, 91658, 38411, 108042, 50701, 89615, 91664, 50714, 60956, 54813, 50718, 60957, 60959, 67105, 58914, 63010, 91690, 101933, 108080, 89651, 44598, 75319, 58936, 89655, 101943, 110137, 75324, 58944, 52804, 46661, 89669, 75337, 5706, 38476, 15949, 75340, 50769, 58964, 42581, 91732, 46682, 38497, 50787, 89699, 93798, 93801, 97897, 46699, 106098, 97908, 61045, 106101, 106107, 75393, 50820, 89733, 36492, 97933, 97934, 89744, 61073, 89748, 44693, 38555, 46754, 38564, 44709, 61098, 61106, 48824, 104120, 61114, 48827, 38589, 102078, 91842, 59075, 104135, 59080, 59084, 108236, 104145, 61143, 89815, 48857, 61147, 48865, 61153, 61154, 46824, 59113, 20205, 61168, 61171, 89847, 61176, 93948, 57087, 57093, 48902, 108295, 44811, 57100, 73484, 59150, 89870, 108302, 65299, 65301, 108311, 83736, 108313, 50972, 36644, 57124, 73510, 57127, 83751, 102183, 48939, 59179, 102187, 108331, 65331, 83763, 83767, 61240, 53049, 38714, 51003, 48961, 59202, 65350, 65353, 48970, 59210, 65354, 106314, 61265, 65361, 73554, 61268, 61269, 83796, 83800, 59228, 44897, 53091, 36709, 104295, 44908, 81773, 65392, 106354, 61301, 36726, 49014, 38776, 51063, 44922, 34683, 73590, 34685, 20351, 34689, 106371, 34692, 34693, 81798, 46990, 34703, 81810, 104344, 106393, 108440, 34715, 73627, 55203, 81828, 34725, 44965, 53157, 83877, 59306, 73642, 106413, 30640, 51127, 83897, 90050, 108484, 51148, 108494, 51152, 38865, 59346, 83920, 108499, 81888, 73697, 104417, 106464, 108516, 65509, 83941, 47080, 83944, 81906, 90099, 61428, 65525, 83956, 90103, 61433, 81914, 61436, 38909}


for DocumentNumber in Documents:
    print(DocumentNumber)
    doc_data = {}
    doc_data.update(Docs.objects.values().get(doc_id=DocumentNumber))

    try:
        auth = doc_data['authors'].split(', ')
    except:
        auth = ['Anonymous']
        # print(DocumentNumber)
    authors = []
    for a in auth:
        authors.append({'name':a})

    namespace = {}


    ###############################

    test = SciData(doc_data['doc_id'])
    test.context(['https://stuchalk.github.io/scidata/contexts/chembl.jsonld','https://stuchalk.github.io/scidata/contexts/scidata.jsonld'])
    test.base({"@base": "http://BASE.jsonld"})
    # test.doc_id("@ID HERE")
    test.graph_id("graph_ID_HERE")
    test.title(doc_data['title'])
    test.author(authors)
    test.description(doc_data['abstract'])
    test.publisher(doc_data['journal'])
    test.version('1.0')
    test.permalink("http://PERMALINK.jsonld")
    # test.related("http://RELATED.jsonld")
    test.discipline('w3i:Chemistry')
    test.subdiscipline('w3i:MedicinalChemistry')
    # test.source([{"citation1": "Johnson Research Group http://CITATION.edu", "url": "http://CITATION.jsonld"}])
    test.rights("https://creativecommons.org/licenses/by-nc-nd/4.0/")
    addnamespace = {'w3i':'https://w3id.org/skgo/modsci#'}

    ####

    # test.add_context("added context")
    # test.add_namespace({"namespace2": "http://NAMESPACE.owl#"}) #content is replaced by test.namespace further in script
    # test.add_keyword('keyword 2')
    # test.add_source([{"citation2": "Chalk Research Group http://chalk.coas.unf.edu",
    #                   "url": "http://stuchalk.github.io/scidata/examples/ph.jsonld"}])
    # test.add_rights("rights 2")

    ###############################

    # activity_id_list = Docs.objects.get(doc_id=DocumentNumber).activities_set.all()

    crosswalks = []
    crosswalksA = {}

    for ont in query_crosswalks_chembl:
        crosswalksA = ont
        if crosswalksA['sdsection'] is None:
            for onto in query_crosswalks_ontterms:
                if crosswalksA['ontterm_id'] == onto['id']:
                    for x,y in onto.items():
                        crosswalksA.update({x:y})
        else:
            for onto in query_crosswalks_ontterms:
                if crosswalksA['ontterm_id'] == onto['id']:
                    for x,y in onto.items():
                        if x not in ['sdsection', 'sdsubsection']:
                            crosswalksA.update({x:y})
        crosswalks.append(crosswalksA)

    molregno_set = set()
    for mo in Activities.objects.values().filter(doc_id=DocumentNumber):
        molregno_set.add(mo['molregno_id'])


    molregno_set_filtered = set()
    for mol in molregno_set:
        SciData.meta['@graph']['toc'] = []
        activity_list = Activities.objects.values().filter(doc_id=DocumentNumber, molregno_id=mol, herg=1)
        if activity_list:
            molregno_set_filtered.add(mol)
    molregno_set = {list(molregno_set_filtered)[0]}

    for mol in molregno_set:
        SciData.meta['@graph']['toc'] = []
        activity_list = Activities.objects.values().filter(doc_id=DocumentNumber, molregno_id=mol, herg=1)


        allunsorted = {}
        datapoint = []
        datagroup = []
        datagroupA = []
        namespacetoc = []
        methodology = []
        methodologyx = []
        system = []
        systemx = []
        nspaces = set()
        nspacestoc = set()

        for ac in activity_list:

            # chembl = (Activities.objects.values('molregno_id__chembl_id').get(activity_id=ac['activity_id']))
            # print(chembl)

            # serialized = serialize(Activities.objects.get(activity_id=ac['activity_id']), dbname)
            serializedpre = serialize(Activities.objects.get(activity_id=ac['activity_id']))


            serializedsetpre = set()
            for cross in crosswalks:
                if cross['category']:
                    serializedsetpre.add(cross['category'])
                else:
                    serializedsetpre.add(cross['table'])


            serialized = []
            for x,y in serializedpre.items():
                # print(x,y)
                den = denester(x,y)
                serialized.append(den)

            serializednew = []
            for x in serialized:
                # print(x)
                for y in x:
                    empty = {}
                    for sersetpre in serializedsetpre:
                        emptee = {sersetpre: {}}
                        for cross in crosswalks:
                            if cross['category']:
                                if cross['category'] == sersetpre:
                                    for serial_table, serial_dict in y.items():
                                        if cross['table'] == serial_table:
                                            emptee[sersetpre].update(serial_dict)

                            else:
                                if cross['table'] == sersetpre:
                                    for serial_table, serial_dict in y.items():
                                        if cross['table'] == serial_table:
                                            emptee[sersetpre].update(serial_dict)

                        if emptee[sersetpre]:
                            empty.update(emptee)

                    if empty:
                        serializednew.append(empty)

            serializedset = set()
            for cross in crosswalks:
                if cross['category']:
                    serializedset.add(cross['category'])
                else:
                    serializedset.add(cross['table'])


            serializedgrouped = []
            for serset in serializedset:
                ser1 = {serset:{}}
                for cross in crosswalks:
                    if cross['category']:
                        if cross['category'] == serset:
                            for serial in serializednew:
                                for serial_table,serial_dict in serial.items():
                                    if cross['table'] == serial_table:
                                        ser1[serset].update(serial_dict)
                    else:
                        if cross['table'] == serset:
                            for serial in serializednew:
                                for serial_table, serial_dict in serial.items():
                                    if cross['table'] == serial_table:
                                        ser1[serset].update(serial_dict)
                if ser1[serset]:
                    serializedgrouped.append(ser1)


            datapoint_set = set()
            # print('_')
            for serial in serializedgrouped:
                # print(serial)

                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['ignore'] is None:
                            if cross['sdsection'] == 'dataset':
                                if cross['category']:
                                    if cross['category'] == serial_table:
                                        datapoint_set.add(cross['sdsubsection'])
                                if cross['table'] == serial_table:
                                    datapoint_set.add(cross['sdsubsection'])

            for serial in serializedgrouped:
                # print(serial)

                allunsorted.update(serial)
                for serial_table, serial_dict in serial.items():

                    dataall = []
                    datapointA = {}

                    for dat in datapoint_set:

                        datapointA = {}
                        meta = {}
                        exptmeta = {'table_name__placeholder':''}
                        experimentaldata = {}
                        exptdataall = {}

                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'dataset':
                                    if cross['category']:
                                        if cross['category'] == serial_table:

                                            for k, v in serial_dict.items():

                                                if k == cross['field']:

                                                    if v not in ['None']:
                                                        nspaces.add(cross['nspace_id'])
                                                        nspacestoc.add(cross['url'])
                                                        if cross['sdsubsection'] == 'metadata':
                                                            meta.update({str(k): str(v)})
                                                        if cross['sdsubsection'] == dat:
                                                            if cross['meta'] is '1':
                                                                exptmeta.update({str(k): str(v)})
                                                            if cross['meta'] is not None:
                                                                if cross['meta'] is not '1':
                                                                    exptmeta.update({str(cross['meta']): str(v)})
                                                            if cross['meta'] is None:
                                                                if not exptmeta['table_name__placeholder']:
                                                                    exptmeta.update({'table_name__placeholder': cross['table']})
                                                                experimentaldata.update({k: str(v)})
                                                                experimentaldata.update(
                                                                    {'@id': 'value', '@type': 'sci:value'})
                                    else:
                                        if cross['table'] == serial_table:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:

                                                    if v not in ['None']:
                                                        nspaces.add(cross['nspace_id']) #$$$
                                                        nspacestoc.add(cross['url'])
                                                        if cross['sdsubsection'] == 'metadata':
                                                            meta.update({str(k): str(v)})
                                                        if cross['sdsubsection'] == dat:
                                                            if cross['meta'] is '1':
                                                                exptmeta.update({str(k): str(v)})
                                                            if cross['meta'] is not None:
                                                                if cross['meta'] is not '1':
                                                                    exptmeta.update({str(cross['meta']): str(v)})
                                                            if cross['meta'] is None:
                                                                if not exptmeta['table_name__placeholder']:
                                                                    exptmeta.update({'table_name__placeholder': cross['table']})
                                                                experimentaldata.update({k: str(v)})
                                                                experimentaldata.update(
                                                                    {'@id': 'value', '@type': 'sci:value'})

                        if experimentaldata:

                            exptdataall.update(exptmeta)
                            exptdataall.update({
                                '@id': 'datum',
                                '@type': 'sci:' + dat,
                                'value': experimentaldata
                            })

                            dataall.append(exptdataall)

                    if dataall:
                        datapointA.update(meta)
                        datapointA.update({
                            '@id': 'datapoint',
                            '@type': 'sci:datapoint',
                            'activity_id': ac['activity_id'],
                            'data': dataall
                        })

                    if datapointA:
                        datapoint.append(datapointA)
                        datagroupA.append('datapoint')
                        datapointA={}



            methodology_set = set()
            for serial in serializedgrouped:
                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['ignore'] is None:
                            if cross['sdsection'] == 'methodology':
                                if cross['table'] == serial_table:
                                    methodology_set.add(cross['sdsubsection'])
            for met in methodology_set:
                methodologyA = {}
                for serial in serializedgrouped:
                    for serial_table, serial_dict in serial.items():
                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'methodology':
                                    if cross['table'] == serial_table:
                                        if cross['sdsubsection'] == met:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:

                                                    if v not in ['None']:
                                                        nspaces.add(cross['nspace_id'])
                                                        nspacestoc.add(cross['url'])
                                                        methodologyA.update({
                                                            '@id': met,
                                                            '@type': 'sci:' + met})
                                                        methodologyA.update({k: str(v)})
                if methodologyA:
                    methodology.append(methodologyA)
            methodologyx = [i for n, i in enumerate(methodology) if i not in methodology[n + 1:]]

            system_set = set()
            systemA = {}
            for serial in serializedgrouped:

                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['ignore'] is None:
                            if cross['sdsection'] == 'system':
                                if cross['table'] == serial_table:
                                    system_set.add(cross['sdsubsection'])
            for sys in system_set:
                systemA = {}
                for serial in serializedgrouped:
                    for serial_table, serial_dict in serial.items():
                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'system':
                                    if cross['table'] == serial_table:
                                        if cross['sdsubsection'] == sys:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:
                                                    if v not in ['None']:
                                                        nspaces.add(cross['nspace_id'])
                                                        nspacestoc.add(cross['url'])
                                                        systemA.update({
                                                            '@id': sys,
                                                            '@type': 'sci:' + sys})
                                                        systemA.update({k:v})
                if systemA:
                    system.append(systemA)
            systemx = [i for n, i in enumerate(system) if i not in system[n + 1:]]

            metadata = []
            for serial in serializedgrouped:
                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['sdsection'] == 'metadata':
                            if cross['table'] == serial_table:
                                for k, v in serial_dict.items():
                                    if k == cross['field']:
                                        metadata.append({k: v, 'type': cross['sdsubsection']})
        #
            # print('xxx',metadata)

        if datagroupA:
            datagroup.append(
                {'@id': 'datagroup', '@type': 'sci:datagroup', 'chembl_id': str(allunsorted['molecule_dictionary']['chembl_id']), 'datapoints': datagroupA})
        #

        if methodology:
            test.aspects(methodologyx)
        if system:
            test.facets(systemx)
        if datapoint:
            test.datapoint(datapoint)
        if datagroup:
            test.datagroup(datagroup)
        #
        if nspaces:
            for x in nspaces:
                for y in query_crosswalks_nspaces:
                    if y['id'] == x:
                        namespace.update({y['ns']:y['path']})

        if nspacestoc:
            for x in nspacestoc:
                namespacetoc.append(x)


        if namespace:
            namespaces = ", ".join(repr(e) for e in namespace)
            test.namespace(namespace)
            test.add_namespace(addnamespace)

        if namespacetoc:
            test.ids(namespacetoc)

        relate = ''
        if relate:
            test.related(relate)



        try:
            test.add_keyword(allunsorted['activities']['type'])
        except:
            pass
        try:
            test.add_keyword(allunsorted['target_dictionary']['pref_name'])
        except:
            pass
        try:
            test.add_keyword(allunsorted['cell_dictionary']['cell_name'])
        except:
            pass
        try:
            test.add_keyword(allunsorted['molecule_dictionary']['molecule_type'])
        except:
            pass

        if datapoint:


            test.starttime()
            test.doc_id('scidata:chembl'+allunsorted['docs']['doc_id']+'_'+allunsorted['molecule_dictionary']['chembl_id'])
            test.source([{'title':allunsorted['docs']['title'],
                          'doi':allunsorted['docs']['doi'],
                          'journal':allunsorted['docs']['journal'],
                          'year':allunsorted['docs']['year'],
                          'volume':allunsorted['docs']['volume'],
                          'issue':allunsorted['docs']['issue']}])
            test.add_source([{"url": "https://www.ebi.ac.uk/chembl/document_report_card/"+allunsorted['docs']['chembl_id']+"/"}])
            test.graph_uid('scidata:chembl'+allunsorted['docs']['doc_id']+'_'+allunsorted['molecule_dictionary']['chembl_id'])
            put = test.output
            with open(str(DocumentNumber) + '_' + str(allunsorted['molecule_dictionary']['chembl_id']) + '.jsonld', 'w') as f:
                json.dump(put, f)


                #
                # other = []
                # for serial in serializedgrouped:
                #     for serial_table, serial_dict in serial.items():
                #         for cross in crosswalks:
                #             if cross['sdsection'] == 'other':
                #                 if cross['table'] == serial_table:
                #                     for k,v in serial_dict.items():
                #                         if k == cross['field']:
                #                             other.append({k:v,'type':cross['sdsubsection']})
                # print(other)

