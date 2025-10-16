#!/usr/bin/env python3
"""
ReAct Agent + Python Sandbox Tool Demo

This script demonstrates how the ReAct Agent utilizes the Python sandbox tool for research tasks
involving calculations and data analysis.
"""

import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Add project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def demo_mathematical_research():
    """Demonstrate mathematical calculation research task"""
    print("=" * 70)
    print("Demo 1: Mathematical Research - Analysis of the Golden Ratio")
    print("=" * 70)
    
    try:
        from inference.react_agent import ReActAgent
        
        if not os.getenv('GLM_API_KEY'):
            print("⚠️ Need to set GLM_API_KEY environment variable to run the full demo")
            print("Demonstrating manual usage of Python sandbox tool:")
            
            # Manual demonstration of Python sandbox tool usage
            from inference import PythonSandboxTool
            tool = PythonSandboxTool()
            
            # Golden ratio calculation
            golden_ratio_code = """
import math

# Calculate golden ratio
phi = (1 + math.sqrt(5)) / 2
print(f"Golden ratio φ = {phi}")

# Verify property: φ² = φ + 1
phi_squared = phi ** 2
print(f"φ² = {phi_squared}")
print(f"φ + 1 = {phi + 1}")
print(f"φ² ≈ φ + 1: {abs(phi_squared - (phi + 1)) < 1e-10}")

# Golden ratio in Fibonacci sequence
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fib_20 = fibonacci(20)
fib_19 = fibonacci(19)
ratio = fib_20 / fib_19
print(f"20th/19th term = {ratio}")
print(f"Difference from golden ratio: {abs(ratio - phi):.6f}")
"""
            
            print("\n🔧 Executing golden ratio calculation:")
            result = tool.call({"code": golden_ratio_code})
            print(result)
            
            return True
        
        # If API key is available, use ReAct Agent
        agent = ReActAgent()
        
        question = """
        Please research the mathematical properties of the golden ratio φ, including:
        1. The exact value of φ
        2. Verification of the property φ² = φ + 1
        3. Manifestation in the Fibonacci sequence
        4. Examples in nature
        
        Please use the python_sandbox tool for relevant mathematical calculations to verify your analysis.
        """
        
        print(f"🔍 Research question: {question.strip()}")
        print("\n⚠️ Note: This will call the actual LLM API")
        user_input = input("Continue? (y/N): ").strip().lower()
        
        if user_input == 'y':
            answer = agent.research(question)
            print("\n📋 Research results:")
            print("=" * 50)
            print(answer)
        else:
            print("✅ Demo cancelled")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def demo_data_analysis():
    """Demonstrate data analysis research task"""
    print("\n" + "=" * 70)
    print("Demo 2: Data Analysis Research - Population Growth Trend Analysis")
    print("=" * 70)
    
    try:
        from inference import PythonSandboxTool
        
        tool = PythonSandboxTool()
        
        # Simulated population data analysis
        data_analysis_code = """
import matplotlib.pyplot as plt
import numpy as np

# Simulated data: population of a city over years (in 10,000s)
years = list(range(2010, 2024))
population = [850, 865, 880, 895, 910, 925, 940, 955, 970, 985, 1000, 1015, 1030, 1045]

print("Population data by year:")
for year, pop in zip(years, population):
    print(f"{year}: {pop} ×10,000")

# Calculate growth rates
growth_rates = []
for i in range(1, len(population)):
    rate = (population[i] - population[i-1]) / population[i-1] * 100
    growth_rates.append(rate)

print("\\nAnnual growth rates:")
for year, rate in zip(years[1:], growth_rates):
    print(f"{year}: {rate:.2f}%")

# Calculate average growth rate
avg_growth = np.mean(growth_rates)
print(f"\\nAverage annual growth rate: {avg_growth:.2f}%")

# Predict population for next 5 years
last_pop = population[-1]
print("\\nPopulation prediction for next 5 years:")
for i in range(1, 6):
    predicted_pop = last_pop * ((1 + avg_growth/100) ** i)
    print(f"{2024 + i}: {predicted_pop:.1f} ×10,000")

# Calculate population doubling time
if avg_growth > 0:
    doubling_time = 70 / avg_growth  # Rule of 70
    print(f"\\nAt current growth rate, population doubling time: {doubling_time:.1f} years")
"""
        
        print("🔧 Executing population data analysis:")
        print("Note: matplotlib may not be available, but calculation part will still execute")
        
        # Simplified version without matplotlib dependency
        simple_analysis_code = """
import numpy as np

# Simulated data: population of a city over years (in 10,000s)
years = list(range(2010, 2024))
population = [850, 865, 880, 895, 910, 925, 940, 955, 970, 985, 1000, 1015, 1030, 1045]

print("Population data by year:")
for year, pop in zip(years, population):
    print(f"{year}: {pop} ×10,000")

# Calculate growth rates
growth_rates = []
for i in range(1, len(population)):
    rate = (population[i] - population[i-1]) / population[i-1] * 100
    growth_rates.append(rate)

print("\\nAnnual growth rates:")
for year, rate in zip(years[1:], growth_rates):
    print(f"{year}: {rate:.2f}%")

# Calculate average growth rate
avg_growth = sum(growth_rates) / len(growth_rates)
print(f"\\nAverage annual growth rate: {avg_growth:.2f}%")

# Predict population for next 5 years
last_pop = population[-1]
print("\\nPopulation prediction for next 5 years:")
for i in range(1, 6):
    predicted_pop = last_pop * ((1 + avg_growth/100) ** i)
    print(f"{2024 + i}: {predicted_pop:.1f} ×10,000")

# Calculate population doubling time
if avg_growth > 0:
    doubling_time = 70 / avg_growth  # Rule of 70
    print(f"\\nAt current growth rate, population doubling time: {doubling_time:.1f} years")
"""
        
        result = tool.call({"code": simple_analysis_code})
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ Data analysis demo failed: {e}")
        return False

