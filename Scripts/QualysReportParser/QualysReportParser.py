import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

import json
import re

args = demisto.args()
file_enry = args.get('entryID')
cve_expression = re.compile('CVE-\d{4}-\d{4,7}')

report = demisto.getFilePath(file_enry)

with open(report['path'], 'r') as f:
    data = f.read().decode('unicode_escape').encode('utf-8')

raw = []
cve_found = []
cve_context = []
qid_context = []

if data:
    report_json = json.loads(xml2json(data))

    generation_date = report_json['ASSET_DATA_REPORT']['HEADER']['GENERATION_DATETIME']

    #Get asset list
    asset_list = report_json['ASSET_DATA_REPORT']['HOST_LIST']['HOST']


    if not asset_list:
        demisto.results( {
            "Type" : entryTypes["note"],
            "ContentsFormat" : formats["text"],
            "Contents" : 'No vulnerable assets were found'
        } )
        sys.exit(0)

    if not isinstance(asset_list, list):
        asset_list = [asset_list]

    # Get list of Vulnerabilities
    general_vulnerabilities = argToList(report_json['ASSET_DATA_REPORT']['GLOSSARY']['VULN_DETAILS_LIST']['VULN_DETAILS'])
    if not isinstance(general_vulnerabilities, list):
        general_vulnerabilities = [general_vulnerabilities]

    #Get list of QID
    qid_text = [demisto.get(vulnerability,"QID.#text") for vulnerability in general_vulnerabilities]

    #Get list of CVE
    for vulnerablity in general_vulnerabilities:
        cve = demisto.get(vulnerablity,"CVE_ID_LIST.CVE_ID")
        if cve is not None:
            cve_found.append (cve)
    cve_id = list(dict.fromkeys(cve_expression.findall(str(cve_found))))

    raw.append(cve_id)
    raw.append(qid_text)

    cve_context.append(cve_id)
    qid_context.append(qid_text)

    context_entry = {
        "Vulnerabilities.CVE": cve_context,
        "Vulnerabilities.QID": qid_context
    }

    human_readable = tableToMarkdown(t=context_entry.get("Vulnerabilities.CVE"), name="CVE's",headers=["CVE's"])
    human_readable += tableToMarkdown(t=context_entry.get("Vulnerabilities.QID"), name="QID's",headers=["QID's"])

    return_outputs(human_readable, context_entry, raw)

else:
    demisto.results( {
        "Type" : entryTypes["error"],
        "ContentsFormat" : formats["text"],
        "Contents" : 'No data could be read.'
    } )




