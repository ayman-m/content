import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *
''' IMPORTS '''

INTEGRATION_NAME = "Atom PY"


def test_module():
    try:
        x = 1 + 1
    except Exception as e:
        LOG(e)
        return_error(e)
    return 'ok'


def atom():
    args = demisto.args()
    orbit = args.get('orbit')
    center = args.get('center')
    raw = []
    context = []
    try:
        title = ("%s - Results for Atom Query" % INTEGRATION_NAME)

        if orbit == 'true' and center == 'true':
            raw.append({
                'orbit': 'electron',
                'center': 'nucleus'
            })
            context.append({
                'orbit': 'electron',
                'center': 'nucleus'
            })
        elif center == 'true':
            raw.append({'center': 'nucleus'})
            context.append({'center': 'nucleus'})
        elif orbit == 'true':
            raw.append({'orbit': 'electron'})
            context.append({'orbit': 'electron'})

        context_entry = {
            "Atom": context
        }

        human_readable = tableToMarkdown(t=context_entry.get("Atom"), name=title)

        return [human_readable, context_entry, raw]

    except Exception as e:
        LOG(e)
        return_error(e)


def main():
    params = demisto.params()

    try:
        commands = {
            'atom': atom,
            'test-module': test_module
        }

        command = demisto.command()
        LOG('Command being called is %s' % command)

        if command in commands:
            if command == 'test-module':
                return_outputs(test_module())

            else:
                outputs = commands[command]()
                return_outputs(outputs[0], outputs[1], outputs[2])
        else:
            return_error("Command Not Found")

    except Exception as e:
        return_error(str(e))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
