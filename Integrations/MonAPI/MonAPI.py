import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *
INTEGRATION_NAME = "MonAPI Integration"

'''API Client'''


class Client:
    def __init__(self, url, api_version, token, proxies):
        self.base_url = url
        self.api_version = api_version
        self.proxies = proxies
        self.token=token

    def query(self, params=None, data=None, suffix=None):
        LOG('running request with url=%s' % self.base_url)
        suffix = suffix
        full_url = urljoin(urljoin(self.base_url, self.api_version+"/"+suffix))+params
        res=requests.request(
            "GET",
            full_url,
            headers={'authorization': self.token,
                     'accept': "application/json"
                     }
        )
        if res.status_code not in [200, 204]:
            raise ValueError("Error in API call to Service API %s. Reason: %s " % (res.status_code,res.text))
        try:
            return res.json()
        except Exception:
            raise ValueError("Failed to parse http response to JSON format. Original response body: \n %s" % res.text)


'''' Helper Functions '''


def calculate_dbot_score(threat_data):
    threat_level = threat_data
    if threat_level:
        if threat_level == 'low':
            return dbotscores['Low']
        elif threat_level == 'medium':
            return dbotscores['Medium']
        if threat_level == 'high':
            return dbotscores['High']
    return 'low'


'''' Commands '''

def test_module(client):
    try:
        client.query(params='8.8.8.8',suffix='ip')
    except Exception as e:
        LOG(e)
        return_error(e)
    return 'ok'


def check_ip_reputation(client,ip_address):
    try:
        title = ("%s - Results for IP Query" % INTEGRATION_NAME)
        raws = []
        ip_ec = []
        monapi_ec = []
        dbotscore_ec = []

        raw_response=client.query(params=ip_address,suffix='ip')

        if raw_response:
            raws.append(raw_response)
            ip_ec.append({
                'Address': raw_response.get('ip'),
                'ASN': raw_response.get('asn_number'),
                'Geo': {
                    'Country': raw_response.get('iso_code'),
                    'Location': (raw_response.get("latitude"),raw_response.get("longitude"))
                }
            })
            monapi_ec.append({
                'IP': {
                    'Reputation': raw_response.get('threat_level'),
                    'IP': raw_response.get('ip'),
                    'Lists': raw_response.get('blacklists')
                }
            })
            dbotscore_ec.append({
                'Indicator': raw_response.get('ip'),
                'Score': calculate_dbot_score(raw_response.get('threat_level')),
                'Type': 'ip',
                'Vendor': 'MonAPI'
            })
        if not raws:
            return ("%s - Could not find any results for given query" % INTEGRATION_NAME)

        context_entry = {
            outputPaths.get("ip"): ip_ec,
            "MonAPI": monapi_ec,
            outputPaths.get("dbotscore"): dbotscore_ec
         }

        human_readable = tableToMarkdown(t=context_entry.get("MonAPI"),name=title)

        return [human_readable,context_entry,raws]

    except Exception as e:
        LOG(e)
        return_error(e)


def main():
    params = demisto.params()
    args = demisto.args()
    token = params.get('token')
    ip_address = args.get('ip')
    domain_name = args.get('domain')

    # Remove trailing slash to prevent wrong URL path to service
    url = params['url'][:-1] if (params['url'] and params['url'].endswith('/')) else params['url']
    api_version = params.get('version')
    # Remove proxy if not set to true in params
    proxies = handle_proxy()
    try:
        client = Client(url, api_version, token, proxies)
        commands = {
            'ip': check_ip_reputation(client,ip_address),
        }

        command = demisto.command()
        LOG('Command being called is %s' % command)

        if command in commands:
            outputs=commands[command]
            return_outputs(outputs[0],outputs[1],outputs[2])
        else:
            return_error("Command Not Found")

    except Exception as e:
        return_error(str(e))

if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
