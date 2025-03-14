# -*- coding: utf-8 -*-
# @Time    : 2025/3/14 上午9:29
# @Author  : wm
# @Software   : PyCharm
from pyswmm import Simulation, Nodes, Subcatchments, LidGroups, LidControls
from pyswmm.swmm5 import PYSWMMException

with Simulation('test.inp') as sim:
    a = LidGroups(sim)
    print(LidGroups(sim))
    print(type(LidGroups(sim)))
    print('---------------------------------------------------')
    print(LidGroups(sim)['SUB00079'])
    print(type(LidGroups(sim)['SUB00079']))
    print('---------------------------------------------------')
    print(LidGroups(sim)['SUB00079'][0])
    print(type(LidGroups(sim)['SUB00079'][0]))
    print('---------------------------------------------------')
    print(LidGroups(sim)['SUB00079'][1])
    print('---------------------------------------------------')
    print(LidGroups(sim)['SUB00080'][0])
    print('---------------------------------------------------')

    # 用于计算前赋值及目标函数1
    print("尝试遍历所有LID单元......")
    success_counter = 0
    for lid_group in LidGroups(sim):
        try:
            for lid_unit in lid_group:
                # lid_unit.lid_control:str LID设施的用户命名名称
                # lid_unit.subcatchment:str lid_unit对应的子汇水区编号
                # 获取对应的LID类型
                if 'BC' in lid_unit.lid_control:
                    print(f"当前子汇水区: {lid_unit.subcatchment} 中的lid_unit: {lid_unit.lid_control} 的LID类型为: 生物滞留网格，面积为: {str(lid_unit.unit_area)}")
                elif 'RG' in lid_unit.lid_control:
                    print(f"当前子汇水区: {lid_unit.subcatchment} 中的lid_unit: {lid_unit.lid_control} 的LID类型为: 雨水花园，面积为: {str(lid_unit.unit_area)}")

                print('---------------------------------------------------')
                # 这里可以将lid_group[0].unit_area赋给x[success_counter]
                # ......
                success_counter += 1  # 这个变量代表x的索引

        except PYSWMMException as e:
            if "Lid Unit Does Not Exist" in str(e):
                continue
            else:
                print(f"出现了其他异常: {str(e)}")

    print(f"成功访问unit_area的次数: {success_counter}")

    # 计算前查看某个子汇水区属性，发现没有statistics属性
    SUB00079 = Subcatchments(sim)['SUB00079']

    # 计算测试
    print("开始计算......")
    for step in enumerate(sim):
        pass
    print("计算结束......")

    # 计算后查看某个子汇水区属性
    SUB00079 = Subcatchments(sim)['SUB00079']

    # 获取子汇水区数量
    print(f"共有 {Subcatchments(sim)._nSubcatchments} 个子汇水区")

    # 遍历所有子汇水区以获取径流深，用于目标函数2
    print("开始遍历所有子汇水区以获取径流深(mm)......")
    for subcatchment in Subcatchments(sim):
        subcatchment_runoff_mm = subcatchment.statistics['runoff'] / subcatchment.area / 10
        print(f"子汇水区: {subcatchment.subcatchmentid} 的总径流体积为: {subcatchment.statistics['runoff']} m^3，总径流深为: {subcatchment_runoff_mm} mm")
        print('---------------------------------------------------')

    # 获取节点数量
    print(f"共有 {Nodes(sim)._nNodes} 个节点")

    # 遍历所有节点以获取平均超载时间，用于目标函数3
    print("开始遍历所有节点(检查井+排水口)以获取平均超载时间(mm)......")
    for node in Nodes(sim):
        surcharge_duration = node.statistics['surcharge_duration']
        print(f"节点: {node.nodeid} 的平均超载时间为： {surcharge_duration} hr")
