base_url = "https://192.168.x.x/api/"

#create credentials structure:
name_pwd = {'aaaUser': {'attributes': {'name': 'myname', 'pwd': "mypass" }}}
json_credentials = json.dumps(name_pwd)

# login in to API:
login_url = base_url + 'aaaLogin.json?gui-token-request=yes'
post_response = requests.post(login_url, data=json_credentials, verify=False)

# get token from login responce structure
auth = json.loads(post_response.text)
login_attributes = auth['imdata'][0]['aaaLogin']['attributes']
auth_token = login_attributes['token']
chal_token = login_attributes['urlToken']

# create cookie array from token:
cookies = {}
cookies['APIC-Cookie'] = auth_token
challenge = "&challenge=" + chal_token

# read a EPG list, incorporating token in request:
sensor_url = base_url + 'node/mo/uni/tn-<tenant-name>/ap-<App-profile-name>.json?query-target=children&target-subtree-class=fvAEPg&query-target-filter=eq(fvAEPg.isAttrBasedEPg,"false")' + challenge
get_response = requests.get(sensor_url, cookies=cookies, verify=False)
#transform json input to python object:
input_dist = get_response.json()

#Filter python object with list comprehensions:
for name in input_dist['imdata']:
	ename = name['fvAEPg']['attributes']
	ename = ename['name']
#Wirte to file:
	f = open(directory+"/"+ename+".txt","w")
	epg_request = base_url + 'node/mo/uni/tn-<tenant-name>/ap-<App-profile-name>/epg-' + ename + '.json?query-target=subtree&target-subtree-class=fvRsCons,fvRsProv' + challenge
	get_epg_response = requests.get(epg_request, cookies=cookies, verify=False)
	epg_response = get_epg_response.json()
	for contract in epg_response['imdata']:
		if  'fvRsProv' in contract:
			prov_contract = contract['fvRsProv']['attributes']
			prov_contract = prov_contract['tnVzBrCPName']
			prov_contract = ("Provider=" + prov_contract)
			f.write("%s\n" % prov_contract)
		if 'fvRsCons' in contract:
			cons_contract = contract['fvRsCons']['attributes']
			cons_contract = cons_contract['tnVzBrCPName']
			cons_contract = ("Consumer=" + cons_contract)
			f.write("%s\n" % cons_contract)
	f.close()

#Get list of Contracts:
contract_url = base_url + 'node/mo/uni/tn-<tenant-name>.json?query-target=children&target-subtree-class=vzBrCP&query-target=subtree&target-subtree-class=vzBrCP&rsp-subtree-class=vzSubj,tagInst,vzRtIf&rsp-subtree=children&order-by=vzBrCP.name' + challenge
get_cont_resp = requests.get(contract_url, cookies=cookies, verify=False)
contract_list = get_cont_resp.json()
cf = open(directory+"/portdetails.txt","w")

#Get all the port details for standard Contracts:
for cont_name in contract_list['imdata']:
	cname = cont_name['vzBrCP']['attributes']
	cname = cname['name']
	contract_request = base_url + 'node/mo/uni/tn-<tenant-name>/brc-' + cname + '/subj-' + cname +'.json?query-target=children&target-subtree-class=vzRsSubjFiltAtt' + challenge
	get_contract_response = requests.get(contract_request, cookies=cookies, verify=False)
	contract_response = get_contract_response.json()
  
#Get all the port details for External Contracts:
	for tcount in contract_response['totalCount']:
		if tcount == '0':
			ext_contract_request = base_url + 'node/mo/uni/tn-<tenant-name>/brc-' + cname + '/subj-' + cname +'/intmnl.json?query-target=children&target-subtree-class=vzRsFiltAtt' + challenge
			get_ext_contract_request = requests.get(ext_contract_request, cookies=cookies, verify=False)
			ext_contract_json = get_ext_contract_request.json()
			for ext_contract in ext_contract_json['imdata']:
				if 'vzRsFiltAtt' in ext_contract:
					ext_contact_name = ext_contract['vzRsFiltAtt'] ['attributes']
					ext_contact_name = ext_contact_name['tnVzFilterName']
					ext_contact_name = (cname + '=' + ext_contact_name)
					cf.write("%s\n" % ext_contact_name)
	for filt_name in contract_response['imdata']:
		if 'vzRsSubjFiltAtt' in filt_name:
			cont_filt_name = filt_name['vzRsSubjFiltAtt']['attributes']
			cont_filt_name = cont_filt_name['tnVzFilterName']
			cont_filt_name = (cname + "=" + cont_filt_name)
			cf.write("%s\n" % cont_filt_name)
cf.close()
