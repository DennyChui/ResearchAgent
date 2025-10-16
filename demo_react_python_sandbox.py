#!/usr/bin/env python3
"""
ReAct Agent + Python Sandbox工具演示

这个脚本演示ReAct Agent如何利用Python sandbox工具进行包含计算和数据分析的研究任务。
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def demo_mathematical_research():
    """演示数学计算研究任务"""
    print("=" * 70)
    print("演示1: 数学计算研究 - 黄金分割比例的分析")
    print("=" * 70)
    
    try:
        from inference.react_agent import ReActAgent
        
        if not os.getenv('GLM_API_KEY'):
            print("⚠️ 需要设置GLM_API_KEY环境变量来运行完整演示")
            print("演示如何手动使用Python sandbox工具:")
            
            # 手动演示Python sandbox工具的使用
            from inference import PythonSandboxTool
            tool = PythonSandboxTool()
            
            # 黄金分割比例计算
            golden_ratio_code = """
import math

# 计算黄金分割比例
phi = (1 + math.sqrt(5)) / 2
print(f"黄金分割比例 φ = {phi}")

# 验证性质: φ² = φ + 1
phi_squared = phi ** 2
print(f"φ² = {phi_squared}")
print(f"φ + 1 = {phi + 1}")
print(f"φ² ≈ φ + 1: {abs(phi_squared - (phi + 1)) < 1e-10}")

# 斐波那契数列中的黄金比例
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fib_20 = fibonacci(20)
fib_19 = fibonacci(19)
ratio = fib_20 / fib_19
print(f"第20项/第19项 = {ratio}")
print(f"与黄金比例的差异: {abs(ratio - phi):.6f}")
"""
            
            print("\n🔧 执行黄金分割比例计算:")
            result = tool.call({"code": golden_ratio_code})
            print(result)
            
            return True
        
        # 如果有API密钥，使用ReAct Agent
        agent = ReActAgent()
        
        question = """
        请研究黄金分割比例φ的数学性质，包括：
        1. φ的精确数值
        2. 验证φ² = φ + 1的性质
        3. 在斐波那契数列中的体现
        4. 与自然界中的实例
        
        请使用python_sandbox工具进行相关的数学计算来验证你的分析。
        """
        
        print(f"🔍 研究问题: {question.strip()}")
        print("\n⚠️ 注意：这将调用真实的LLM API")
        user_input = input("是否继续？(y/N): ").strip().lower()
        
        if user_input == 'y':
            answer = agent.research(question)
            print("\n📋 研究结果:")
            print("=" * 50)
            print(answer)
        else:
            print("✅ 演示已取消")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def demo_data_analysis():
    """演示数据分析研究任务"""
    print("\n" + "=" * 70)
    print("演示2: 数据分析研究 - 人口增长趋势分析")
    print("=" * 70)
    
    try:
        from inference import PythonSandboxTool
        
        tool = PythonSandboxTool()
        
        # 模拟人口数据分析
        data_analysis_code = """
import matplotlib.pyplot as plt
import numpy as np

# 模拟数据：某城市历年人口（万人）
years = list(range(2010, 2024))
population = [850, 865, 880, 895, 910, 925, 940, 955, 970, 985, 1000, 1015, 1030, 1045]

print("历年人口数据:")
for year, pop in zip(years, population):
    print(f"{year}: {pop}万人")

# 计算增长率
growth_rates = []
for i in range(1, len(population)):
    rate = (population[i] - population[i-1]) / population[i-1] * 100
    growth_rates.append(rate)

print("\\n年增长率:")
for year, rate in zip(years[1:], growth_rates):
    print(f"{year}: {rate:.2f}%")

# 计算平均增长率
avg_growth = np.mean(growth_rates)
print(f"\\n平均年增长率: {avg_growth:.2f}%")

# 预测未来5年人口
last_pop = population[-1]
print("\\n未来5年人口预测:")
for i in range(1, 6):
    predicted_pop = last_pop * ((1 + avg_growth/100) ** i)
    print(f"{2024 + i}: {predicted_pop:.1f}万人")

# 计算人口翻倍时间
if avg_growth > 0:
    doubling_time = 70 / avg_growth  # 70法则
    print(f"\\n按当前增长率，人口翻倍时间约需: {doubling_time:.1f}年")
"""
        
        print("🔧 执行人口数据分析:")
        print("注意：matplotlib可能不可用，但计算部分仍会执行")
        
        # 简化版本，不依赖matplotlib
        simple_analysis_code = """
import numpy as np

# 模拟数据：某城市历年人口（万人）
years = list(range(2010, 2024))
population = [850, 865, 880, 895, 910, 925, 940, 955, 970, 985, 1000, 1015, 1030, 1045]

print("历年人口数据:")
for year, pop in zip(years, population):
    print(f"{year}: {pop}万人")

# 计算增长率
growth_rates = []
for i in range(1, len(population)):
    rate = (population[i] - population[i-1]) / population[i-1] * 100
    growth_rates.append(rate)

print("\\n年增长率:")
for year, rate in zip(years[1:], growth_rates):
    print(f"{year}: {rate:.2f}%")

