# -*- coding: utf-8 -*-
# @Time    : 2025/3/14 上午9:29
# @Author  : wm
# @Software   : PyCharm
from pyswmm import Simulation, Nodes, Subcatchments, LidGroups
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

    success_counter = 0
    for lid_group in LidGroups(sim):
        print(lid_group)
        print(type(lid_group))
        print('---------------------------------------------------')
        try:
            print(lid_group[0].unit_area)
            print('---------------------------------------------------')

            # 这里可以将lid_group[0].unit_area赋给x[success_counter]

            success_counter += 1  # 这个变量代表x的索引
        except PYSWMMException as e:
            if "Lid Unit Does Not Exist" in str(e):
                continue
            else:
                print(f"出现了其他异常: {str(e)}")

    print(f"成功访问unit_area的次数: {success_counter}")