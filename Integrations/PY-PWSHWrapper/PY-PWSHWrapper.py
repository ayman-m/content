import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

''' IMPORTS '''

import sys, subprocess
import uuid

INTEGRATION_NAME = "PY-PWSH Wrapper"
TEST_CMDLET = 'Write-Output "Test Successful"'
USERNAME = demisto.params()['credentials']['identifier'].replace("'", "''")
PASSWORD = demisto.params()['credentials']['password'].replace("'", "''")

'''' Functions '''


def create_ps_file(ps_name, ps_content):
    temp_path = os.getenv('TEMP')
    if not temp_path:
        return_error(
            "Check that the integration is using single engine without docker. If so, add TEMP variable to the environmental variables.")
    ps_path = temp_path + '\\' + ps_name
    with open(ps_path, 'w+') as file:
        file.write(ps_content)
    return ps_path


def delete_ps_file(ps_path):
    if os.path.exists(ps_path):
        os.remove(ps_path)


'''' Commands '''


def test_module():
    try:
        ps_path = create_ps_file('testcmdlet.ps1', TEST_CMDLET)
        output = subprocess.run(["powershell.exe", ps_path, "'" + USERNAME + "'", "'" + PASSWORD + "'"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout = output.stdout.strip()
        delete_ps_file(ps_path)

        if stdout == 'Test Successful':
            demisto.results('ok')
        else:
            return_error(stdout)
    except Exception as e:
        LOG(e)
        return_error(e)
    return 'ok'


def pwsh_cmdlet_run():
    args = demisto.args()
    raw = []
    context = []

    try:
        title = ("%s - Results for the CMDLET Run" % INTEGRATION_NAME)
        if 'args' in demisto.args():
            cmdlet = args.get('cmdlet') + " " + args.get('args') + " | ConvertTo-Json"
            ps_path = create_ps_file('wrapped_cmdlet.ps1', cmdlet)
            output = subprocess.run(
                ["powershell.exe", ps_path, "'" + USERNAME + "'", "'" + PASSWORD + "'"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            cmdlet = args.get('cmdlet') + "| ConvertTo-Json"
            ps_path = create_ps_file('wrapped_cmdlet.ps1', cmdlet)
            output = subprocess.run(
                ["powershell.exe", ps_path, "'" + USERNAME + "'", "'" + PASSWORD + "'"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)

        stdout = output.stdout
        stderr = output.stderr
        delete_ps_file(ps_path)

        if stderr:
            entry = {
                'Type': entryTypes['error'],
                'Contents': stderr,
                'ContentsFormat': formats['text']
            }
        else:
            raw = json.loads(stdout)
            context = raw
        context_entry = {
            "Pwsh": context
        }

        if isinstance (context_entry.get("Pwsh"),str):
            human_readable = tableToMarkdown(t=context_entry.get("Pwsh"), name=title,headers="No Header")
        elif not context_entry.get("Pwsh"):
            human_readable = tableToMarkdown(t=context_entry.get("Pwsh"), name=title, headers="No Header")
        else:
            human_readable = tableToMarkdown(t=context_entry.get("Pwsh"), name=title)

        return [human_readable, context_entry, raw]

    except Exception as e:
        LOG(e)
        return_error(e)


def pwsh_script_run():
    args = demisto.args()
    raw = []
    context = []

    try:
        title = ("%s - Results for the Script Run" % INTEGRATION_NAME)
        #cmdlet = args.get('script-path') + " " + " | ConvertTo-Json"
        ps_path = args.get('script-path') + " | ConvertTo-Json"
        output = subprocess.run(
            ["powershell.exe", ps_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        stdout = output.stdout
        stderr = output.stderr

        if stderr:
            entry = {
                'Type': entryTypes['error'],
                'Contents': stderr,
                'ContentsFormat': formats['text']
            }
        else:
            raw = json.loads(stdout)
            context = raw
        context_entry = {
            "Pwsh": context
        }

        if isinstance (context_entry.get("Pwsh"),str):
            human_readable = tableToMarkdown(t=context_entry.get("Pwsh"), name=title,headers="No Header")
        elif not context_entry.get("Pwsh"):
            human_readable = tableToMarkdown(t=context_entry.get("Pwsh"), name=title, headers="No Header")
        else:
            human_readable = tableToMarkdown(t=context_entry.get("Pwsh"), name=title)

        return [human_readable, context_entry, raw]

    except Exception as e:
        LOG(e)
        return_error(e)


def main():
    params = demisto.params()

    try:
        commands = {
            'pwsh-cmdlet': pwsh_cmdlet_run,
            'pwsh-script': pwsh_script_run,
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
