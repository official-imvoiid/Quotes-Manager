import sqlite3
import os
import sys
import json
import csv
from datetime import datetime
from typing import List, Tuple, Optional, Dict
import random
import textwrap
import shutil
import time

# For cross-platform non-echoing input
if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix/Linux/Mac
    import termios
    import tty

class QuotesManager:
    def __init__(self, db_name: str = "quotes.db"):
        """Initialize the quote database with enhanced features"""
        self.db_name = db_name
        self.setup_database()
    
    def setup_database(self):
        """Create enhanced quotes table with additional fields"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Enhanced quotes table with more fields
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
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
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_author ON quotes(author)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_category ON quotes(category)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_favorite ON quotes(favorite)
            ''')
            
            conn.commit()
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self, message="Press Enter to continue..."):
        """Pause execution with optional message - non-echoing input"""
        print(f"\n{message}", end='', flush=True)
        self._getch()
    
    def _getch(self):
        """Get a single character without echoing - cross-platform"""
        if os.name == 'nt':  # Windows
            msvcrt.getch()
        else:  # Unix
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def initialize_from_myquotes(self):
        """Initialize database with quotes from MYQuotes.py"""
        try:
            if os.path.exists('MYQuotes.py'):
                print("Running MYQuotes.py...")
                print("It will populate the database. Wait for it to finish.")
                # Run MYQuotes.py interactively and wait for it to end
                import subprocess
                subprocess.call([sys.executable, 'MYQuotes.py'])
                print("\nMYQuotes.py finished. Database should now be populated.")
                return True
            else:
                print("[X] MYQuotes.py file not found!")
                print("Please ensure MYQuotes.py is in the same directory.")
                return False
        except Exception as e:
            print(f"[X] Error running MYQuotes.py: {e}")
            return False
    
    def add_quote(self, quote: str, author: str = "Unknown", 
                  category: str = "General", tags: str = "", 
                  source: str = "", year: int = None) -> Optional[int]:
        """Add a new quote with enhanced metadata"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO quotes (quote_text, author, category, tags, source, year)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (quote.strip(), author, category, tags, source, year))
                
                quote_id = cursor.lastrowid
                print(f"[OK] Quote #{quote_id} saved successfully!")
                return quote_id
        except sqlite3.IntegrityError:
            print(f"[!] This quote already exists in the database!")
            return None
        except Exception as e:
            print(f"[X] Error adding quote: {e}")
            return None
    
    def search_quotes(self, search_term: str, search_in: str = "all") -> List[Tuple]:
        """Search quotes by text, author, category, or tags"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            search_term = f"%{search_term}%"
            
            if search_in == "all":
                query = '''
                    SELECT id, quote_text, author, category, favorite
                    FROM quotes 
                    WHERE quote_text LIKE ? 
                       OR author LIKE ? 
                       OR category LIKE ? 
                       OR tags LIKE ?
                    ORDER BY id
                '''
                cursor.execute(query, (search_term, search_term, search_term, search_term))
            elif search_in == "text":
                cursor.execute('SELECT id, quote_text, author, category, favorite FROM quotes WHERE quote_text LIKE ? ORDER BY id', (search_term,))
            elif search_in == "author":
                cursor.execute('SELECT id, quote_text, author, category, favorite FROM quotes WHERE author LIKE ? ORDER BY id', (search_term,))
            elif search_in == "category":
                cursor.execute('SELECT id, quote_text, author, category, favorite FROM quotes WHERE category LIKE ? ORDER BY id', (search_term,))
            
            return cursor.fetchall()
    
    def show_all_quotes(self, limit: int = None, show_stats: bool = False):
        """Display all quotes with improved formatting"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            if limit:
                cursor.execute('SELECT id, quote_text, author, category, favorite FROM quotes ORDER BY id DESC LIMIT ?', (limit,))
            else:
                cursor.execute('SELECT id, quote_text, author, category, favorite FROM quotes ORDER BY id')
            
            quotes = cursor.fetchall()
            
            if not quotes:
                print("No quotes found! Add some quotes first.")
                self.pause()
                return
            
            # Get statistics if requested
            total_count = len(quotes)
            if show_stats:
                cursor.execute('SELECT COUNT(*) FROM quotes')
                total = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(DISTINCT author) FROM quotes WHERE author != "Unknown"')
                authors = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM quotes WHERE author = "Unknown"')
                unknown_authors = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(DISTINCT category) FROM quotes')
                categories = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM quotes WHERE favorite = 1')
                favorites = cursor.fetchone()[0]
                
                print("\nSTATISTICS:")
                print(f"  Total Quotes: {total}")
                print(f"  Known Authors: {authors}")
                print(f"  Unknown Authors: {unknown_authors}")
                print(f"  Categories: {categories}")
                print(f"  Favorites: {favorites}")
            
            print(f"\nQUOTES COLLECTION ({total_count} quotes):")
            print("-" * 75)
            
            for quote_id, text, author, category, favorite in quotes:
                # Simpler format
                fav = "[*]" if favorite else "   "
                print(f"{fav} #{quote_id} {text}")
                print(f"      Author: {author}")
                print(f"      Category: {category}")
                print()
            
            self.pause()
    
    def add_remove_favorite(self, quote_id: int, action: str = "toggle"):
        """Add, remove, or toggle favorite status of a quote"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT favorite, quote_text FROM quotes WHERE id = ?', (quote_id,))
            result = cursor.fetchone()
            
            if result:
                current_status = result[0]
                quote_preview = result[1][:50] + "..." if len(result[1]) > 50 else result[1]
                
                if action == "toggle":
                    new_status = 0 if current_status else 1
                elif action == "add":
                    new_status = 1
                elif action == "remove":
                    new_status = 0
                else:
                    print("[X] Invalid action!")
                    return
                
                cursor.execute('UPDATE quotes SET favorite = ? WHERE id = ?', (new_status, quote_id))
                
                if action == "add":
                    if new_status == 1:
                        print(f"[OK] Quote #{quote_id} added to favorites!")
                        print(f'     "{quote_preview}"')
                    else:
                        print(f"[!] Quote #{quote_id} is already in favorites!")
                elif action == "remove":
                    if new_status == 0:
                        print(f"[OK] Quote #{quote_id} removed from favorites!")
                        print(f'     "{quote_preview}"')
                    else:
                        print(f"[!] Quote #{quote_id} is not in favorites!")
                else:
                    status_text = "added to favorites" if new_status else "removed from favorites"
                    print(f"[OK] Quote #{quote_id} {status_text}!")
                
                time.sleep(2)  # Brief pause to show the message
            else:
                print(f"[X] Quote #{quote_id} not found!")
                time.sleep(2)
    
    def show_favorites(self):
        """Display only favorite quotes"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, quote_text, author, category FROM quotes WHERE favorite = 1 ORDER BY id')
            quotes = cursor.fetchall()
            
            if not quotes:
                print("\nNo favorite quotes yet! Mark some quotes as favorites.")
                self.pause()
                return
            
            print(f"\nFAVORITE QUOTES ({len(quotes)} total):")
            print("-" * 75)
            
            for quote_id, text, author, category in quotes:
                print(f"[*] #{quote_id} {text}")
                print(f"      Author: {author}")
                print(f"      Category: {category}")
                print()
            
            self.pause()
    
    def get_random_quote(self, category: str = None):
        """Get a random quote, optionally filtered by category"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            if category:
                cursor.execute('''
                    SELECT id, quote_text, author, category 
                    FROM quotes 
                    WHERE category = ? 
                    ORDER BY RANDOM() 
                    LIMIT 1
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT id, quote_text, author, category 
                    FROM quotes 
                    ORDER BY RANDOM() 
                    LIMIT 1
                ''')
            
            quote = cursor.fetchone()
            
            if quote:
                # Update view statistics
                cursor.execute('UPDATE quotes SET times_viewed = times_viewed + 1, last_viewed = CURRENT_TIMESTAMP WHERE id = ?', (quote[0],))
                conn.commit()
                
                print(f"RANDOM QUOTE #{quote[0]}:")
                print("------------------------------------------------------------")
                print(quote[1])
                print(f"\t- {quote[2]} | Category: {quote[3]}")
            else:
                print("[X] No quotes available!")
            
            self.pause()
    
    def delete_quote(self, quote_id: int):
        """Delete a quote by ID with confirmation"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # First, show the quote to be deleted
            cursor.execute('SELECT quote_text, author FROM quotes WHERE id = ?', (quote_id,))
            quote = cursor.fetchone()
            
            if quote:
                print(f"\nQuote to delete:")
                print(f'  #{quote_id}: "{quote[0][:60]}{"..." if len(quote[0]) > 60 else ""}"')
                print(f"  - {quote[1]}")
                
                confirm = input("\nAre you sure? (y/N): ").lower()
                if confirm == 'y':
                    cursor.execute('DELETE FROM quotes WHERE id = ?', (quote_id,))
                    conn.commit()
                    print(f"[OK] Quote #{quote_id} deleted successfully!")
                else:
                    print("[!] Deletion cancelled.")
            else:
                print(f"[X] Quote #{quote_id} not found!")
            
            time.sleep(2)
    
    def export_quotes(self, format: str = "json", filename: str = None):
        """Export quotes to JSON or CSV file"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM quotes ORDER BY id')
            quotes = cursor.fetchall()
            
            if not quotes:
                print("[X] No quotes to export!")
                self.pause()
                return
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"quotes_export_{timestamp}.{format}"
            
            try:
                if format == "json":
                    data = []
                    for quote in quotes:
                        data.append(dict(zip(columns, quote)))
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                
                elif format == "csv":
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(columns)
                        writer.writerows(quotes)
                
                print(f"[OK] Exported {len(quotes)} quotes to {filename}")
                self.pause()
            except Exception as e:
                print(f"[X] Export failed: {e}")
                self.pause()
    
    def import_quotes(self, filename: str):
        """Import quotes from JSON or CSV file"""
        if not os.path.exists(filename):
            print(f"[X] File {filename} not found!")
            self.pause()
            return
        
        imported = 0
        skipped = 0
        
        try:
            if filename.endswith('.json'):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    result = self.add_quote(
                        item.get('quote_text', ''),
                        item.get('author', 'Unknown'),
                        item.get('category', 'General'),
                        item.get('tags', ''),
                        item.get('source', ''),
                        item.get('year')
                    )
                    if result:
                        imported += 1
                    else:
                        skipped += 1
            
            elif filename.endswith('.csv'):
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        result = self.add_quote(
                            row.get('quote_text', ''),
                            row.get('author', 'Unknown'),
                            row.get('category', 'General'),
                            row.get('tags', ''),
                            int(row.get('year')) if row.get('year') else None
                        )
                        if result:
                            imported += 1
                        else:
                            skipped += 1
            
            print(f"[OK] Import complete: {imported} added, {skipped} skipped (duplicates)")
            self.pause()
        except Exception as e:
            print(f"[X] Import failed: {e}")
            self.pause()
    
    def backup_database(self, backup_name: str = None):
        """Create a backup of the database"""
        try:
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"quotes_backup_{timestamp}.db"
            
            shutil.copy2(self.db_name, backup_name)
            print(f"[OK] Database backed up to: {backup_name}")
            self.pause()
        except Exception as e:
            print(f"[X] Backup failed: {e}")
            self.pause()
    
    def get_statistics(self):
        """Display detailed statistics about the quotes database"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Basic stats
            cursor.execute('SELECT COUNT(*) FROM quotes')
            total = cursor.fetchone()[0]
            
            if total == 0:
                print("No quotes in database yet!")
                self.pause()
                return
            
            cursor.execute('SELECT COUNT(DISTINCT author) FROM quotes WHERE author != "Unknown"')
            known_authors_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM quotes WHERE author = "Unknown"')
            unknown_authors = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT category) FROM quotes')
            categories_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM quotes WHERE favorite = 1')
            favorites = cursor.fetchone()[0]
            
            # Most viewed quote
            cursor.execute('SELECT id, quote_text, author, times_viewed FROM quotes ORDER BY times_viewed DESC LIMIT 1')
            most_viewed = cursor.fetchone()
            
            # All authors with counts (including Unknown)
            cursor.execute('''
                SELECT author, COUNT(*) as count 
                FROM quotes 
                GROUP BY author 
                ORDER BY count DESC, author
            ''')
            all_authors = cursor.fetchall()
            
            # All categories with counts
            cursor.execute('''
                SELECT category, COUNT(*) as count 
                FROM quotes 
                GROUP BY category 
                ORDER BY count DESC, category
            ''')
            all_categories = cursor.fetchall()
            
            print("\n" + "=" * 70)
            print("QUOTES DATABASE STATISTICS")
            print("=" * 70)
            print(f"Total Quotes: {total}")
            print(f"Total Authors: {known_authors_count + (1 if unknown_authors > 0 else 0)}")
            print(f"  Known Authors: {known_authors_count}")
            print(f"  Unknown Author Quotes: {unknown_authors}")
            print(f"Categories: {categories_count}")
            print(f"Favorites: {favorites} ({favorites*100//total if total else 0}%)")
            
            if most_viewed and most_viewed[3] > 0:
                print(f"\nMost Viewed Quote (viewed {most_viewed[3]} times):")
                print(f'  #{most_viewed[0]}: "{most_viewed[1][:50]}{"..." if len(most_viewed[1]) > 50 else ""}"')
                print(f"  - {most_viewed[2]}")
            
            print("\n" + "-" * 70)
            print("ALL AUTHORS:")
            print("-" * 70)
            for author, count in all_authors:
                print(f"  {author}: {count} quotes")
            
            print("\n" + "-" * 70)
            print("ALL CATEGORIES:")
            print("-" * 70)
            for category, count in all_categories:
                print(f"  {category}: {count} quotes")
            
            print("=" * 70)
            self.pause()
    
    def add_multiple_quotes(self):
        """Add multiple quotes at once"""
        self.clear_screen()
        print("\nADD MULTIPLE QUOTES")
        print("=" * 60)
        print("Instructions:")
        print("  - Paste or type multiple quotes")
        print("  - One quote per line")
        print("  - Type 'DONE' on a new line when finished")
        print("=" * 60)
        
        quotes = []
        print("\nEnter quotes (type 'DONE' when finished):\n")
        
        while True:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            if line.strip():
                quotes.append(line.strip())
        
        if not quotes:
            print("[X] No quotes entered!")
            self.pause()
            return
        
        print(f"\nYou entered {len(quotes)} quotes.")
        print("-" * 50)
        
        # Ask for author preference first
        print("\nHow do you want to set authors?")
        print("1. Same author for all quotes")
        print("2. Enter author for each quote individually")
        print("3. All quotes are 'Unknown' author")
        
        author_choice = input("\nChoose (1/2/3): ").strip()
        
        authors_list = []
        if author_choice == '1':
            author = input("Enter author name for all quotes: ").strip() or "Unknown"
            authors_list = [author] * len(quotes)
        elif author_choice == '2':
            print("\nEnter author for each quote (press Enter for 'Unknown'):")
            for i, quote in enumerate(quotes, 1):
                print(f'\n{i}. "{quote[:50]}{"..." if len(quote) > 50 else ""}"')
                ind_author = input(f"   Author: ").strip() or "Unknown"
                authors_list.append(ind_author)
        else:
            authors_list = ["Unknown"] * len(quotes)
        
        # Ask for category and tags
        category = input("\nCategory for all quotes (Enter for 'General'): ").strip() or "General"
        tags = input("Tags for all (comma-separated, optional): ").strip()
        
        # Add quotes to database
        added = 0
        skipped = 0
        
        for quote, quote_author in zip(quotes, authors_list):
            result = self.add_quote(quote, quote_author, category, tags)
            if result:
                added += 1
            else:
                skipped += 1
        
        print("\n" + "=" * 60)
        print(f"[OK] Results: {added} added, {skipped} skipped (duplicates)")
        print("=" * 60)
        self.pause()


