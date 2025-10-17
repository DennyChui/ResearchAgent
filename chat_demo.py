#!/usr/bin/env python3
"""
Chatbot Demo Script

This script demonstrates the ChatAgent functionality with research capabilities.
Run this script to interact with the chatbot that can conduct research.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from inference.chat_agent import ChatAgent


def print_banner():
    """Print a welcome banner."""
    print("=" * 60)
    print("🤖 ResearchAgent Chatbot Demo")
    print("=" * 60)
    print("This chatbot can:")
    print("• Engage in natural conversation")
    print("• Conduct comprehensive research on various topics")
    print("• Ask clarifying questions to refine research requests")
    print("• Present research results in a user-friendly format")
    print("\nCommands:")
    print("• Type 'quit' to exit")
    print("• Type 'reset' to clear conversation history")
    print("• Type 'stats' to view conversation statistics")
    print("=" * 60)


def print_help():
    """Print help information."""
    print("\n📚 **Chatbot Help**")
    print("-" * 30)
    print("**For Research:**")
    print("• Be specific about what you want to research")
    print("• Include time frames if relevant (e.g., 'in 2024')")
    print("• Mention your purpose (academic, business, general knowledge)")
    print("\n**Example Research Queries:**")
    print('• "What are the latest developments in quantum computing?"')
    print('• "How does climate change affect biodiversity in tropical regions?"')
    print('• "Current applications of AI in healthcare for 2024"')
    print("\n**For Conversation:**")
    print("• Just ask questions or chat normally!")
    print("• The chatbot will detect when research is needed")
    print("-" * 30)


def main():
    """Main demo function."""
    print_banner()
    
    # Check environment
    if not os.getenv('GLM_API_KEY'):
        print("❌ Error: GLM_API_KEY environment variable is required")
        print("Please set the GLM_API_KEY environment variable and try again.")
        return
    
    try:
        # Initialize chat agent
        print("\n🔄 Initializing ChatAgent...")
        agent = ChatAgent()
        print("✅ ChatAgent initialized successfully!")
        
        print_help()
        
        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                # Handle commands
                if user_input.lower() == 'quit':
                    print("\n👋 Goodbye! Thanks for using ResearchAgent Chatbot!")
                    break
                elif user_input.lower() == 'reset':
                    agent.reset_conversation()
                    print("\n🔄 Conversation history cleared!")
                    continue
                elif user_input.lower() == 'stats':
                    stats = agent.get_stats()
                    print("\n📊 **Conversation Statistics**")
                    print(f"• Messages exchanged: {stats['conversation_length']}")
                    print(f"• Research mode: {'Active' if stats['is_research_mode'] else 'Inactive'}")
                    if stats.get('research_stats') and isinstance(stats['research_stats'], dict):
                        print(f"• LLM calls for research: {stats['research_stats'].get('llm_calls', 0)}")
                    continue
                elif user_input.lower() == 'help':
                    print_help()
                    continue
                elif not user_input:
                    continue
                
                print("\n🤖 Assistant: ", end="", flush=True)
                
                # Get agent response
                response = agent.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using ResearchAgent Chatbot!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'quit' to exit.")
    
    except Exception as e:
        print(f"❌ Failed to initialize ChatAgent: {str(e)}")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
