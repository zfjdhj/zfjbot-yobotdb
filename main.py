import time
from datetime import datetime
from .yobotdb import yobotdb

import hoshino
from hoshino import Service, priv
from hoshino import *


db_path = "C:/tmp/xcwbot/xcwbot/HoshinoBot_go/hoshino/modules/yobot/yobot/src/client/yobot_data/yobotdata.db"

sv = Service("zfjbot-yobotdb")


async def get_bid(group_id: int) -> int:
    yobotdb_tmp = yobotdb(db_path, group_id)
    res = yobotdb_tmp.get_bid()
    return res


## 增加一条报刀数据默认时间12：00
async def add_battle_data(group_id: int, data: dict) -> str:
    new_dict = {
        "bid": await get_bid(group_id),
        "gid": group_id,
        "qqid": data["qqid"],
        "challenge_pcrdate": (int(time.time() + 3600 * 3) // 86400) + int(data["challenge_pcrdate"]),
        "challenge_pcrtime": 25200,
        "boss_health_ramain": data["boss_health_ramain"],
        "boss_cycle": data["boss_cycle"],
        "boss_num": data["boss_num"],
        "challenge_damage": data["challenge_damage"],
        "is_continue": data["is_continue"],
    }
    yobotdb_tmp = yobotdb(db_path, group_id)
    reply = yobotdb_tmp.add_battle_data(new_dict)
    test = yobotdb_tmp.get_data(new_dict, new_dict["challenge_pcrdate"])
    for item in test:
        if int(item[9]) == int(data["challenge_damage"]):
            reply = "添加数据成功"
    if reply:
        return reply
    return "添加数据失败"


## 删除一条报刀数据
async def delete_battle_data(group_id: int, pcr_date: int, qqid: int, damage: int) -> str:
    yobotdb_tmp = yobotdb(db_path, group_id)
    new_today = int(time.time() + 3600 * 3) // 86400 + pcr_date
    reply = yobotdb_tmp.delete_data(qqid, damage, new_today)
    test = yobotdb_tmp.get_data({"gid": group_id, "qqid": qqid}, new_today)
    for item in test:
        if item[9] == damage:
            reply = "删除数据失败"
    if reply:
        return reply
    return "删除数据成功"


## 修改一条报刀数据
async def change_battle_data(today: int, group_id: int, qqid: int, old_damage: int, new_damage: int) -> str:
    yobotdb_tmp = yobotdb(db_path, group_id)
    new_today = int(time.time() + 3600 * 3) // 86400 + today
    res = yobotdb_tmp.set_battle_damage_today(new_today, qqid, old_damage, new_damage)
    reply = ""
    if res["status"] == "success":
        reply = "修改数据成功"
    elif res["status"] == "error":
        reply = res["msg"]
    return reply


## 查看[昨日]报刀数据
async def get_battle_data(group_id: int, today: int) -> str:
    new_today = int(time.time() + 3600 * 3) // 86400 + today
    yobotdb_tmp = yobotdb(db_path, group_id)
    result = yobotdb_tmp.get_battle_damage_today_all(new_today, group_id)
    reply = f"报刀数据{len(result)}条"
    for (x, y) in result.items():
        reply += f"\n{x}:{y}"
    return reply


## 指令部分
HELP_MSG = """
yobotdb 增加数据 [昨日] <伤害> <周目> <boss> [尾刀] [@某人]>：增加(昨日)出刀数据
yobotdb 删除数据 [昨日] <伤害> [@某人]：删除(昨日)出刀数据
yobotdb 修改数据 [昨日] <旧伤害> <新伤害> [@某人]：修改(昨日)出刀数据
yobotdb 查看数据 [昨日]：查看(昨日)出刀数据
"""


@sv.on_prefix("yobotdb")
async def zfjbot_yobotdb(bot, ev):
    msg = ""
    user_id = ev.user_id
    target_id = 0
    for m in ev.message:
        if m.type == "at" and m.data["qq"] != "all":
            target_id = int(m.data["qq"])
    group_id = ev.group_id
    args = ev.message.extract_plain_text().split()
    print([item for item in args])
    is_admin = priv.check_priv(ev, priv.SUPERUSER)
    # is_admin = priv.check_priv(ev, priv.ADMIN)
    if len(args) == 0:
        msg = HELP_MSG
    elif args[0] == "增加数据":
        if is_admin:
            data = {
                "qqid": target_id,
                "challenge_pcrdate": 0,
                "boss_cycle": 0,
                "boss_num": 0,
                "boss_health_ramain": 1,
                "challenge_damage": 0,
                "is_continue": 0,
            }
            if len(args) == 4:
                if target_id == 0:
                    data["qqid"] = user_id
                data["boss_cycle"] = args[2]
                data["boss_num"] = args[3]
                data["challenge_damage"] = args[1]
            elif len(args) == 5:
                data["boss_cycle"] = args[2]
                data["boss_num"] = args[3]
                data["challenge_damage"] = args[1]
                if target_id == 0:
                    data["qqid"] = user_id
                if args[4] == "尾刀":
                    data["boss_health_ramain"] = 0
                elif args[4] == "补偿刀":
                    data["is_continue"] = 1
                elif args[1] == "昨日":
                    data["boss_cycle"] = args[3]
                    data["boss_num"] = args[4]
                    data["challenge_damage"] = args[2]
                    data["challenge_pcrdate"] = -1
            elif len(args) == 6:
                if target_id == 0:
                    data["qqid"] = user_id
                data["boss_cycle"] = args[3]
                data["boss_num"] = args[4]
                data["challenge_damage"] = args[2]
                data["challenge_pcrdate"] = -1
                if args[4] == "尾刀":
                    data["boss_health_ramain"] = 0
                elif args[4] == "补偿刀":
                    data["is_continue"] = 1
            else:
                msg = "参数错误\n" + HELP_MSG
            msg = await add_battle_data(group_id, data)
        else:
            msg = "权限不足"
    elif args[0] == "删除数据":
        if is_admin:
            pcr_date = 0
            if len(args) == 2:
                if target_id == 0:
                    msg = await delete_battle_data(group_id, pcr_date, user_id, args[1])
                else:
                    msg = await delete_battle_data(group_id, pcr_date, target_id, args[1])
            elif len(args) == 3:
                if target_id != 0:
                    msg = await delete_battle_data(group_id, pcr_date - 1, target_id, args[2])
                else:
                    msg = await delete_battle_data(group_id, pcr_date - 1, user_id, args[2])
            else:
                msg = "参数错误\n" + HELP_MSG
        else:
            msg = "权限不足"
    elif args[0] == "修改数据":
        if is_admin:
            if len(args) == 3:
                if target_id == 0:
                    msg = await change_battle_data(0, group_id, user_id, args[1], args[2])
                else:
                    msg = await change_battle_data(0, group_id, target_id, args[1], args[2])
            elif len(args) == 4:
                if target_id == 0 and args[1] == "昨日":
                    msg = await change_battle_data(-1, group_id, user_id, args[1], args[2])
                else:
                    msg = await change_battle_data(-1, group_id, target_id, args[1], args[2])
            else:
                msg = "参数错误\n" + HELP_MSG
        else:
            msg = "权限不足"
    elif args[0] == "查看数据":
        if is_admin:
            if len(args) == 1:
                msg = await get_battle_data(group_id, 0)
            elif len(args) == 2 and args[1] == "昨日":
                msg = await get_battle_data(group_id, -1)
            else:
                msg = "参数错误\n" + HELP_MSG
        else:
            msg = "权限不足"
    await bot.send(ev, msg)