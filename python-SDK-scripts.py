Login to APIC:
    apicUrl = 'https://' + str(host)
    loginSession = LoginSession(apicUrl, user, password)
    moDir = MoDirectory(loginSession)
    moDir.login()
    return moDir


Create Tenent:
    from cobra.model.fv import Tenant
    from cobra.mit.request import ConfigRequest
    fvTenantMo = Tenant(uniMo, 'Tenant1')
    cfgRequest = ConfigRequest()
    cfgRequest.addMo(fvTenantMo)
    moDir.commit(cfgRequest)

Create Filters-entries:
        entryMo = Entry(filter_obj, filter_entry_name)
        entryMo.dFromPort = entry['dFromPort']    # HTTP port
        entryMo.dToPort = entry['dToPort']
        entryMo.sFromPort = entry['sFromPort']
        entryMo.sToPort = entry['sToPort']
        entryMo.prot = entry['prot']          # TCP protocol number
        entryMo.etherT = entry['etherT']
        entryMo.tcpRules = entry['tcp_flag']
        
Create Contracts:
            filterMo = create_filter_inside(fv_tenant, filter_entry_name)
            create_filter_entries(filterMo, **filter_entries)
        vz_ct = BrCP(fv_tenant, name=each_contract, prio='unspecified')
        vzSubj = Subj(vz_ct, revFltPorts=u'false', name=each_contract,
                      targetDscp=u'unspecified')
        RsSubjFiltAtt(vzSubj, tnVzFilterName=filterMo.name)
        
Create External Contract:
                vzSubj = Subj(vz_ct, revFltPorts=u'false', name=each_contract,
                              targetDscp=u'unspecified')
                vzInTerm = InTerm(vzSubj, name='', prio='unspecified', targetDscp='unspecified')
                vzOutTerm = OutTerm(vzSubj, name='', prio='unspecified', targetDscp='unspecified')

                for each_term_entry, filter_name in term_name.iteritems():
                # print each_term_entry  -> InTerm; OutTerm
                # print filter_name -> ['HTTPPort','ICMP'];[HTTPSPort]

                    for every_filter in filter_name:
                    # print every_filter  -> HTTPPort; ICMP; HTTPSPort
                    # print each_term_entry

                        if each_term_entry == 'InTerm':
                            RsFiltAtt(vzInTerm, tnVzFilterName=every_filter)

                        if each_term_entry == 'OutTerm':
                            RsFiltAtt(vzOutTerm, tnVzFilterName=every_filter)


Create BD:
            fvBDMo = BD(tenant, bd_name)
            # Association between BD and VRF
            RsCtx(fvBDMo, tnFvCtxName=vrf_obj.name)
            for each_bdname, each_values in bd_values.iteritems():
                for each_entry, entry_values in each_values.iteritems():
                    if each_entry=='subnet': # Gateway ip add
                        Subnet(fvBDMo,ip=entry_values['ip'],scope=entry_values['scope'])
                    if each_entry=='monitoringpolicy': # Monitoring Policy
                        RsABDPolMonPol(fvBDMo,tnMonEPGPolName=entry_values['policyname'])
                        
Create EPG: #
        fvApMo = Ap(tenant, each_app)
        for epg_name, epg_value in tmd['application_profile'][each_app].iteritems():
            # Following Creates EPGs
            fvEPGMo = AEPg(fvApMo, epg_name)

            # Following attaches Bridge Domain BD to EPGs
            if 'bd' in epg_value:
                for each_bd in epg_value['bd']:
                    RsBd(fvEPGMo, tnFvBDName=each_bd)

            # Following Attaches Consumer Contracts with EPGs as defined in YAML
            if 'RsCons' in epg_value:
                for each_rscons in epg_value['RsCons']:
                    RsCons(fvEPGMo, each_rscons)

            # Following Attaches Producer Contracts with EPGs as defined in YAML
            if 'RsProv' in epg_value:
                for each_rsprov in epg_value['RsProv']:
                    RsProv(fvEPGMo, each_rsprov)