def demo_scientific_computation():
    """Demonstrate scientific computation research task"""
    print("\n" + "=" * 70)
    print("Demo 3: Scientific Computation - Projectile Motion Analysis")
    print("=" * 70)
    
    try:
        from inference import PythonSandboxTool
        
        tool = PythonSandboxTool()
        
        # Projectile motion calculation
        physics_code = """
import math

# Physical constants
g = 9.8  # Acceleration due to gravity (m/s²)

def projectile_motion(v0, angle, h0=0):
    \"\"\"
    Calculate projectile motion parameters
    v0: Initial velocity (m/s)
    angle: Launch angle (degrees)
    h0: Initial height (m)
    \"\"\"
    angle_rad = math.radians(angle)
    
    # Horizontal and vertical velocity components
    vx = v0 * math.cos(angle_rad)
    vy = v0 * math.sin(angle_rad)
    
    # Flight time
    # Solve quadratic equation: -0.5*g*t² + vy*t + h0 = 0
    discriminant = vy**2 + 2*g*h0
    if discriminant < 0:
        return None
    
    t_flight = (vy + math.sqrt(discriminant)) / g
    
    # Maximum height
    h_max = h0 + (vy**2) / (2*g)
    
    # Range
    range_x = vx * t_flight
    
    return {
        'flight_time': t_flight,
        'max_height': h_max,
        'range': range_x,
        'impact_velocity': math.sqrt(vx**2 + (vy - g*t_flight)**2)
    }

# Test different launch angles
v0 = 30  # Initial velocity 30 m/s
angles = [15, 30, 45, 60, 75]

print(f"Initial velocity: {v0} m/s")
print("Projectile motion parameters for different launch angles:")
print("-" * 60)

for angle in angles:
    result = projectile_motion(v0, angle)
    if result:
        print(f"Angle {angle}°:")
        print(f"  Flight time: {result['flight_time']:.2f} s")
        print(f"  Maximum height: {result['max_height']:.2f} m")
        print(f"  Range: {result['range']:.2f} m")
        print(f"  Impact velocity: {result['impact_velocity']:.2f} m/s")
        print()

# Find optimal angle (maximum range)
best_angle = 0
max_range = 0

for angle in range(1, 90):
    result = projectile_motion(v0, angle)
    if result and result['range'] > max_range:
        max_range = result['range']
        best_angle = angle

print(f"Optimal launch angle: {best_angle}° (theoretical value: 45°)")
print(f"Maximum range: {max_range:.2f} m")

# Theoretical maximum range (45° angle)
theoretical_max = v0**2 / g
print(f"Theoretical maximum range: {theoretical_max:.2f} m")
print(f"Error: {abs(max_range - theoretical_max):.2f} m")
"""
        
        print("🔧 Executing projectile motion analysis:")
        result = tool.call({"code": physics_code})
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ Scientific computation demo failed: {e}")
        return False

def main():
    """Main demonstration function"""
    print("🚀 ReAct Agent + Python Sandbox Tool Integration Demo")
    print("This demo shows how to use Python code execution capabilities in research tasks")
    
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
            print("\n⚠️ Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ Demo {i} encountered an error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("Demo Summary")
    print("=" * 70)
    
    if results:
        passed = sum(results)
        total = len(results)
        print(f"Completed demos: {passed}/{total}")
        
        if passed == total:
            print("🎉 All demos completed successfully!")
            print("\n✨ ReAct Agent now has powerful calculation and data analysis capabilities:")
            print("   • Mathematical calculations and verification")
            print("   • Data analysis and statistics")
            print("   • Scientific computation and modeling")
            print("   • Algorithm implementation and testing")
        else:
            print("⚠️ Some demos failed, but basic functionality is working")
    
    print("\n💡 To use in actual research, please set the GLM_API_KEY environment variable")
    print("   Then run: agent = ReActAgent(); answer = agent.research('your research question')")

if __name__ == "__main__":
    main()