# 计算平均增长率
avg_growth = sum(growth_rates) / len(growth_rates)
print(f"\\n平均年增长率: {avg_growth:.2f}%")

# 预测未来5年人口
last_pop = population[-1]
print("\\n未来5年人口预测:")
for i in range(1, 6):
    predicted_pop = last_pop * ((1 + avg_growth/100) ** i)
    print(f"{2024 + i}: {predicted_pop:.1f}万人")

# 计算人口翻倍时间
if avg_growth > 0:
    doubling_time = 70 / avg_growth  # 70法则
    print(f"\\n按当前增长率，人口翻倍时间约需: {doubling_time:.1f}年")
"""
        
        result = tool.call({"code": simple_analysis_code})
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ 数据分析演示失败: {e}")
        return False

def demo_scientific_computation():
    """演示科学计算研究任务"""
    print("\n" + "=" * 70)
    print("演示3: 科学计算 - 抛体运动分析")
    print("=" * 70)
    
    try:
        from inference import PythonSandboxTool
        
        tool = PythonSandboxTool()
        
        # 抛体运动计算
        physics_code = """
import math

# 物理常数
g = 9.8  # 重力加速度 (m/s²)

def projectile_motion(v0, angle, h0=0):
    \"\"\"
    计算抛体运动参数
    v0: 初速度 (m/s)
    angle: 发射角度 (度)
    h0: 初始高度 (m)
    \"\"\"
    angle_rad = math.radians(angle)
    
    # 水平和垂直速度分量
    vx = v0 * math.cos(angle_rad)
    vy = v0 * math.sin(angle_rad)
    
    # 飞行时间
    # 使用二次方程求解: -0.5*g*t² + vy*t + h0 = 0
    discriminant = vy**2 + 2*g*h0
    if discriminant < 0:
        return None
    
    t_flight = (vy + math.sqrt(discriminant)) / g
    
    # 最大高度
    h_max = h0 + (vy**2) / (2*g)
    
    # 射程
    range_x = vx * t_flight
    
    return {
        'flight_time': t_flight,
        'max_height': h_max,
        'range': range_x,
        'impact_velocity': math.sqrt(vx**2 + (vy - g*t_flight)**2)
    }

# 测试不同的发射角度
v0 = 30  # 初速度 30 m/s
angles = [15, 30, 45, 60, 75]

print(f"初速度: {v0} m/s")
print("不同发射角度的抛体运动参数:")
print("-" * 60)

for angle in angles:
    result = projectile_motion(v0, angle)
    if result:
        print(f"角度 {angle}°:")
        print(f"  飞行时间: {result['flight_time']:.2f} s")
        print(f"  最大高度: {result['max_height']:.2f} m")
        print(f"  射程: {result['range']:.2f} m")
        print(f"  落地速度: {result['impact_velocity']:.2f} m/s")
        print()

# 找出最佳角度（最大射程）
best_angle = 0
max_range = 0

for angle in range(1, 90):
    result = projectile_motion(v0, angle)
    if result and result['range'] > max_range:
        max_range = result['range']
        best_angle = angle

print(f"最佳发射角度: {best_angle}° (理论值: 45°)")
print(f"最大射程: {max_range:.2f} m")

# 理论最大射程 (45°角)
theoretical_max = v0**2 / g
print(f"理论最大射程: {theoretical_max:.2f} m")
print(f"误差: {abs(max_range - theoretical_max):.2f} m")
"""
        
        print("🔧 执行抛体运动分析:")
        result = tool.call({"code": physics_code})
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ 科学计算演示失败: {e}")
        return False

def main():
    """主演示函数"""
    print("🚀 ReAct Agent + Python Sandbox工具集成演示")
    print("本演示展示如何在研究任务中使用Python代码执行能力")
    
    demos = [
        demo_mathematical_research,
        demo_data_analysis,
        demo_scientific_computation,
    ]
    
    results = []
    
    for i, demo_func in enumerate(demos, 1):
        try:
            success = demo_func()
            results.append(success)
        except KeyboardInterrupt:
            print("\n⚠️ 演示被用户中断")
            break
        except Exception as e:
            print(f"❌ 演示 {i} 发生错误: {e}")
            results.append(False)
    
    # 总结
    print("\n" + "=" * 70)
    print("演示总结")
    print("=" * 70)
    
    if results:
        passed = sum(results)
        total = len(results)
        print(f"完成演示: {passed}/{total}")
        
        if passed == total:
            print("🎉 所有演示都成功完成！")
            print("\n✨ ReAct Agent现在具备了强大的计算和数据分析能力:")
            print("   • 数学计算和验证")
            print("   • 数据分析和统计")
            print("   • 科学计算和建模")
            print("   • 算法实现和测试")
        else:
            print("⚠️ 部分演示失败，但基本功能正常")
    
    print("\n💡 要在实际研究中使用，请设置GLM_API_KEY环境变量")
    print("   然后运行: agent = ReActAgent(); answer = agent.research('你的研究问题')")

if __name__ == "__main__":
    main()
