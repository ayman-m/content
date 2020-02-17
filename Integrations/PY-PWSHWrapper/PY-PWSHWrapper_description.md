  # Integration Instructions
test
## Overview

An integration to Invoke PowerShell Code using Python, the integration spawns a new "Powershell" process, connects to it's input/output/error pipes, and obtain it's return codes. 
This integration needs to run on a remote Windows Engine with Python 3 Interpreter installed. 

## Use Cases:

* Run a Powershell Cmdlet 
* Call a Powershell Script


## Configure PY-PWSHWrapper on Demisto

1. Go to __Settings__ > __Integrations__ > __Servers & Services__ 

2. Locate __PY-PWSHWrapper__ by searching for it using the search box on the top of the page.

3. Click __Add instance__ to create and configure a new integration. You should configure the following settings:

__Username and Password__:
The credentials entered here are used to run the Cmdlet, running scripts with specific credenetials is not currently supported


##Commands

You can execute these commands from the Demisto CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.
1. pwsh-cmdlet
2. pwsh-script

###1. pwsh-cmdlet
####Input
| **Argument**|**Description** |
| :------:|:------:|
| cmdlet |	The CMDLET Command |
| args | The CMDLET Arguments |

#####Context Output
| **Path** |**Type**  | **Description**  |
| :------:|:------:|:------:|
| Pwsh | String | The Commands Outputs |

###2. pwsh-script
####Input
| **Argument**|**Description** |
| :------:|:------:|
| script-path |	The Script Path |

#####Context Output
| **Path** |**Type**  | **Description**  |
| :------:|:------:|:------:|
| Pwsh | String | The Commands Outputs |