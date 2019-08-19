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
LoginSession : used to send user credientals to create session
ConfigRequest : to commit config 
Ap : Application profile creation
AEPg : EPG creation
BD : Bridge domain creation
Ctx, RsCtx :  assocated with VRF and BD.
RsProv, RsCons, RsBd, Subnet, RsABDPolMonPol : Contract as provider and consumer.
Filter, Entry, BrCP, Subj, RsSubjFiltAtt, InTerm, OutTerm, RsFiltAtt : used to create filters. 

3) Below is the flow to configure Cisco ACI.

•	Tenent
  o	VRF
    	Bridge Domain
      •	Subnet/Gateway
  o	Application Profile
    	EPG
      •	Contract as consumer
      •	Contract as provider
  o	Filters
    	Filter entries(ex:port:80)
  o	Contract
    	filters



