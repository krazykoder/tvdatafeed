#!/usr/bin/env python3
"""
Build a guided learning tour of the tvdatafeed codebase.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path("/Users/towshif/code/python/tvdatafeed")
INTERMEDIATE_DIR = PROJECT_ROOT / ".understand-anything" / "intermediate"

# Load graph and layers
with open(INTERMEDIATE_DIR / 'assembled-graph.json') as f:
    graph = json.load(f)

with open(INTERMEDIATE_DIR / 'layers.json') as f:
    layers = json.load(f)

nodes = graph['nodes']
edges = graph['edges']

print("[Phase 5/7] Building guided tour...")

# Define tour steps aligned with project structure
tour_steps = [
    {
        'order': 1,
        'title': 'Project Overview',
        'description': 'Start here to understand tvdatafeed\'s purpose: download historical OHLCV data from TradingView via WebSocket.',
        'nodeIds': ['document:README.md'],
        'languageLesson': 'This project demonstrates WebSocket-based data collection, async I/O patterns, and financial data parsing.'
    },
    {
        'order': 2,
        'title': 'Package Entry Point',
        'description': 'The public API is defined in __init__.py, which exports the main tvData class and Interval enum.',
        'nodeIds': ['file:tvDatafeed/__init__.py'],
        'languageLesson': 'See how the package exposes its primary interface through __all__ exports.'
    },
    {
        'order': 3,
        'title': 'Core Engine: tvData Class',
        'description': 'The main implementation in tvDatafeed/main.py contains the entire data-fetching logic: authentication, WebSocket communication, parsing.',
        'nodeIds': ['file:tvDatafeed/main.py', 'class:tvDatafeed/main.py:tvData'],
        'languageLesson': 'Explore the tvData class to understand WebSocket message framing (~m~...~m~), regex parsing, and state management.'
    },
    {
        'order': 4,
        'title': 'Public API Methods',
        'description': 'Three main entry points: get_timeseries (OHLCV data), get_financials (financial metrics), and get_timeseries_earnings_dividends (events).',
        'nodeIds': [
            'function:tvDatafeed/main.py:tvData.get_timeseries',
            'function:tvDatafeed/main.py:tvData.get_financials',
            'function:tvDatafeed/main.py:tvData.get_timeseries_earnings_dividends'
        ],
        'languageLesson': 'Each method follows a similar pattern: format symbol → create WebSocket session → send requests → parse response → return DataFrame.'
    },
    {
        'order': 5,
        'title': 'Authentication & Connection',
        'description': 'Understand how authentication works: users can authenticate with credentials or use unauthorized tokens.',
        'nodeIds': ['function:tvDatafeed/main.py:tvData.__auth', 'function:tvDatafeed/main.py:tvData.__send_request'],
        'languageLesson': 'The WebSocket connection uses set_auth_token messages and maintains state across multiple requests.'
    },
    {
        'order': 6,
        'title': 'Data Parsing & Normalization',
        'description': 'See how raw WebSocket responses are parsed: regex extraction, JSON parsing, DataFrame creation.',
        'nodeIds': ['function:tvDatafeed/main.py:tvData.__create_timeseries_df'],
        'languageLesson': 'Learn regex patterns for parsing time series data and handling special cases like indices without volume.'
    },
    {
        'order': 7,
        'title': 'Test & Debug Scripts',
        'description': 'Validation utilities in debug/ folder: test_parser.py validates parsing, download_raw_data.py captures live WebSocket data.',
        'nodeIds': ['file:debug/test_parser.py', 'file:debug/download_raw_data.py'],
        'languageLesson': 'See how to validate implementations and create reproducible test data.'
    },
    {
        'order': 8,
        'title': 'Data Extraction & Analysis',
        'description': 'The data_extract/ folder contains analysis of financial fields and earnings/dividend patterns.',
        'nodeIds': ['document:data_extract/TIMESERIES_NOMENCLATURE_REFERENCE.md', 'document:data_extract/TIMESERIES_PATTERNS_DETAILED.md'],
        'languageLesson': 'Understand the structure of financial data and how WebSocket messages encode complex hierarchies.'
    },
    {
        'order': 9,
        'title': 'Configuration & Setup',
        'description': 'Install dependencies and understand the project structure through setup.py and requirements.txt.',
        'nodeIds': ['file:setup.py', 'file:requirements.txt'],
        'languageLesson': 'Key dependencies: pandas (data frames), websocket-client (WebSocket protocol), requests (HTTP auth).'
    },
    {
        'order': 10,
        'title': 'Putting It All Together',
        'description': 'Review examples in tv.ipynb or fiddle_socket.py to see complete workflows: authenticate, download OHLCV, financials, events.',
        'nodeIds': ['file:tv.ipynb', 'file:fiddle_socket.py'],
        'languageLesson': 'Interactive examples show real-world usage patterns and how to handle authentication errors.'
    }
]

# Write tour
tour_file = INTERMEDIATE_DIR / 'tour.json'
with open(tour_file, 'w') as f:
    json.dump(tour_steps, f, indent=2)

print(f"  Created {len(tour_steps)} tour steps:")
for step in tour_steps:
    print(f"    {step['order']}. {step['title']} ({len(step['nodeIds'])} nodes)")

print(f"\n✓ Phase 5 complete")
print(f"  Output: {tour_file}")
