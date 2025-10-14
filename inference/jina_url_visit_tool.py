"""
Jina URL Visit Tool for Qwen-Agent

This module implements a web content extraction and summarization tool
using Jina API to fetch readable content and LLM to generate summaries.
"""

import json
import urllib.parse
import http.client
import os
import re
from typing import Union, Dict, Any, List
import logging

from qwen_agent.tools.base import BaseTool, register_tool

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@register_tool('visit')
class JinaURLVisitTool(BaseTool):
    """
    Jina URL Visit tool for extracting and summarizing web content.

    This tool allows Qwen-Agent to visit URLs using Jina API to get
    structured content and then generate intelligent summaries using LLM.
    """

    name = 'visit'
    description = 'Visit web pages using Jina API to extract structured content and generate intelligent summaries based on a specific goal.'

    parameters = {
        "type": "object",
        "properties": {
            "url": {
                "type": ["string", "array"],
                "description": "URL(s) to visit and extract content from - can be single URL or array of URLs",
                "minItems": 1,
                "maxItems": 5,
                "items": {
                    "type": "string",
                    "format": "uri"
                }
            },
            "goal": {
                "type": "string",
                "description": "The goal or objective for summarizing the web page content",
                "minLength": 5,
                "maxLength": 200
            }
        },
        "required": ["url", "goal"]
    }

    def __init__(self):
        """Initialize the Jina URL Visit tool."""
        super().__init__()
        self.jina_api_key = os.getenv('JINA_API_KEY', 'jina_0b07d5982d6f4ee287de16cc4b32981fTBZpS-i7feuvLyPdauhoeeIjX0XZ')
        self.jina_api_host = 'r.jina.ai'
        self.max_tokens = 8000

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Visit URL(s) and generate content summaries.

        Args:
            params: Tool parameters, can be string or dict
            **kwargs: Additional keyword arguments

        Returns:
            Formatted summaries as string
        """
        try:
            # Parse parameters
            if isinstance(params, str):
                try:
                    params_dict = json.loads(params)
                    url = params_dict.get('url', '')
                    goal = params_dict.get('goal', '')
                except json.JSONDecodeError:
                    return "Error: Invalid JSON parameters format."
            elif isinstance(params, dict):
                url = params.get('url', '')
                goal = params.get('goal', '')
            else:
                return "Error: Invalid parameters format. Expected string or dictionary."

            if not url or not goal:
                return "Error: Both 'url' and 'goal' parameters are required."

            if not goal.strip():
                return "Error: Goal cannot be empty."

            # Handle single URL or array of URLs
            if isinstance(url, str):
                urls = [url.strip()]
            elif isinstance(url, list):
                urls = [str(u).strip() for u in url if str(u).strip()]
            else:
                return "Error: URL must be a string or array of strings."

            if not urls:
                return "Error: No valid URLs provided."

            # Validate URLs
            valid_urls = []
            for u in urls:
                if self._validate_url(u):
                    valid_urls.append(u)
                else:
                    logger.warning(f"Invalid URL skipped: {u}")

            if not valid_urls:
                return "Error: No valid URLs provided."

            # Process each URL
            results = []
            for i, single_url in enumerate(valid_urls):
                if len(valid_urls) > 1:
                    results.append(f"\n## URL {i+1}: {single_url}\n")

                try:
                    # Fetch content using Jina
                    jina_content = self._fetch_jina_content(single_url)

                    # Generate summary using LLM
                    summary = self._summarize_content(jina_content, goal.strip())

                    # Format result
                    formatted_result = self._format_single_result(single_url, goal, summary)
                    results.append(formatted_result)

                except Exception as e:
                    error_result = f"Error processing URL {single_url}: {str(e)}"
                    results.append(error_result)
                    logger.error(error_result)

            # Return combined results
            if len(valid_urls) > 1:
                header = f"\n## Batch URL Summary Report\n\n**Goal:** {goal}\n\n"
                footer = f"\n---\n**Summary:** Processed {len(valid_urls)} URLs"
                return header + "\n".join(results) + footer
            else:
                return "\n".join(results)

        except Exception as e:
            logger.error(f"Error in Jina URL visit: {str(e)}")
            return f"Error performing URL visit: {str(e)}"

    def _validate_url(self, url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if valid, False otherwise
        """
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return url_pattern.match(url) is not None

    def _fetch_jina_content(self, url: str, retries: int = 5) -> str:
        """
        Fetch web content using Jina API.

        Args:
            url: URL to fetch
            retries: Number of retry attempts

        Returns:
            Extracted content as string
        """
        for attempt in range(retries):
            try:
                # Prepare the Jina API URL
                encoded_url = urllib.parse.quote(url, safe='')
                jina_url = f"https://{self.jina_api_host}/{encoded_url}"

                # Parse the URL to get host and path
                parsed = urllib.parse.urlparse(jina_url)
                host = parsed.netloc
                path = parsed.path or '/'

                # Create HTTPS connection with timeout
                conn = http.client.HTTPSConnection(host, timeout=10)

                # Prepare request headers
                headers = {
                    'Authorization': f'Bearer {self.jina_api_key}',
                    'User-Agent': 'Qwen-Agent-Jina-URL-Visit-Tool/1.0',
                    'Accept': 'text/plain',
                    'Accept-Language': 'en-US,en;q=0.9'
                }

                # Make the request
                conn.request('GET', path, headers=headers)

                # Get response
                response = conn.getresponse()
                response_data = response.read().decode('utf-8')

                # Close connection
                conn.close()

                # Check response status
                if response.status == 200:
                    content = response_data.strip()
                    if content:
                        return content
                    else:
                        return "Error: No content extracted from the URL."
                else:
                    logger.warning(f"Jina API returned status {response.status}: {response_data[:200]}")
                    if attempt < retries - 1:
                        continue
                    return f"Error: Jina API request failed with status {response.status}."

            except Exception as e:
                logger.warning(f"Jina API attempt {attempt + 1} failed: {str(e)}")
                if attempt < retries - 1:
                    continue
                return f"Error: Failed to fetch content after {retries} attempts: {str(e)}"

        return "Error: All fetch attempts failed."

    def _summarize_content(self, jina_content: str, goal: str) -> str:
        """
        Generate content summary using LLM with structured output.

        Args:
            jina_content: Raw content from Jina API
            goal: User's goal for summarization

        Returns:
            Generated structured summary as JSON string
        """
        try:
            # Build the user message with template and JSON output format
            user_content = f"""## **Task Guidelines**
1. **Content Scanning for Rational**: Locate the **specific sections/data** directly related to the user's goal within the webpage content
2. **Key Extraction for Evidence**: Identify and extract the **most relevant information** from the content, you never miss any important information, output the **full original context** of the content as far as possible, it can be more than three paragraphs.
3. **Summary Output for Summary**: Organize into a concise paragraph with logical flow, prioritizing clarity and judge the contribution of the information to the goal.

**Web Content:**
{jina_content}

**Goal:** {goal}

**Final Output Format using JSON format has "rational", "evidence", "summary" fields**

Please analyze the content and return a JSON object with the following structure:
{{
  "rational": "Explain which specific sections of the content are most relevant to the goal and why",
  "evidence": "Extract the complete relevant information from the content, including full context, quotes, and data. This should be comprehensive and can span multiple paragraphs",
  "summary": "Provide a concise summary that directly addresses the goal, prioritizing clarity and logical flow"
}}"""

            # Build messages list (single user message as specified)
            messages = [
                {"role": "user", "content": user_content}
            ]

            # Apply truncation after building the message
            truncated_messages = self._truncate_messages(messages, self.max_tokens)

            # Call LLM
            structured_summary = self._call_llm(truncated_messages)
            return structured_summary

        except Exception as e:
            logger.error(f"Error in content summarization: {str(e)}")
            # Return error in structured format
            error_response = {
                "rational": f"Error occurred during content analysis",
                "evidence": f"Unable to extract evidence due to: {str(e)}",
                "summary": f"Failed to generate summary: {str(e)}"
            }
            return json.dumps(error_response, ensure_ascii=False, indent=2)

    def _truncate_messages(self, messages: list, max_tokens: int) -> list:
        """
        Truncate message content to fit within token limits.

        Args:
            messages: List of messages to truncate
            max_tokens: Maximum allowed tokens

        Returns:
            Truncated messages list
        """
        truncated_messages = []

        for message in messages:
            original_content = message["content"]
            estimated_tokens = self._estimate_tokens(original_content)

            if estimated_tokens <= max_tokens * 0.7:
                # No truncation needed
                truncated_messages.append(message)
            else:
                # Apply smart truncation
                target_chars = int(max_tokens * 0.7 * 4)  # Approximate 1 token = 4 chars
                truncated_content = self._smart_truncate(original_content, target_chars)

                truncated_messages.append({
                    "role": message["role"],
                    "content": truncated_content + "\n\n[Note: Content was truncated for processing]"
                })

        return truncated_messages

    def _smart_truncate(self, content: str, max_chars: int) -> str:
        """
        Smartly truncate content while preserving readability.

        Args:
            content: Content to truncate
            max_chars: Maximum characters

        Returns:
            Truncated content
        """
        if len(content) <= max_chars:
            return content

        # Try to truncate at natural breakpoints
        truncated = content[:max_chars]

        # Look for the last sentence ending or paragraph break
        breakpoints = ['。\n', '！\n', '？\n', '.\n', '!\n', '?\n', '。\n', '！\n', '？\n',
                      '。\n', '。', '！', '？', '.', '!', '?', '\n\n', '\n']

        best_pos = -1
        for breakpoint in breakpoints:
            pos = truncated.rfind(breakpoint)
            if pos > best_pos and pos > max_chars * 0.6:  # Don't truncate too much
                best_pos = pos + len(breakpoint)

        if best_pos > 0:
            return truncated[:best_pos]
        else:
            # Fallback to hard truncation with ellipsis
            return truncated[:max_chars-3] + "..."

    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Args:
            text: Text to estimate tokens for

        Returns:
            Estimated token count
        """
        # Simple estimation: 1 token ≈ 4 characters for Chinese/English mixed content
        return len(text) // 4 + len(text.split())

    def _call_llm(self, messages: list) -> str:
        """
        Call LLM for content summarization with structured JSON output.

        Args:
            messages: Messages to send to LLM

        Returns:
            LLM response as JSON string with rational, evidence, summary fields
        """
        try:
            # For now, return a structured mock response
            # In a real implementation, this would call the GLM-4.5-Air model
            # using the project's LLM configuration

            # This is a mock implementation for testing that returns proper JSON structure
            mock_response = {
                "rational": "The content contains key information directly relevant to the user's goal. I identified the main sections that provide the most valuable insights and data points.",
                "evidence": "Based on the web content analysis, the following evidence supports the goal:\n\n- The main topics and themes discussed in the content provide context for understanding the subject matter\n- Key data points and statistics mentioned offer concrete evidence\n- Authoritative sources and references mentioned add credibility to the information\n- The content structure and organization help in extracting relevant information efficiently\n\nThis comprehensive evidence covers multiple aspects and provides sufficient context for informed decision-making.",
                "summary": "The web content successfully addresses the stated goal by providing relevant information and insights. Key findings include important data points, contextual information, and actionable insights that directly contribute to achieving the specified objective. The analysis reveals both strengths and areas for consideration, offering a balanced perspective on the topic."
            }

            return json.dumps(mock_response, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            error_response = {
                "rational": "Error occurred during LLM processing",
                "evidence": f"Unable to process content due to: {str(e)}",
                "summary": f"LLM call failed: {str(e)}"
            }
            return json.dumps(error_response, ensure_ascii=False, indent=2)

    def _format_single_result(self, url: str, goal: str, structured_summary: str) -> str:
        """
        Format result for a single URL with structured output.

        Args:
            url: The processed URL
            goal: User's goal
            structured_summary: Generated structured summary (JSON string)

        Returns:
            Formatted result string
        """
        try:
            # Parse the structured summary
            summary_data = json.loads(structured_summary)

            # Extract components
            rational = summary_data.get('rational', 'No rational provided')
            evidence = summary_data.get('evidence', 'No evidence provided')
            summary = summary_data.get('summary', 'No summary provided')

            # Format the result
            return f"""## URL Analysis for: {url}

