"""
@File:swmm_nsga2.py
@Author:MJZJZ
@Version:1.0
@Date:2023/04/03
@Time:14:31
"""
import numpy as np

from pyswmm import Simulation, Nodes, Subcatchments, LidGroups
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter


# Pre_runoff = [28.84793721, 31.06321707, 11.96966298, 29.81131282, 22.76600575, 20.5654663,
#               32.03460237, 11.54445679, 11.39371698, 29.31124099, 26.40671222, 23.23278734,
#               29.09242243, 14.4631284, 13.2157434, 29.24380799, 26.48086273, 19.48246667,
#               29.14060795, 11.70136631, 12.75527874, 29.25169541, 26.61230667, 27.28638322,
#               26.29139334, 12.81874815, 13.18556032, 18.39743068, 26.2929191, 29.45805644,
#               29.632263, 24.50601238, 22.87947793, 26.18072453, 30.5640098, 28.75785111,
#               29.25407989, 28.78694888, 29.23303827, 30.4157768, 29.4229525, 29.88916333,
#               30.6586755, 29.72818431, 29.14815945, 32.80225754, 29.03260243, 15.24535308,
#               22.10563715, 28.67348727, 29.36437599, 31.8935914, 29.07932792, 23.60885133,
#               23.93630402, 29.05591441, 29.04791563]

