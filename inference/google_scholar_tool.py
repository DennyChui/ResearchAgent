"""
Google Scholar Search Tool for Qwen-Agent

This module implements a Google Scholar search tool using the Serper API
to provide academic search capabilities to Qwen-Agent.
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


@register_tool('google_scholar')
class GoogleScholarTool(BaseTool):
    """
    Google Scholar search tool using Serper API to search academic literature.

    This tool allows Qwen-Agent to perform Google Scholar searches and retrieve
    academic search results with publication information, citations, and PDF links.
    """

    name = 'google_scholar'
    description = 'Search Google Scholar for academic literature using Serper API. Returns scholarly results with publication info, citations, and PDF links.'

    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": ["string", "array"],
                "description": "Search query(s) - can be a single query string or array of queries to perform on Google Scholar",
                "minItems": 1,
                "items": {"type": "string"}
            }
        },
        "required": ["query"]
    }

    def __init__(self):
        """Initialize the Google Scholar Search tool."""
        super().__init__()
        self.api_key = os.getenv('SERPER_KEY_ID', '2fb71d719108d02677a2d8492809a4922e766c3c')
        self.api_host = 'google.serper.dev'
        self.api_endpoint = '/scholar'

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Perform Google Scholar search using Serper API.

        Args:
            params: Search parameters, can be string, dict, or array
            **kwargs: Additional keyword arguments

        Returns:
            Formatted scholarly search results as string
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
                return "Error: Invalid parameters format. Expected string, dictionary, or array."

            if not query or not str(query).strip():
                return "Error: Search query cannot be empty."

            # Convert query to list for batch processing
            if isinstance(query, str):
                queries = [query.strip()]
            elif isinstance(query, list):
                queries = [str(q).strip() for q in query if str(q).strip()]
            else:
                return "Error: Query must be a string or array of strings."

            if not queries:
                return "Error: No valid queries provided."

            # Perform searches and combine results
            all_results = []
            for i, single_query in enumerate(queries):
                if len(queries) > 1:
                    all_results.append(f"\n## Scholar Search Results for Query {i+1}: '{single_query}'\n")

                search_results = self._perform_search(single_query)
                formatted_result = self._format_results(single_query, search_results)
                all_results.append(formatted_result)

            # Return combined results
            return "\n".join(all_results)

        except Exception as e:
            logger.error(f"Error in Google Scholar search: {str(e)}")
            return f"Error performing Google Scholar search: {str(e)}"

    def _perform_search(self, query: str) -> Dict[str, Any]:
        """
        Perform the actual API call to Serper Scholar endpoint.

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
                'User-Agent': 'Qwen-Agent-Google-Scholar-Tool/1.0'
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
                logger.error(f"Serper Scholar API returned status {response.status}: {response_data}")
                return {
                    'error': f"API request failed with status {response.status}",
                    'message': response_data
                }

        except Exception as e:
            logger.error(f"Error calling Serper Scholar API: {str(e)}")
            return {
                'error': "Failed to connect to scholar search service",
                'message': str(e)
            }

    def _format_results(self, query: str, results: Dict[str, Any]) -> str:
        """
        Format scholarly search results into a readable string.

        Args:
            query: The original search query
            results: API response data

        Returns:
            Formatted scholarly search results string
        """
        # Check for errors
        if 'error' in results:
            return f"Scholar search failed: {results.get('message', 'Unknown error')}"

        # Extract organic results (scholar papers)
        organic_results = results.get('organic', [])

        if not organic_results:
            return f"A Google Scholar search for '{query}' found no academic results."

        # Format each result
        formatted_pages = []
        for i, result in enumerate(organic_results, 1):
            title = result.get('title', 'No title')
            snippet = result.get('snippet', 'No description available')
            link = result.get('link', '')

            # Scholar-specific fields
            publication_info = result.get('publicationInfo', '')
            year = result.get('year', '')
            cited_by = result.get('citedBy', '')
            pdf_url = result.get('pdfUrl', '')

            # Clean up snippet (remove extra whitespace and newlines)
            snippet = ' '.join(snippet.split())

            # Build formatted result
            formatted_page = f"### {i}. {title}\n\n"

            if snippet:
                formatted_page += f"{snippet}\n\n"

            # Add publication information
            if publication_info:
                formatted_page += f"**Publication:** {publication_info}\n"

            # Add year if available
            if year:
                formatted_page += f"**Year:** {year}\n"

            # Add citation count if available
            if cited_by:
                formatted_page += f"**Cited by:** {cited_by}\n"

            # Add PDF link if available
            if pdf_url:
                formatted_page += f"**PDF:** {pdf_url}\n"

            # Add main link
            formatted_page += f"🔗 {link}"

            formatted_pages.append(formatted_page)

        # Add search information
        search_info = results.get('searchInformation', {})
        total_results = search_info.get('totalResults', len(organic_results))
        search_time = search_info.get('formattedSearchTime', 'N/A')

        # Create final result string
        result_string = (
            f"A Google Scholar search for '{query}' found {total_results} results (search time: {search_time}s):\n\n"
            f"## Academic Results\n\n"
            f"{chr(10).join(formatted_pages)}"
        )

        return result_string


# For direct testing
if __name__ == "__main__":
    # Create tool instance
    tool = GoogleScholarTool()

    # Test searches with academic queries
    test_queries = [
        "machine learning neural networks",
        "climate change impact assessment",
        "quantum computing applications"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing Google Scholar search for: {query}")
        print(f"{'='*60}")

        result = tool.call({"query": query})
        print(result)
        print()