**Goal:** {goal}

### 🎯 Rational
{rational}

### 📋 Evidence
{evidence}

### 📝 Summary
{summary}

🔗 **Original URL:** {url}
📄 **Source:** Jina API
⚡ **Generated by:** Jina URL Visit Tool"""

        except json.JSONDecodeError:
            # Fallback for non-JSON response
            return f"""## URL Summary for: {url}

**Goal:** {goal}

{structured_summary}

🔗 **Original URL:** {url}
📄 **Source:** Jina API
⚡ **Generated by:** Jina URL Visit Tool

⚠️ *Note: Response format may be incomplete*"""
        except Exception as e:
            logger.error(f"Error formatting result: {str(e)}")
            return f"""## URL Summary for: {url}

**Goal:** {goal}

Error formatting result: {str(e)}

Raw Response:
{structured_summary}

🔗 **Original URL:** {url}
📄 **Source:** Jina API
⚡ **Generated by:** Jina URL Visit Tool"""


# For direct testing
if __name__ == "__main__":
    # Create tool instance
    tool = JinaURLVisitTool()

    # Test URLs
    test_cases = [
        {"url": "https://www.python.org", "goal": "Extract key information about Python programming language"},
        {"url": ["https://www.python.org", "https://docs.python.org"], "goal": "Compare Python official website and documentation"},
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}")
        print(f"{'='*60}")
        print(f"URL(s): {test_case['url']}")
        print(f"Goal: {test_case['goal']}")
        print(f"{'='*60}")

        try:
            result = tool.call(test_case)
            print(result[:1000] + "..." if len(result) > 1000 else result)
        except Exception as e:
            print(f"Test failed: {e}")

        print()