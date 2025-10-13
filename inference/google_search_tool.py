"""
Google Search Tool for Qwen-Agent

This module implements a Google search tool using the Serper API
to provide web search capabilities to Qwen-Agent.
"""

import json
import urllib.parse
import http.client
import os
from typing import Union, Dict, Any
import logging

from qwen_agent.tools.base import BaseTool, register_tool

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@register_tool('google_search')
class GoogleSearchTool(BaseTool):
    """
    Google Search tool using Serper API to search the web.

    This tool allows Qwen-Agent to perform Google searches and retrieve
    organic search results in a formatted string.
    """

    description = 'Search Google for information using Serper API. Returns organic search results with titles, snippets, and links.'

    parameters = [
        {
            'name': 'query',
            'type': 'string',
            'description': 'The search query to perform on Google',
            'required': True
        }
    ]

    def __init__(self):
        """Initialize the Google Search tool."""
        super().__init__()
        self.api_key = os.getenv('SERPER_KEY_ID', '2fb71d719108d02677a2d8492809a4922e766c3c')
        self.api_host = 'google.serper.dev'
        self.api_endpoint = '/search'

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Perform Google search using Serper API.

        Args:
            params: Search parameters, can be string or dict
            **kwargs: Additional keyword arguments

        Returns:
            Formatted search results as string
        """
        try:
            # Parse parameters
            if isinstance(params, str):
                try:
                    params_dict = json.loads(params)
                    query = params_dict.get('query', '')
                except json.JSONDecodeError:
                    # If params is not valid JSON, treat it as the query directly
                    query = params
            elif isinstance(params, dict):
                query = params.get('query', '')
            else:
                return "Error: Invalid parameters format. Expected string or dictionary."

            if not query or not query.strip():
                return "Error: Search query cannot be empty."

            # Perform the search
            search_results = self._perform_search(query.strip())

            # Format and return results
            return self._format_results(query, search_results)

        except Exception as e:
            logger.error(f"Error in Google search: {str(e)}")
            return f"Error performing Google search: {str(e)}"

    def _perform_search(self, query: str) -> Dict[str, Any]:
        """
        Perform the actual API call to Serper.

        Args:
            query: The search query

        Returns:
            API response as dictionary
        """
        try:
            # Create HTTPS connection with timeout
            conn = http.client.HTTPSConnection(self.api_host, timeout=10)

            # Prepare request headers
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'Qwen-Agent-Google-Search-Tool/1.0'
            }

            # Prepare request payload
            payload = {
                'q': query,
                'num': 10  # Number of results to retrieve
            }

            # Make the request
            conn.request('POST', self.api_endpoint,
                        body=json.dumps(payload),
                        headers=headers)

            # Get response
            response = conn.getresponse()
            response_data = response.read().decode('utf-8')

            # Close connection
            conn.close()

            # Parse response
            if response.status == 200:
                return json.loads(response_data)
            else:
                logger.error(f"Serper API returned status {response.status}: {response_data}")
                return {
                    'error': f"API request failed with status {response.status}",
                    'message': response_data
                }

        except Exception as e:
            logger.error(f"Error calling Serper API: {str(e)}")
            return {
                'error': "Failed to connect to search service",
                'message': str(e)
            }

    def _format_results(self, query: str, results: Dict[str, Any]) -> str:
        """
        Format search results into a readable string.

        Args:
            query: The original search query
            results: API response data

        Returns:
            Formatted search results string
        """
        # Check for errors
        if 'error' in results:
            return f"Search failed: {results.get('message', 'Unknown error')}"

        # Extract organic results
        organic_results = results.get('organic', [])

        if not organic_results:
            return f"A Google search for '{query}' found no organic results."

        # Format each result
        formatted_pages = []
        for i, result in enumerate(organic_results, 1):
            title = result.get('title', 'No title')
            snippet = result.get('snippet', 'No description available')
            link = result.get('link', '')

            # Clean up snippet (remove extra whitespace and newlines)
            snippet = ' '.join(snippet.split())

            formatted_page = f"### {i}. {title}\n\n{snippet}\n\n🔗 {link}"
            formatted_pages.append(formatted_page)

        # Add search information
        search_info = results.get('searchInformation', {})
        total_results = search_info.get('totalResults', len(organic_results))
        search_time = search_info.get('formattedSearchTime', 'N/A')

        # Create final result string
        result_string = (
            f"A Google search for '{query}' found {total_results} results (search time: {search_time}s):\n\n"
            f"## Web Results\n\n"
            f"{chr(10).join(formatted_pages)}"
        )

        return result_string


# For direct testing
if __name__ == "__main__":
    # Create tool instance
    tool = GoogleSearchTool()

    # Test search
    test_queries = [
        "Python programming",
        "artificial intelligence latest news",
        "climate change effects"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing search for: {query}")
        print(f"{'='*60}")

        result = tool.call({"query": query})
        # print(result[:1000] + "..." if len(result) > 1000 else result)
        print(result)
        print()