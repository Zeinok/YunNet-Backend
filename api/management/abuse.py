from sanic.request import Request
from sanic.response import json
from sanic import Blueprint
from sanic.log import logger
from datetime import datetime
from sanic_openapi import doc, api
from sanic_openapi.doc import JsonBody
import asyncio

import config
from Base import messages
from Base.types import LockTypes
from Query import Lock, User
from Decorators import permission
from BackgroundJobs.switch_update import do_switch_update
from Query.ip import Ip
from Base.MongoDB.lock import log_lock, log_unlock

bp_abuse = Blueprint("management-abuse")


class abuse_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        title = doc.String("lock title for public")
        description = doc.String("description only for admin")
        lock_until = doc.Date("YYYY-MM-DD")
        no_update = doc.Boolean("Should do switch_update(dev only)")

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 200
        description = "On request succeded"

        class model:
            message = doc.String("OPERATION_SUCCESS")

        model = dict(vars(model))

    class FailResp:
        code = 400
        description = "On failed request"

        class model:
            message = doc.String("BAD_REQUEST")

        model = dict(vars(model))

    class ServerFailResp:
        code = 500
        description = "When server failed to process the response"

        class model:
            message = doc.String("INTERNAL_SERVER_ERROR")

        model = dict(vars(model))

    class AuthResp:
        code = 401
        description = "On failed auth"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp, ServerFailResp, AuthResp]


@abuse_doc
@bp_abuse.route("/abuse/<ip>", methods=["PUT"], strict_slashes=True)
@permission("api.ip.lock.add")
async def bp_abuse_put(request: Request, ip):
    try:
        title = request.json["title"]
        description = request.json["description"]
        lock_until_str = request.json["lock_until"]

        if None in (title, description):
            return messages.BAD_REQUEST

        lock_until = None
        no_update = False
        if "no_update" in request.json.keys():
            if request.json["no_update"]:
                no_update = True

        if lock_until_str is not None:
            lock_until = datetime.strptime(lock_until_str, "%Y-%m-%d")
        locked_by = await User.get_user_id(request["username"])

        ip_data = await Ip.get_ip_by_id(ip)
        uid = ip_data["uid"]
        gid = ip_data["gid"]

    except Exception as e:
        logger.debug(e.with_traceback())
        return messages.BAD_REQUEST

    await Lock.set_lock(
        ip, 0, datetime.now(), lock_until, title, description, uid, gid, locked_by
    )
    app_config: config = request.app.config
    await log_lock(ip, uid, locked_by, lock_until)
    if not no_update:
        asyncio.create_task(do_switch_update(app_config.MAC_UPDATER_ENDPOINT, True))
    return messages.ACCEPTED


class unlock_abuse_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = False

    class consumes:
        unlock_date = doc.Date(
            "Set unlock date. if not provided will unlock immediately"
        )

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 200
        description = "On request succeded"

        class model:
            message = doc.String("OPERATION_SUCCESS")

        model = dict(vars(model))

    class FailResp:
        code = 400
        description = "On failed request"

        class model:
            message = doc.String("BAD_REQUEST")

        model = dict(vars(model))

    class ServerFailResp:
        code = 500
        description = "When server failed to process the response"

        class model:
            message = doc.String("INTERNAL_SERVER_ERROR")

        model = dict(vars(model))

    class AuthResp:
        code = 401
        description = "On failed auth"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp, ServerFailResp, AuthResp]


@unlock_abuse_doc
@bp_abuse.route("/abuse/<ip>", methods=["DELETE"], strict_slashes=True)
@permission("api.ip.lock.edit")
async def bp_abuse_unlock(request: Request, ip):
    try:

        if request.json is not None and "unlock_date" in request.json:
            date = request.json["unlock_date"]
            datetime.strptime(date, "%Y-%m-%d")
            await Lock.unlock(ip, date)
        else:
            date = datetime.now()
            await Lock.unlock(ip)

        app_config: config = request.app.config
        asyncio.create_task(do_switch_update(app_config.MAC_UPDATER_ENDPOINT, True))

        unlocked_by = await User.get_user_id(request["username"])

        ip_data = await Ip.get_ip_by_id(ip)
        uid = ip_data["uid"]
        gid = ip_data["gid"]

        await log_unlock(ip, uid, unlocked_by, date)
        return messages.ACCEPTED
    except Exception as e:
        logger.debug(e.with_traceback())
        return messages.BAD_REQUEST
