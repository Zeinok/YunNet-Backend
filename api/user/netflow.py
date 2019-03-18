from sanic.response import json
from sanic import Blueprint

netflow = Blueprint('netflow')

@netflow.route('/netflow', methods=['GET'])
async def bp_netflow_offset(request):
    netflow_data = {'netflow': [
                        {
                            'date':'2020-1-2',
                            'lan_download':500,
                            'lan_upload':600,
                            'wan_download':32767,
                            'wan_upload':1024
                        },
                        {
                            'date':'2020-1-1',
                            'lan_download':7,
                            'lan_upload':87,
                            'wan_download':6,
                            'wan_upload':3
                        },
                    ]}
    response =  json(netflow_data)
    return response

@netflow.route('/netflow/<OFFSET>', methods=['GET'])
async def bp_netflow(request):
    netflow_data = {'netflow': [
                        {
                            'date':'2020-1-2',
                            'lan_download':500,
                            'lan_upload':600,
                            'wan_download':32767,
                            'wan_upload':1024
                        },
                        {
                            'date':'2020-1-1',
                            'lan_download':7,
                            'lan_upload':87,
                            'wan_download':6,
                            'wan_upload':3
                        },
                    ]}
    response =  json(netflow_data)
    return response
