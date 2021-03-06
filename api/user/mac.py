from sanic.log import error_logger
from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc, api
import re

from Base import messages
from Base.MongoDB.mac import log_mac_change
from Decorators import permission
from Query import MAC
from Query.ip import Ip

bp_mac = Blueprint("mac")

# TODO(biboy1999): management logic or not belong here :/
# @bp_mac.route("/<ip>/mac", methods=["GET"])
# async def bp_ip_get_owned_ip_mac(request, username, ip):
#     response = json()
#     return response


class user_set_owned_ip_mac_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        mac = doc.String("Mac address")

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    class FailResp:
        code = 500
        description = "On failed request"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    class AuthResp:
        code = 401
        description = "On failed Auth"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp, AuthResp]


@user_set_owned_ip_mac_doc
@bp_mac.route("/<ip>/mac", methods=["PATCH"])
@permission("api.ip.mac.edit")
async def bp_ip_set_owned_ip_mac(request, username, ip):
    username = request["username"]
    mac = request.json["mac"]

    ips = await Ip.get_user_own_ip(username)
    target_ip = next((i for i in ips if i["ip"] == ip), None)

    if re.match("^([0-9A-Fa-f]{12})$", mac) is None:
        return messages.INVALID_MAC
    # cant edit not owned ip
    if target_ip is None:
        return messages.NO_PERMISSION
    if await MAC.set_mac(target_ip["ip"], mac):
        await log_mac_change(ip, username, target_ip["mac"], mac)        
        return messages.OPERATION_SUCCESS
    else:
        error_logger.error("Operation failed")
        error_logger.error(request.url)
        error_logger.error(target_ip)
        error_logger.error(mac)
        return messages.INTERNAL_SERVER_ERROR

