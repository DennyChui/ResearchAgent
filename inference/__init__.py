"""
Inference modules for ResearchAgent

This package contains core inference tools and utilities.
"""

from .google_search_tool import GoogleSearchTool
from .google_scholar_tool import GoogleScholarTool

__all__ = ['GoogleSearchTool', 'GoogleScholarTool']