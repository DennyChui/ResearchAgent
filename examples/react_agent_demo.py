#!/usr/bin/env python3
"""
ReAct Agent Usage Example

This script demonstrates how to use the ReAct Agent for research tasks.
"""

import sys
import os

# Add the current directory to the path to import inference modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inference.react_agent import ReActAgent


def example_research():
    """Example research session with the ReAct Agent."""
    print("🤖 ReAct Agent Research Example")
    print("=" * 60)
    
    # Initialize the agent
    agent = ReActAgent()
    
    # Research questions to try
    research_questions = [
        "What are the latest developments in quantum computing?",
        "How does machine learning impact healthcare?",
        "What are the best practices for sustainable software development?"
    ]
    
    print("Choose a research topic:")
    for i, question in enumerate(research_questions, 1):
        print(f"{i}. {question}")
    print("4. Enter your own question")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        question = research_questions[0]
    elif choice == "2":
        question = research_questions[1]
    elif choice == "3":
        question = research_questions[2]
    elif choice == "4":
        question = input("Enter your research question: ").strip()
    else:
        print("Invalid choice. Using default question.")
        question = research_questions[0]
    
    print(f"\n🔍 Researching: {question}")
    print("=" * 60)
    
    try:
        # Conduct research
        result = agent.research(question)
        
        print("\n📋 Research Results:")
        print("=" * 60)
        print(result)
        print("=" * 60)
        
        # Show statistics
        print(f"\n📊 Research Statistics:")
        print(f"   - LLM calls made: {agent.llm_calls}")
        print(f"   - Total messages: {len(agent.messages)}")
        
    except Exception as e:
        print(f"❌ Error during research: {e}")


def simple_test():
    """Simple test of the ReAct Agent."""
    print("🧪 Simple ReAct Agent Test")
    print("=" * 40)
    
    agent = ReActAgent()
    
    # Test with a simple question
    question = "What is Python programming?"
    print(f"Question: {question}")
    
    try:
        result = agent.research(question)
        print(f"Answer: {result[:200]}...")
        print(f"LLM calls: {agent.llm_calls}")
        print("✅ Test successful!")
    except Exception as e:
        print(f"❌ Test failed: {e}")


def interactive_research():
    """Interactive research mode."""
    print("🔬 Interactive Research Mode")
    print("=" * 50)
    print("Enter 'quit' to exit, 'help' for commands")
    
    agent = ReActAgent()
    
    while True:
        try:
            user_input = input("\n🔍 Research question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("Available commands:")
                print("  quit/exit/q - Exit the program")
                print("  help - Show this help")
                print("  stats - Show research statistics")
                print("  reset - Reset agent state")
                print("  Any other text - Research that topic")
                continue
            elif user_input.lower() == 'stats':
                print(f"📊 Current statistics:")
                print(f"   - LLM calls: {agent.llm_calls}")
                print(f"   - Messages: {len(agent.messages)}")
                continue
            elif user_input.lower() == 'reset':
                agent.reset()
                print("🔄 Agent state reset.")
                continue
            elif not user_input:
                print("❌ Please enter a research question.")
                continue
            
            # Conduct research
            print(f"\n🔍 Researching: {user_input}")
            print("=" * 50)
            
            result = agent.research(user_input)
            
            print("\n📋 Results:")
            print("=" * 50)
            print(result)
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function to choose the example mode."""
    print("🤖 ReAct Agent Examples")
    print("=" * 40)
    print("1. Example research session")
    print("2. Simple test")
    print("3. Interactive research")
    
    choice = input("\nChoose mode (1-3): ").strip()
    
    if choice == "1":
        example_research()
    elif choice == "2":
        simple_test()
    elif choice == "3":
        interactive_research()
    else:
        print("Invalid choice. Running simple test...")
        simple_test()


if __name__ == "__main__":
    main()
