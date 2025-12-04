"""
Research Tool for Chatbot Agent

This module wraps the ReActAgent as a BaseTool for use by other agents,
providing deep research capabilities through a standardized tool interface.
"""

import json
import os
from typing import Union, Dict, Any
import logging

from qwen_agent.tools.base import BaseTool, register_tool
from inference.react_agent import ReActAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@register_tool('research', allow_overwrite=True)
class ResearchTool(BaseTool):
    """
    Research tool that wraps ReActAgent to provide comprehensive research capabilities.

    This tool allows agents to conduct deep, systematic research using the ReActAgent's
    advanced search, analysis, and synthesis capabilities.
    """

    name = 'research'
    description = 'Conduct comprehensive research on any topic using advanced search and analysis tools. Provide deep insights and well-structured answers with proper citations.'

    parameters = {
        "type": "object",
        "properties": {
            "research_quest": {
                "type": "string",
                "description": "The research question or topic to investigate. Be specific and clear about what you want to research.",
                "minLength": 5,
                "maxLength": 500
            }
        },
        "required": ["research_quest"]
    }

    def __init__(self):
        """Initialize the Research tool with ReActAgent."""
        super().__init__()

        # Initialize ReActAgent
        try:
            self.react_agent = ReActAgent()
            logger.info("ReActAgent initialized successfully for ResearchTool")
        except Exception as e:
            logger.error(f"Failed to initialize ReActAgent: {str(e)}")
            # Create a dummy agent for fallback
            self.react_agent = None

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Conduct comprehensive research using the ReActAgent.

        Args:
            params: Research parameters, can be string, dict, or JSON string
            **kwargs: Additional keyword arguments

        Returns:
            Comprehensive research answer as formatted string
        """
        try:
            # Check if ReActAgent is available
            if not self.react_agent:
                return "Error: ReActAgent is not available. Please check GLM_API_KEY configuration."

            # Parse parameters
            if isinstance(params, str):
                try:
                    params_dict = json.loads(params)
                    research_quest = params_dict.get('research_quest', '')
                except json.JSONDecodeError:
                    # If params is not valid JSON, treat it as the research quest directly
                    research_quest = params
            elif isinstance(params, dict):
                research_quest = params.get('research_quest', '')
            else:
                return "Error: Invalid parameters format. Expected string, dictionary, or JSON object."

            # Validate research quest
            if not research_quest or not str(research_quest).strip():
                return "Error: Research question cannot be empty. Please provide a specific topic or question to research."

            research_quest = str(research_quest).strip()

            # Log the research request
            logger.info(f"Starting research on: {research_quest}")

            # Conduct research using ReActAgent
            try:
                research_result = self.react_agent.research(research_quest)

                # Format the result
                formatted_result = self._format_research_result(research_quest, research_result)

                logger.info(f"Research completed for: {research_quest}")
                return formatted_result

            except Exception as e:
                logger.error(f"Error during ReActAgent research: {str(e)}")
                return f"Error during research execution: {str(e)}"

        except Exception as e:
            logger.error(f"Error in ResearchTool.call: {str(e)}")
            return f"Error processing research request: {str(e)}"

    def _format_research_result(self, question: str, result: str) -> str:
        """
        Format the research result into a readable and structured output.

        Args:
            question: The original research question
            result: The raw research result from ReActAgent

        Returns:
            Formatted research result
        """
        # Create a structured header
        header = f"📋 Research Report: {question}\n"
        separator = "=" * len(header.split('\n')[0]) + "\n\n"

        # Get research statistics if available
        stats = ""
        if hasattr(self.react_agent, 'llm_calls'):
            stats = f"📊 Research Statistics:\n"
            stats += f"• LLM Calls: {self.react_agent.llm_calls}\n"
            if hasattr(self.react_agent, 'messages'):
                stats += f"• Messages Exchanged: {len(self.react_agent.messages)}\n"
            stats += "\n"

        # Combine all parts
        formatted_result = header + separator + stats + result

        # Add footer
        footer = "\n\n" + "=" * 50 + "\n"
        footer += "🔍 Research completed using ReActAgent methodology"
        footer += "\n✅ Sources: Google Search, Google Scholar, Jina URL extraction, Python analysis"

        return formatted_result + footer

    def get_research_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the research agent's performance.

        Returns:
            Dictionary containing research statistics
        """
        if not self.react_agent:
            return {"error": "ReActAgent not initialized"}

        stats = {
            "llm_calls": getattr(self.react_agent, 'llm_calls', 0),
            "message_count": len(getattr(self.react_agent, 'messages', [])),
            "available_tools": list(getattr(self.react_agent, 'tools', {}).keys())
        }

        return stats

    def reset_research_agent(self):
        """Reset the ReActAgent for a fresh research session."""
        if self.react_agent and hasattr(self.react_agent, 'reset'):
            self.react_agent.reset()
            logger.info("ReActAgent has been reset for new research session")


# For direct testing
if __name__ == "__main__":
    # Create tool instance
    tool = ResearchTool()

    # Test research
    test_questions = [
        "What are the latest developments in quantum computing?",
        "How does climate change affect biodiversity?",
        "What are the benefits of renewable energy sources?"
    ]

    for question in test_questions:
        print(f"\n{'='*80}")
        print(f"Testing research for: {question}")
        print(f"{'='*80}")

        result = tool.call({"research_quest": question})
        print(result)
        print()

        # Show stats
        stats = tool.get_research_stats()
        print(f"🔢 Research Stats: {stats}")
        print()

        # Reset for next test
        tool.reset_research_agent()