# 用ElementwiseProblem自定义优化问题
class MyProblem(ElementwiseProblem):
    #  初始化
    def __init__(self):
        super().__init__(n_var=61,  # 自变量个数
                         n_obj=3,  # 优化目标函数个数
                         n_ieq_constr=4,  # 约束个数
                         xl=0.0,  # 自变量约束 这里上下限一样就直接用一个数来表示 否则可以用数组的形式
                         xu=300.0)

    #  重写问题 这里直接在_evaluate下写pyswmm的部分
    def _evaluate(self, x, out, *args, **kwargs):
        with Simulation(r'C:\Users\13618\Desktop\inp\P=1.inp') as sim:
            LidGroups(sim)['H00000'][0].unit_area = x[0]  # 设定inp文件里的LID面积
            LidGroups(sim)['H00000'][1].unit_area = x[1]  # 该文件里不同subcatchments（子汇水区）的LID项数不一样 手动添加所有项
            LidGroups(sim)['H00001'][0].unit_area = x[2]  # 对应inp文件的[LID_USAGE]
            LidGroups(sim)['H00001'][1].unit_area = x[3]
            LidGroups(sim)['H00002'][0].unit_area = x[4]
            LidGroups(sim)['H00004'][0].unit_area = x[5]
            LidGroups(sim)['H00005'][0].unit_area = x[6]
            LidGroups(sim)['H00006'][0].unit_area = x[7]
            LidGroups(sim)['H00007'][0].unit_area = x[8]
            LidGroups(sim)['H00008'][0].unit_area = x[9]
            LidGroups(sim)['H00009'][0].unit_area = x[10]
            LidGroups(sim)['H00009'][1].unit_area = x[11]
            LidGroups(sim)['H00010'][0].unit_area = x[12]
            LidGroups(sim)['H00011'][0].unit_area = x[13]
            LidGroups(sim)['H00012'][0].unit_area = x[14]
            LidGroups(sim)['H00013'][0].unit_area = x[15]
            LidGroups(sim)['H00014'][0].unit_area = x[16]
            LidGroups(sim)['H00015'][0].unit_area = x[17]
            LidGroups(sim)['H00015'][1].unit_area = x[18]
            LidGroups(sim)['H00016'][0].unit_area = x[19]
            LidGroups(sim)['H00017'][0].unit_area = x[20]
            LidGroups(sim)['H00018'][0].unit_area = x[21]
            LidGroups(sim)['H00019'][0].unit_area = x[22]
            LidGroups(sim)['H00020'][0].unit_area = x[23]
            LidGroups(sim)['H00021'][0].unit_area = x[24]
            LidGroups(sim)['H00021'][1].unit_area = x[25]
            LidGroups(sim)['H00022'][0].unit_area = x[26]
            LidGroups(sim)['H00023'][0].unit_area = x[27]
            LidGroups(sim)['H00024'][0].unit_area = x[28]
            LidGroups(sim)['H00025'][0].unit_area = x[29]
            LidGroups(sim)['H00026'][0].unit_area = x[30]
            LidGroups(sim)['H00027'][0].unit_area = x[31]
            LidGroups(sim)['H00029'][0].unit_area = x[32]
            LidGroups(sim)['H00029'][1].unit_area = x[33]
            LidGroups(sim)['H00031'][0].unit_area = x[34]
            LidGroups(sim)['H00032'][0].unit_area = x[35]
            LidGroups(sim)['H00032'][1].unit_area = x[36]
            LidGroups(sim)['H00034'][0].unit_area = x[37]
            LidGroups(sim)['H00035'][0].unit_area = x[38]
            LidGroups(sim)['H00036'][0].unit_area = x[39]
            LidGroups(sim)['H00036'][1].unit_area = x[40]
            LidGroups(sim)['H00037'][0].unit_area = x[41]
            LidGroups(sim)['H00038'][0].unit_area = x[42]
            LidGroups(sim)['H00038'][1].unit_area = x[43]
            LidGroups(sim)['H00039'][0].unit_area = x[44]
            LidGroups(sim)['H00041'][0].unit_area = x[45]
            LidGroups(sim)['H00044'][0].unit_area = x[46]
            LidGroups(sim)['H00046'][0].unit_area = x[47]
            LidGroups(sim)['H00047'][0].unit_area = x[48]
            LidGroups(sim)['H00047'][1].unit_area = x[49]
            LidGroups(sim)['H00048'][0].unit_area = x[50]
            LidGroups(sim)['H00048'][1].unit_area = x[51]
            LidGroups(sim)['H00049'][0].unit_area = x[52]
            LidGroups(sim)['H00051'][0].unit_area = x[53]
            LidGroups(sim)['H00052'][0].unit_area = x[54]
            LidGroups(sim)['H00053'][0].unit_area = x[55]
            LidGroups(sim)['H00053'][1].unit_area = x[56]
            LidGroups(sim)['H00054'][0].unit_area = x[57]
            LidGroups(sim)['H00054'][1].unit_area = x[58]
            LidGroups(sim)['H00055'][0].unit_area = x[59]
            LidGroups(sim)['H00056'][0].unit_area = x[60]
            # 开始仿真
            for step in enumerate(sim):
                pass  # 若需要每步的仿真都修改 则在这里添加代码
            # 本问题只需完整仿真完 直接pass即可
            # 仿真结束
            lid_area = np.array(np.zeros(61))  # 便于后续使用所有子汇水区LID面积 放在数组里
            lid_area[0] = LidGroups(sim)['H00000'][0].unit_area  # 仿真后提取各子汇水区LID面积
            lid_area[1] = LidGroups(sim)['H00000'][1].unit_area
            lid_area[2] = LidGroups(sim)['H00001'][0].unit_area
            lid_area[3] = LidGroups(sim)['H00001'][1].unit_area
            lid_area[4] = LidGroups(sim)['H00002'][0].unit_area
            lid_area[5] = LidGroups(sim)['H00004'][0].unit_area
            lid_area[6] = LidGroups(sim)['H00005'][0].unit_area
            lid_area[7] = LidGroups(sim)['H00006'][0].unit_area
            lid_area[8] = LidGroups(sim)['H00007'][0].unit_area
            lid_area[9] = LidGroups(sim)['H00008'][0].unit_area
            lid_area[10] = LidGroups(sim)['H00009'][0].unit_area
            lid_area[11] = LidGroups(sim)['H00009'][1].unit_area
            lid_area[12] = LidGroups(sim)['H00010'][0].unit_area
            lid_area[13] = LidGroups(sim)['H00011'][0].unit_area
            lid_area[14] = LidGroups(sim)['H00012'][0].unit_area
            lid_area[15] = LidGroups(sim)['H00013'][0].unit_area
            lid_area[16] = LidGroups(sim)['H00014'][0].unit_area
            lid_area[17] = LidGroups(sim)['H00015'][0].unit_area
            lid_area[18] = LidGroups(sim)['H00015'][1].unit_area
            lid_area[19] = LidGroups(sim)['H00016'][0].unit_area
            lid_area[20] = LidGroups(sim)['H00017'][0].unit_area
            lid_area[21] = LidGroups(sim)['H00018'][0].unit_area
            lid_area[22] = LidGroups(sim)['H00019'][0].unit_area
            lid_area[23] = LidGroups(sim)['H00020'][0].unit_area
            lid_area[24] = LidGroups(sim)['H00021'][0].unit_area
            lid_area[25] = LidGroups(sim)['H00021'][1].unit_area
            lid_area[26] = LidGroups(sim)['H00022'][0].unit_area
            lid_area[27] = LidGroups(sim)['H00023'][0].unit_area
            lid_area[28] = LidGroups(sim)['H00024'][0].unit_area
            lid_area[29] = LidGroups(sim)['H00025'][0].unit_area
            lid_area[30] = LidGroups(sim)['H00026'][0].unit_area
            lid_area[31] = LidGroups(sim)['H00027'][0].unit_area
            lid_area[32] = LidGroups(sim)['H00029'][0].unit_area
            lid_area[33] = LidGroups(sim)['H00029'][1].unit_area
            lid_area[34] = LidGroups(sim)['H00031'][0].unit_area
            lid_area[35] = LidGroups(sim)['H00032'][0].unit_area
            lid_area[36] = LidGroups(sim)['H00032'][1].unit_area
            lid_area[37] = LidGroups(sim)['H00034'][0].unit_area
            lid_area[38] = LidGroups(sim)['H00035'][0].unit_area
            lid_area[39] = LidGroups(sim)['H00036'][0].unit_area
            lid_area[40] = LidGroups(sim)['H00036'][1].unit_area
            lid_area[41] = LidGroups(sim)['H00037'][0].unit_area
            lid_area[42] = LidGroups(sim)['H00038'][0].unit_area
            lid_area[43] = LidGroups(sim)['H00038'][1].unit_area
            lid_area[44] = LidGroups(sim)['H00039'][0].unit_area
            lid_area[45] = LidGroups(sim)['H00041'][0].unit_area
            lid_area[46] = LidGroups(sim)['H00044'][0].unit_area
            lid_area[47] = LidGroups(sim)['H00046'][0].unit_area
            lid_area[48] = LidGroups(sim)['H00047'][0].unit_area
            lid_area[49] = LidGroups(sim)['H00047'][1].unit_area
            lid_area[50] = LidGroups(sim)['H00048'][0].unit_area
            lid_area[51] = LidGroups(sim)['H00048'][1].unit_area
            lid_area[52] = LidGroups(sim)['H00049'][0].unit_area
            lid_area[53] = LidGroups(sim)['H00051'][0].unit_area
            lid_area[54] = LidGroups(sim)['H00052'][0].unit_area
            lid_area[55] = LidGroups(sim)['H00053'][0].unit_area
            lid_area[56] = LidGroups(sim)['H00053'][1].unit_area
            lid_area[57] = LidGroups(sim)['H00054'][0].unit_area
            lid_area[58] = LidGroups(sim)['H00054'][1].unit_area
            lid_area[59] = LidGroups(sim)['H00055'][0].unit_area
            lid_area[60] = LidGroups(sim)['H00056'][0].unit_area
            # 下面是优化函数1的计算 需要各类型LID的面积分别求和
            a_lswd = lid_area[1] + lid_area[3] + lid_area[5] + lid_area[6] + lid_area[7] \
                     + lid_area[10] + lid_area[12] + lid_area[13] + lid_area[14] + lid_area[17] \
                     + lid_area[19] + lid_area[20] + lid_area[21] + lid_area[24] + lid_area[26] \
                     + lid_area[27] + lid_area[28] + lid_area[32] + lid_area[34] + lid_area[39] \
                     + lid_area[42] + lid_area[46] + lid_area[47] + lid_area[48] + lid_area[50] \
                     + lid_area[52] + lid_area[53] + lid_area[54] + lid_area[55] + lid_area[57] \
                     + lid_area[59] + lid_area[60]

            b_xcsld = lid_area[0] + lid_area[2] + lid_area[11] + lid_area[18] + lid_area[25] \
                      + lid_area[33] + lid_area[35] + lid_area[37] + lid_area[38] + lid_area[40] \
                      + lid_area[41] + lid_area[43] + lid_area[44] + lid_area[45]

            d_tslm = lid_area[4] + lid_area[8] + lid_area[9] + lid_area[15] + lid_area[16] \
                     + lid_area[22] + lid_area[23] + lid_area[29] + lid_area[30] + lid_area[31] \
                     + lid_area[36] + lid_area[49] + lid_area[51] + lid_area[56] + lid_area[58]

            # max R 径流量
            # 目前的径流量runoff只在subcatchment的statistic函数里保存 需要单独提取出来 单位不一致 需要单独换算
            # 详见https://github.com/OpenWaterAnalytics/pyswmm/discussions/416 开发团队已表示pyswmm2将会认真考虑该问题
            subcatchment_runoff = np.array(np.zeros(57))
            for i in range(10):
                subcatchment_runoff[i] = Subcatchments(sim)["H0000" + str(i)].statistics['runoff'] / Subcatchments(sim)[
                    "H0000" + str(i)].area / 10
            for i in range(10, 57):
                subcatchment_runoff[i] = Subcatchments(sim)["H000" + str(i)].statistics['runoff'] / Subcatchments(sim)[
                    "H000" + str(i)].area / 10
            R = 0
            # global Pre_runoff
            # for i in range(57):
            #     R = R + (subcatchment_runoff[i] - Pre_runoff[i]) / Pre_runoff[i]
            # Pre_runoff = subcatchment_runoff
            for i in range(57):
                R = R + subcatchment_runoff[i]
            R = R / 1640 - 1

            # min T 节点超载时间
            # 节点超载时间surcharge_duration同样在node的statistic函数里保存 这些都在官网的文档里有描述函数用法
            node_surcharged_duration = np.array(np.zeros(57))
            for i in range(1, 10):
                node_surcharged_duration[i - 1] = Nodes(sim)[str("J00" + str(i))].statistics['surcharge_duration']
            for i in range(10, 58):
                node_surcharged_duration[i - 1] = Nodes(sim)["J0" + str(i)].statistics['surcharge_duration']
            T = np.sum(node_surcharged_duration) / 30

            # 注意优化目标函数与约束都只能是min的形式 这里上面的R已经全部添加了负号进行计算
            f1 = 221.64 * a_lswd + 110.78 * b_xcsld + 303.13 * d_tslm
            f2 = R
            f3 = T
            # 约束 同样是min的形式
            g1 = a_lswd - 5500
            g2 = b_xcsld - 14600
            g3 = d_tslm - 3800
            g4 = R
            # 将优化目标函数与约束分别赋值给F、G
            out["F"] = [f1, f2, f3]
            out["G"] = [g1, g2, g3, g4]
            # 更新 养成好习惯 关闭仿真
    		sim.close()
			#如需单步内仿真多个inp，则需多次使用sim和sim.close()

# 照搬pymoo即可
problem = MyProblem()

algorithm = NSGA2(pop_size=100)  # 种群大小100

res = minimize(problem,
               algorithm,
               ("n_gen", 500),  # 迭代500代
               verbose=True,  # true则在终端显示每代部分参数
               # save_history=True,
               seed=1)  # 这里并未改动具体的变异率等，详细参数可以转到NSGA2的类型声明查看
# val = [e.opt.get("F")[0] for e in res.history]
# import matplotlib.pyplot as plt
# plt.plot(np.arange(len(val)), val)
# plt.show()
print(res.exec_time)  # 打印耗时
np.savetxt(r'C:\Users\13618\Desktop\design.txt', res.X)  # 保存最后pop_size大小的结果 分别是design spaces values 即自变量的值
np.savetxt(r'C:\Users\13618\Desktop\objective.txt', res.F)  # objective spaces values 即优化目标函数的值
np.savetxt(r'C:\Users\13618\Desktop\constraint.txt', res.G)  # constraint values 即约束的值
# 用三维散点图展示结果
plot = Scatter()
plot.add(res.F, edgecolor="red", facecolor="none")
plot.show()