def display_menu():
    """Display the enhanced menu"""
    print("\n" + "="*60)
    print("QUOTES MANAGER")
    print("="*60)
    print("  BASIC OPERATIONS:")
    print("  1. Add single quote")
    print("  2. Add multiple quotes (one line per quote)")
    print("  3. Show all quotes")
    print("  4. Random quote")
    print("  5. Delete quote by ID")
    
    print("\n  SEARCH & FAVORITES:")
    print("  6. Search quotes")
    print("  7. Add to favorites")
    print("  8. Remove from favorites")
    print("  9. Show favorites")
    
    print("\n  DATA MANAGEMENT:")
    print("  10. Statistics")
    print("  11. Export quotes")
    print("  12. Import quotes")
    print("  13. Backup database")
    print("  14. Exit")
    print("="*60)


def is_db_empty(db_name: str) -> bool:
    """Check if the database is empty (no quotes)"""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # First, check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quotes'")
            if not cursor.fetchone():
                return True
            cursor.execute('SELECT COUNT(*) FROM quotes')
            return cursor.fetchone()[0] == 0
    except sqlite3.Error:
        return True  # Assume empty if error (e.g., DB doesn't exist)


# Global functions for startup
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(message="Press Enter to continue..."):
    print(f"\n{message}")
    if os.name == 'nt':
        msvcrt.getch()
    else:
        input()

