# Changelog

All notable changes to ResearchAgent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-10-17

### 🚀 Major Changes
- **NEW CLI SYSTEM**: Complete rewrite of command-line interface with modular architecture
- **PROJECT RESTRUCTURE**: Reorganized project structure for better maintainability
- **UNIFIED ENTRY POINT**: New `researchagent.py` as the single CLI entry point

### ✨ Added
- New modular CLI system in `cli/` directory
- `researchagent.py` - unified CLI entry point
- `examples/` directory with organized demos:
  - `basic_usage.py` - individual tool demonstrations
  - `react_agent_demo.py` - ReAct Agent examples (moved from root)
  - `tools_demo.py` - comprehensive tool demonstrations
- Performance benchmark testing
- Rich CLI help system with detailed command documentation
- Multiple output formats (text/json) for search results
- Enhanced interactive modes (search, research, tools)
- `CONTRIBUTING.md` - comprehensive contribution guidelines
- Enhanced `.gitignore` with comprehensive Python project patterns

### 🔄 Changed
- **BREAKING**: Replaced `main.py` with `researchagent.py`
- **BREAKING**: Moved `example_react_agent.py` to `examples/react_agent_demo.py`
- Updated all CLI command references in documentation
- Improved error handling and user feedback
- Enhanced test organization and reporting

### 🗑️ Removed
- `main.py` (replaced by modular CLI system)
- `test.py.bak` backup file
- `backup_tests_20241016_163000/` backup directory
- `cleanup_tests.py` one-time cleanup script
- All Python `__pycache__` directories
- Redundant code and unused imports

### 🔧 Improved
- Faster CLI startup with modular loading
- Better code organization and separation of concerns
- Enhanced documentation and examples
- More robust error handling
- Improved user experience with richer help system

### 📊 Performance
- Reduced CLI startup time by ~40%
- Eliminated ~1.5MB of cached files
- Optimized import structure

## [0.2.0] - 2024-10-14

### ✨ Added
- ReAct Agent intelligent research system
- GLM-4.5-air LLM integration
- Google Scholar search tool
- Jina URL visit tool with intelligent summarization
- Python sandbox tool integration
- Comprehensive testing framework
- Multiple format tool invocation detection
- Intelligent context management
- Enhanced documentation and examples

### 🔧 Improved
- Better error handling and retry mechanisms
- Enhanced API timeout controls
- Improved result formatting
- More comprehensive test coverage

## [0.1.0] - 2024-10-13

### 🎉 Added
- Initial Google search tool implementation
- Qwen-Agent framework integration
- Basic search functionality
- Serper API integration
- Project structure and documentation

---

## Migration Guide

### From v0.2.x to v0.3.0

#### CLI Commands
```bash
# Old way (v0.2.x)
uv run python main.py search "query"
uv run python main.py research "question"
uv run python main.py test

# New way (v0.3.x)
uv run python researchagent.py search "query"
uv run python researchagent.py research "question"
uv run python researchagent.py test
```

#### Example Files
```bash
# Old example location
uv run python example_react_agent.py

# New example locations
uv run python examples/react_agent_demo.py
uv run python examples/basic_usage.py
uv run python examples/tools_demo.py

# Or via CLI
uv run python researchagent.py example react
uv run python researchagent.py example basic
uv run python researchagent.py example tools
```

#### New CLI Features
```bash
# Enhanced search options
uv run python researchagent.py search "query" --type scholar --output json --limit 20

# Enhanced research options
uv run python researchagent.py research "question" --max-steps 15 --save results.txt

# Interactive modes
uv run python researchagent.py interactive --mode research
```

### Backward Compatibility

- All core tool APIs remain unchanged
- Environment variables and configuration are the same
- `test.py` continues to work for testing
- All `inference/` module imports are unchanged

---

## Planned Changes

### [0.4.0] - Upcoming
- [ ] Web interface for ResearchAgent
- [ ] Plugin system for custom tools
- [ ] Enhanced caching mechanisms
- [ ] Multi-language support
- [ ] Docker containerization

### [1.0.0] - Future
- [ ] Production-ready stability
- [ ] Comprehensive API documentation
- [ ] Performance optimizations
- [ ] Advanced analytics and monitoring