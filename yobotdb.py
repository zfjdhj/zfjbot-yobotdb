import sqlite3


class yobotdb:
    def __init__(self, db_path: str, group_id: int):
        self.db_path = db_path
        self.group_id = group_id

    def add_battle_data(self, data: dict):
        conn = sqlite3.connect(self.db_path)
        sql = f"""insert into clan_challenge {tuple(data.keys())} values {tuple(data.values())}"""
        conn.execute(sql)
        conn.commit()
        conn.close()
        return

    def delete_data(self, qqid: int, damage: int, pcr_date: int):
        conn = sqlite3.connect(self.db_path)
        sql = f"""delete from clan_challenge 
                where gid={self.group_id} 
                and qqid={qqid}
                and challenge_damage={damage}
                and challenge_pcrdate={pcr_date}"""
        conn.execute(sql)
        conn.commit()
        conn.close()
        return

    def get_data(self, data: dict, pcr_date: int):
        conn = sqlite3.connect(self.db_path)
        sql = f"""select * from clan_challenge
                where gid={data["gid"]} 
                and qqid={data["qqid"]}
                and challenge_pcrdate={pcr_date}"""
        data_res = conn.execute(sql)
        res = []
        for item in data_res:
            res.append(item)
        conn.commit
        conn.close()
        return res

    def get_bid(self):
        conn = sqlite3.connect(self.db_path)
        data = conn.execute("SELECT * from clan_challenge where gid = %s " % (self.group_id))
        bid_tmp = 0
        for item in data:
            if item[1] > bid_tmp:
                bid_tmp = item[1]
        conn.close()
        return bid_tmp

    def get_challenge_today_total(self, pcrdate_today: int) -> list:
        challenge_list = []
        conn = sqlite3.connect(self.db_path)
        data = conn.execute(
            "SELECT * from clan_challenge where challenge_pcrdate = %s and gid = %s and not is_continue = true"
            % (pcrdate_today, self.group_id)
        )
        for x in data:
            data2 = conn.execute("select * from user where qqid = %d" % x[3])
            for y in data2:
                challenge_list.append(y[0])
        conn.close()
        return challenge_list

    def get_user_list(self) -> list:
        user_list = []
        conn = sqlite3.connect(self.db_path)
        nickname_data = conn.execute("select * from clan_member where group_id = %d" % self.group_id)
        for item in nickname_data:
            user_list.append(item[1])
        conn.close()
        return user_list

    def get_qqid_nickname(self, qq_id: int) -> dict:
        qqid_nickname = {}
        # qqid_nickname = {"qqid":"nickname"}
        conn = sqlite3.connect(self.db_path)
        data = conn.execute("select * from user where qqid = %d" % qq_id)
        for item in data:
            qqid_nickname[item[0]] = item[1]
        return qqid_nickname

    def get_battle_damage_today_all(self, pcrdate_today: int, group_id: int) -> dict:
        # 返回dict={damage:nickname,...}
        challenge_list = {}
        print(self.db_path)
        conn = sqlite3.connect(self.db_path)
        try:
            data = conn.execute(
                "SELECT * from clan_challenge where challenge_pcrdate = %s and gid = %s" % (pcrdate_today, group_id)
            )
            for x in data:
                data2 = conn.execute("select * from user where qqid = %d" % x[3])
                for y in data2:
                    challenge_list[f"{x[9]}"] = y[1]
            conn.close()
            return challenge_list
        except Exception as e:
            conn.close()
            return {"status": "error", "msg": str(e)}

    def set_battle_damage_today(self, today: int, qqid: int, old_damage: int, new_damage: int) -> dict:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                "update clan_challenge set challenge_damage = %s where challenge_pcrdate=%s and gid = %s and qqid = %s and challenge_damage = %s"
                % (new_damage, today, self.group_id, qqid, old_damage)
            )
            conn.commit()
            conn.close()
            return {"status": "success", "msg": "修改成功"}
        except Exception as e:
            conn.close()
            return {"status": "error", "msg": str(e)}