def initialize_from_myquotes():
    """Global version for startup"""
    try:
        if os.path.exists('MYQuotes.py'):
            print("Running MYQuotes.py...")
            print("It will populate the database. Wait for it to finish.")
            import subprocess
            subprocess.call([sys.executable, 'MYQuotes.py'])
            print("\nMYQuotes.py finished. Database should now be populated.")
            return True
        else:
            print("[X] MYQuotes.py file not found!")
            print("Please ensure MYQuotes.py is in the same directory.")
            return False
    except Exception as e:
        print(f"[X] Error running MYQuotes.py: {e}")
        return False


def main():
    """Main menu system"""
    db_name = "quotes.db"
    empty = is_db_empty(db_name)
    
    qm = None
    if not empty:
        qm = QuotesManager(db_name)
    else:
        clear_screen()
        print("\nDatabase is empty!")
        print("Choose an option to get started:")
        print("1. Import quotes from a file (JSON/CSV)")
        print("2. Start adding quotes manually")
        print("3. Run MYQuotes.py to populate database")
        
        choice = input("\nChoose (1/2/3): ").strip()
        
        if choice == '3':
            clear_screen()
            success = initialize_from_myquotes()
            if success:
                print("\nMYQuotes.py completed successfully! Entering main menu...")
            else:
                print("\nMYQuotes.py failed or not found. You can try again or add quotes manually.")
            pause()
            qm = QuotesManager(db_name)
        else:
            qm = QuotesManager(db_name)
            if choice == '1':
                clear_screen()
                print("\nIMPORT FROM FILE")
                print("Supported formats: .json, .csv")
                filename = input("Enter file path: ").strip()
                filename = filename.strip('"').strip("'")
                if filename:
                    qm.import_quotes(filename)
                else:
                    print("[X] No file path provided!")
                    qm.pause()
            # For choice 2, just proceed to menu
    
    # Now qm is created, enter main menu loop
    while True:
        qm.clear_screen()
        display_menu()
        choice = input("Choose an option (1-14): ").strip()
        
        if choice == '1':
            qm.clear_screen()
            print("\nADD NEW QUOTE")
            print("-" * 50)
            quote = input("Quote text: ").strip()
            if quote:
                author = input("Author (Enter for 'Unknown'): ").strip() or "Unknown"
                category = input("Category (Enter for 'General'): ").strip() or "General"
                tags = input("Tags (comma-separated, optional): ").strip()
                source = input("Source (optional): ").strip()
                year_str = input("Year (optional): ").strip()
                year = int(year_str) if year_str.isdigit() else None
                
                qm.add_quote(quote, author, category, tags, source, year)
                time.sleep(2)
            else:
                print("[X] Quote cannot be empty!")
                time.sleep(2)
        
        elif choice == '2':
            qm.add_multiple_quotes()
        
        elif choice == '3':
            qm.clear_screen()
            print("\nVIEW QUOTES")
            print("-" * 50)
            limit_str = input("Show how many? (Enter for all): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else None
            show_stats = input("Show statistics? (y/N): ").lower() == 'y'
            qm.clear_screen()
            qm.show_all_quotes(limit, show_stats)
        
        elif choice == '4':
            qm.clear_screen()
            print("\nRANDOM QUOTE")
            category = input("Filter by category? (Enter for any): ").strip()
            qm.clear_screen()
            qm.get_random_quote(category if category else None)
        
        elif choice == '5':
            try:
                qm.clear_screen()
                quote_id = int(input("\nEnter quote ID to delete: "))
                qm.delete_quote(quote_id)
            except ValueError:
                print("[X] Please enter a valid number!")
                time.sleep(2)
        
        elif choice == '6':
            qm.clear_screen()
            print("\nSEARCH QUOTES")
            print("-" * 50)
            search_term = input("What are you looking for? (keyword/phrase): ").strip()
            if search_term:
                print("\nWhere to search?")
                print("1) All fields")
                print("2) Quote text only")
                print("3) Author names only")
                print("4) Categories only")
                search_choice = input("\nChoose (1-4): ").strip()
                search_map = {'1': 'all', '2': 'text', '3': 'author', '4': 'category'}
                search_in = search_map.get(search_choice, 'all')
                
                qm.clear_screen()
                results = qm.search_quotes(search_term, search_in)
                if results:
                    print(f"\nFound {len(results)} matching quotes:")
                    print("-" * 75)
                    for quote_id, text, author, category, favorite in results:
                        fav = "[*]" if favorite else "   "
                        print(f"{fav} #{quote_id} {text}")
                        print(f"      Author: {author}")
                        print(f"      Category: {category}")
                        print()
                else:
                    print(f"[X] No quotes found matching '{search_term}'")
                qm.pause()
        
        elif choice == '7':
            try:
                qm.clear_screen()
                quote_id = int(input("\nEnter quote ID to ADD to favorites: "))
                qm.add_remove_favorite(quote_id, "add")
            except ValueError:
                print("[X] Please enter a valid number!")
                time.sleep(2)
        
        elif choice == '8':
            try:
                qm.clear_screen()
                quote_id = int(input("\nEnter quote ID to REMOVE from favorites: "))
                qm.add_remove_favorite(quote_id, "remove")
            except ValueError:
                print("[X] Please enter a valid number!")
                time.sleep(2)
        
        elif choice == '9':
            qm.clear_screen()
            qm.show_favorites()
        
        elif choice == '10':
            qm.clear_screen()
            qm.get_statistics()
        
        elif choice == '11':
            qm.clear_screen()
            print("\nEXPORT QUOTES")
            format_choice = input("Export format (json/csv): ").lower()
            if format_choice in ['json', 'csv']:
                filename = input(f"Filename (Enter for auto): ").strip()
                qm.export_quotes(format_choice, filename if filename else None)
            else:
                print("[X] Invalid format! Choose 'json' or 'csv'")
                qm.pause()
        
        elif choice == '12':
            qm.clear_screen()
            print("\nIMPORT QUOTES")
            filename = input("Enter file path: ").strip()
            filename = filename.strip('"').strip("'")
            if filename:
                qm.import_quotes(filename)
            else:
                print("[X] Filename required!")
                qm.pause()
        
        elif choice == '13':
            qm.clear_screen()
            print("\nBACKUP DATABASE")
            backup_name = input("Backup filename (Enter for auto): ").strip()
            qm.backup_database(backup_name if backup_name else None)
        
        elif choice == '14':
            qm.clear_screen()
            print("\nThank you for using Quotes Manager!")
            print("Your wisdom has been preserved. Until next time!")
            break
        
        else:
            print("[X] Invalid choice! Please choose 1-14.")
            time.sleep(2)


if __name__ == "__main__":
    main()