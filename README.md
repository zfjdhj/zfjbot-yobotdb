# zfjbot-yobotdb

a plugin for hoshino

## 说明

数据库操作有风险，一切操作后果自行承担。

自用，代码废物，不保证代码可用以及不承担可能会出现的任何后果。

## 插件安装

1. 默认安装方式

2. 修改`main.py`中的`db_path`为yobot数据库位置。

## 指令（仅主人可用）

| 指令 | 功能 |
| :- | :- |
| yobotdb 增加数据 [昨日] <伤害> <周目> \<boss\> [尾刀\|补偿刀] [@某人] | 增加(昨日)出刀数据 |
| yobotdb 删除数据 [昨日] <伤害> [@某人] | 删除(昨日)出刀数据 |
| yobotdb 修改数据 [昨日] <旧伤害> <新伤害> [@某人] | 修改(昨日)出刀数据 |
| yobotdb 查看数据 [昨日] | 查看(昨日)出刀数据|
