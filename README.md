# Cisco-ACI-Datacenter / PYTHON SDK + REST
Cisco-ACI automation with REST API &amp; Python

Summary:
This repository contains HOW TO automate cisco ACI platform which enables CI/CD in datacenter networking. There are multiple ways to configure Cisco ACI. Here we follow Python SDK + REST. 

Prerequisite:
Install Ubuntu 16.04 server in your VM. Follow the below link to install the SDK(.eggs) in your ubuntu VM.

https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/1-x/api/python/install/b_Install_Cisco_APIC_Python_SDK_Standalone.html

Building scripts step by step:

1) Login into Cisco ACI:
 Use the below code to create a Login session. This Loginsession can be used to query, create/delete from the end point.
 
"from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
session = LoginSession('https://sample-host.coolapi.com', 'admin',
                       'xxx?xxx?xxx')
moDir = MoDirectory(session)
moDir.login()"

2) Modules required to import are as follows.

MoDirectory : Handels the session info
LoginSession : used to send user credentials to create session
ConfigRequest : to commit config 
Ap : Application profile creation
AEPg : EPG creation
BD : Bridge domain creation
Ctx, RsCtx :  assocated with VRF and BD.
RsProv, RsCons, RsBd, Subnet, RsABDPolMonPol : Contract as provider and consumer.
Filter, Entry, BrCP, Subj, RsSubjFiltAtt, InTerm, OutTerm, RsFiltAtt : used to create filters. 

3) Below is the flow to configure Cisco ACI.

1)Tenent
  a)	VRF
    i)	Bridge Domain
     (1)	Subnet/Gateway
  b)	Application Profile
    i)	EPG
     (1)	Contract as consumer
     (2)	Contract as provider
  c)	Filters
    i)	Filter entries(ex:port:80)
  d)	Contract
    i)	filters
    
 4) Python SDK connection:
     Python SDK connects to Cisco ACI with REST API, This supports only Json or xml. 
     
 5) Config File:
     You can write the config in a file. Python will reads the file and construct the json and send to Rest API. The config file can be in any format as per your comfort. We are using YAML format for config file. 
     

Source : Cisco APIC Python SDK Documentation
https://cobra.readthedocs.io/en/latest/index.html
