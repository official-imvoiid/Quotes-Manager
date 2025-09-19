# Quotes Manager

A comprehensive command-line application for managing, organizing, and exploring your favorite quotes. Built with Python and SQLite for efficient storage and retrieval.

## Features

### Core Functionality
- **Add Quotes**: Single quote entry or batch import multiple quotes at once
- **Search & Filter**: Search by text, author, category, or tags
- **Favorites System**: Mark and manage your favorite quotes
- **Random Quotes**: Get inspiration with random quote display (optionally filtered by category)
- **Statistics**: Detailed analytics about your quote collection

### Data Management
- **Import/Export**: Support for JSON and CSV formats
- **Database Backup**: Create backups of your quote collection
- **Multiple Authors**: Support for known authors and unknown attributions
- **Categorization**: Organize quotes by categories and tags
- **View Tracking**: Track how often quotes are viewed

### Enhanced Features
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Rich Metadata**: Store source, year, tags, and other quote details
- **Duplicate Detection**: Prevents duplicate quotes from being added
- **Database Statistics**: Comprehensive overview of your collection

## Installation

### Prerequisites
- Python 3.6 or higher
- Standard Python libraries (sqlite3, os, sys, json, csv, datetime, random, textwrap, shutil, time)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/official-imvoiid/Quotes-Manager.git
cd Quotes-Manager
```

2. No additional dependencies required - uses only Python standard library

## Quick Start

### Option 1: Use Pre-built Database
Run the main program and choose to initialize with the included quote collection:
```bash
# Windows
StartWindows.bat

# Linux/macOS
chmod +x StartLinux.sh
./StartLinux.sh

# Or directly
python QuotesManager.py
```

### Option 2: Initialize Database Manually
```bash
python MYQuotes.py
```
Choose from three initialization options:
1. **Empty Database**: Start with clean database structure
2. **Pre-loaded Database**: Use the included collection of quotes
3. **Merge Mode**: Combine existing database with the included quotes

## File Structure

```
Quotes-Manager/
├── QuotesManager.py    # Main application (START HERE)
├── MYQuotes.py         # Database initialization script
├── StartWindows.bat    # Windows launcher
├── StartLinux.sh       # Linux/macOS launcher
├── quotes.db           # SQLite database (created on first run)
└── README.md           # This file
```

### File Descriptions

- **`QuotesManager.py`** - The main application interface with full quote management functionality
- **`MYQuotes.py`** - Database setup script containing pre-defined quotes and initialization options
- **`StartWindows.bat`** - Windows batch file for easy launching
- **`StartLinux.sh`** - Shell script for Linux/macOS systems
- **`quotes.db`** - SQLite database file (auto-created)

## Usage Guide

### Main Menu Options

#### Basic Operations
1. **Add single quote** - Enter one quote with author, category, and tags
2. **Add multiple quotes** - Batch entry mode for multiple quotes
3. **Show all quotes** - Display your entire collection with optional statistics
4. **Random quote** - Get a random quote, optionally filtered by category
5. **Delete quote by ID** - Remove quotes from your collection

#### Search & Favorites
6. **Search quotes** - Find quotes by text, author, category, or tags
7. **Add to favorites** - Mark quotes as favorites
8. **Remove from favorites** - Unmark favorite quotes
9. **Show favorites** - Display only your favorite quotes

#### Data Management
10. **Statistics** - View detailed analytics about your collection
11. **Export quotes** - Save quotes to JSON or CSV files
12. **Import quotes** - Load quotes from JSON or CSV files
13. **Backup database** - Create database backups
14. **Exit** - Close the application

### Database Initialization Options

When running `MYQuotes.py`, you can choose:

#### For New Installation:
1. **Create EMPTY database** - Just the structure, no quotes
2. **Create database with pre-loaded quotes** - Includes the author's curated collection

#### For Existing Database:
1. **Delete and create EMPTY database** - Reset to empty structure
2. **Replace with pre-loaded quotes** - Clear existing and use author's collection
3. **Merge with pre-loaded quotes** - Add author's quotes to your existing collection

## Quote Collection

The included quote database contains:
- **Philosophy**: Classic philosophical quotes from Socrates, Nietzsche, Camus, and more
- **Stoicism**: Wisdom from Marcus Aurelius, Epictetus, and Seneca
- **Eastern Philosophy**: Insights from Buddhism, Taoism, and spiritual traditions
- **Psychology**: Carl Jung's profound observations on the human psyche
- **Personal Reflections**: Contemporary quotes on life, love, loss, and growth

Categories include: Motivation, Resilience, Philosophy, Love, Death, Transformation, Purpose, and many more.

## Export/Import Formats

### JSON Format
```json
[
  {
    "id": 1,
    "quote_text": "The unexamined life is not worth living.",
    "author": "Socrates",
    "category": "Philosophy",
    "tags": "self-awareness,meaning",
    "source": "",
    "year": null,
    "favorite": 0,
    "times_viewed": 5,
    "date_added": "2024-01-01 12:00:00",
    "last_viewed": "2024-01-15 14:30:00"
  }
]
```

### CSV Format
Supports all database fields in standard CSV format with headers.

## Database Schema

```sql
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_text TEXT NOT NULL UNIQUE,
    author TEXT DEFAULT 'Unknown',
    category TEXT DEFAULT 'General',
    tags TEXT DEFAULT '',
    source TEXT DEFAULT '',
    year INTEGER DEFAULT NULL,
    favorite BOOLEAN DEFAULT 0,
    times_viewed INTEGER DEFAULT 0,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_viewed DATETIME DEFAULT NULL
);
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

**Database not found**: Run `python MYQuotes.py` to initialize the database.

**Permission errors on Linux/macOS**: Make the shell script executable:
```bash
chmod +x StartLinux.sh
```

**Import errors**: Ensure your JSON/CSV files are properly formatted and encoded in UTF-8.

**Python version issues**: This project requires Python 3.6+. Check your version:
```bash
python --version
```

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/official-imvoiid/Quotes-Manager).

---

*"The privilege of a lifetime is to become who you truly are."* - Carl Jung
