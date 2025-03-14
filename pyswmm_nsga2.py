# -*- coding: utf-8 -*-
# @Time    : 2025/3/14 上午9:02
# @Author  : wm
# @Software   : PyCharm
import numpy as np
from pyswmm import Simulation, Nodes, Subcatchments, LidGroups
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pyswmm.swmm5 import PYSWMMException


# 用ElementwiseProblem自定义优化问题
class MyProblem(ElementwiseProblem):
    #  初始化
    def __init__(self, n_var, n_obj, n_ieq_constr, xl, xu):
        self.n_var = n_var
        self.n_obj = n_obj
        self.n_ieq_constr = n_ieq_constr
        self.xl = xl
        self.xu = xu
        super().__init__(n_var=self.n_var,  # 自变量个数（每个子汇水区中的一个LID设施算一个自变量）
                         n_obj=self.n_obj,  # 优化目标函数个数
                         n_ieq_constr=self.n_ieq_constr,  # 约束个数
                         xl=self.xl,  # 自变量约束 这里上下限一样就直接用一个数来表示 否则可以用数组的形式
                         xu=self.xu)

    #  重写问题 这里直接在_evaluate下写pyswmm的部分
    def _evaluate(self, x, out, *args, **kwargs):
        with Simulation('test.inp') as sim:
            success_counter = 0
            # 统计不同LID类型单元的数量
            # 如果还有其他类型的单元，需要新增相应的计数变量
            BC_counter = 0
            RG_counter = 0
            for lid_group in LidGroups(sim):
                try:
                    for lid_unit in lid_group:
                        lid_unit.unit_area = x[success_counter]
                        success_counter += 1
                        # 这里用代号判断当前LID单元属于哪个类型
                        # 如果还有其他类型的单元，需要新增相应的判断逻辑
                        if 'BC' in lid_unit.lid_control:
                            BC_counter += 1
                        elif 'RG' in lid_unit.lid_control:
                            RG_counter += 1
                except PYSWMMException as e:
                    if "Lid Unit Does Not Exist" in str(e):
                        continue
            # 开始仿真
            for step in enumerate(sim):
                pass  # 若需要每步的仿真都修改 则在这里添加代码
            # 本问题只需完整仿真完 直接pass即可
            # 仿真结束

            # 用数组保存每类LID设施的单元数量和
            # 如果还有其他类型的单元，需要新增相应的数组
            lid_area_BC = np.array(np.zeros(BC_counter))  # 所有LID类型为生物滞留网格的单元
            lid_area_RG = np.array(np.zeros(RG_counter))  # 所有LID类型为雨水花园的单元

            # 统计不同LID类型单元的数量
            # 如果还有其他类型的单元，需要新增相应的计数变量
            BC_counter = 0
            RG_counter = 0
            for lid_group in LidGroups(sim):
                try:
                    for lid_unit in lid_group:
                        # 这里用代号判断当前LID单元属于哪个类型
                        # 如果还有其他类型的单元，需要新增相应的判断逻辑
                        if 'BC' in lid_unit.lid_control:
                            lid_area_BC[BC_counter] = lid_unit.unit_area
                            BC_counter += 1
                        elif 'RG' in lid_unit.lid_control:
                            lid_area_RG[RG_counter] = lid_unit.unit_area
                            RG_counter += 1
                except PYSWMMException as e:
                    if "Lid Unit Does Not Exist" in str(e):
                        continue

            # 下面是目标函数的计算
            # 这里的目标函数仅用于测试，与原文相比有所改动
            # 下面是优化函数1的计算 需要各类型LID的面积分别求和
            a_BC = np.sum(lid_area_BC)
            b_RG = np.sum(lid_area_RG)

            # max R 径流量
            # 目前的径流量runoff只在subcatchment的statistic函数里保存 需要单独提取出来 单位不一致 需要单独换算
            # 详见https://github.com/OpenWaterAnalytics/pyswmm/discussions/416 开发团队已表示pyswmm2将会认真考虑该问题
            # 截至2025.3.14 最新版本pyswmm2.0.1仍然存在此问题

            # 从Subcatchments(sim)._nSubcatchments中获取子汇水区的数量，无需写死
            subcatchment_runoff = np.array(np.zeros(Subcatchments(sim)._nSubcatchments))
            for i, subcatchment in enumerate(Subcatchments(sim)):
                subcatchment_runoff[i] = subcatchment.statistics['runoff'] / subcatchment.area / 10


            # global Pre_runoff
            # for i in range(57):
            #     R = R + (subcatchment_runoff[i] - Pre_runoff[i]) / Pre_runoff[i]
            # Pre_runoff = subcatchment_runoff
            # for i in range(114):
            #     R = R + subcatchment_runoff[i]
            R = np.sum(subcatchment_runoff) / 1640 - 1

            # min T 节点超载时间
            # 节点超载时间surcharge_duration同样在node的statistic函数里保存 这些都在官网的文档里有描述函数用法
            # 从Nodes(sim)._nNodes中获取节点的数量，无需写死
            node_surcharged_duration = np.array(np.zeros(Nodes(sim)._nNodes))
            for i, node in enumerate(Nodes(sim)):
                node_surcharged_duration[i] = node.statistics['surcharge_duration']

            T = np.sum(node_surcharged_duration) / 30

            # 注意优化目标函数与约束都只能是min的形式 这里上面的R已经全部添加了负号进行计算
            f1 = 221.64 * a_BC + 110.78 * b_RG
            # 约束 同样是min的形式
            g1 = a_BC - 5500
            g2 = b_RG - 14600
            # 将优化目标函数与约束分别赋值给F、G
            out["F"] = [f1, R, T]
            out["G"] = [g1, g2, R]


"""
定义问题时需要依次填入: 
自变量个数（每个子汇水区中的一个LID设施算一个自变量）
优化目标函数个数
约束个数
自变量约束（这里上下限一样就直接用一个数来表示 否则可以用数组的形式）
具体可看下面一行的例子
"""
problem = MyProblem(4, 3, 3, 0, 300)

algorithm = NSGA2(pop_size=50)  # 种群大小50

res = minimize(problem,
               algorithm,
               ("n_gen", 200),  # 迭代200代
               verbose=True,  # true则在终端显示每代部分参数
               # save_history=True,
               seed=1)  # 这里并未改动具体的变异率等，详细参数可以转到NSGA2的类型声明查看
# val = [e.opt.get("F")[0] for e in res.history]
# import matplotlib.pyplot as plt
# plt.plot(np.arange(len(val)), val)
# plt.show()
print(res.exec_time)  # 打印耗时
np.savetxt('design.txt', res.X)  # 保存最后pop_size大小的结果 分别是design spaces values 即自变量的值
np.savetxt('objective.txt', res.F)  # objective spaces values 即优化目标函数的值
np.savetxt('constraint.txt', res.G)  # constraint values 即约束的值
# 用三维散点图展示结果
plot = Scatter()
plot.add(res.F, edgecolor="red", facecolor="none")
plot.show()
