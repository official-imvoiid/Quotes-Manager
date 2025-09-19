import sqlite3
import os

def initialize_database(mode):
    """Initialize the quotes database with all quotes"""
    
    # Create or connect to database
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    
    print("Initializing Quotes Database...")
    
    # Create table with all fields
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
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_author ON quotes(author)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON quotes(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_favorite ON quotes(favorite)')
    
    # For option 1, create empty database structure only
    if mode == 1:
        conn.commit()
        cursor.execute('SELECT COUNT(*) FROM quotes')
        total = cursor.fetchone()[0]
        conn.close()
        
        print("\n" + "="*60)
        print("EMPTY DATABASE CREATED!")
        print("="*60)
        print("Database structure created with 0 quotes.")
        print("You can now add quotes manually through QuotesManager.")
        print("="*60)
        return 0
    
    # For option 2, clear ALL existing quotes and reset the auto-increment
    if mode == 2:
        cursor.execute('DROP TABLE IF EXISTS quotes')
        conn.commit()
        
        # Recreate the table fresh
        cursor.execute('''
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
            )
        ''')
        
        # Recreate indexes
        cursor.execute('CREATE INDEX idx_author ON quotes(author)')
        cursor.execute('CREATE INDEX idx_category ON quotes(category)')
        cursor.execute('CREATE INDEX idx_favorite ON quotes(favorite)')
        
        print("Cleared ALL existing quotes. Adding only your quotes...")
    # All quotes collection
    quotes_data = [
        # Original Dark/Personal Collection
        ("If your why is strong enough, how becomes easy.", "Unknown", "Motivation", "purpose,strength"),
        ("Let it hurt until it hurts no more.", "Unknown", "Resilience", "pain,healing"),
        ("Everything remains, yet nothing is the same.", "Unknown", "Philosophy", "change,time"),
        ("We are just like the moon, bright but always alone.", "Unknown", "Solitude", "loneliness,beauty"),
        ("The rain stopped, but we never found our way back.", "Unknown", "Loss", "memory,past"),
        ("Raindrops on the coffin, like nature saying farewell.", "Unknown", "Death", "nature,grief"),
        ("When you're too numb to cry, the sky does it for you.", "Unknown", "Grief", "pain,nature"),
        ("She left with the storm—quiet, sudden, and gone.", "Unknown", "Loss", "departure,memory"),
        ("Never stop protecting, save what's left.", "Unknown", "Resilience", "protection,strength"),
        ("It's in the eyes that the truth of someone lives.", "Unknown", "Truth", "perception,authenticity"),
        ("Fight for what matters for it is your true light.", "Unknown", "Purpose", "passion,meaning"),
        ("It stayed with me in the dark, so I'll keep it in the light.", "Unknown", "Loyalty", "gratitude,memory"),
        ("Some stories are born of tragedy, written by the unlucky who lost their love and themselves.", "Unknown", "Tragedy", "loss,story"),
        ("Humans are tragic art, rotting on the walls of time.", "Unknown", "Philosophy", "existence,time"),
        ("Maybe I grew older... or maybe I simply died.", "Unknown", "Change", "aging,transformation"),
        ("The strongest pain comes from what you love most.", "Unknown", "Love", "pain,attachment"),
        ("Sometimes I feel like shooting myself, other times, the people.", "Unknown", "Dark", "anger,pain"),
        ("You die a thousand times before life truly begins.", "Unknown", "Transformation", "rebirth,growth"),
        ("The deepest pain comes from what you love the most.", "Unknown", "Love", "attachment,suffering"),
        ("I smile so no one sees I'm already gone.", "Unknown", "Masks", "depression,facade"),
        ("I choose pain over peace, just to become her hero.", "Unknown", "Sacrifice", "love,heroism"),
        ("To be what I'm not, I had to bury myself alive.", "Unknown", "Identity", "transformation,sacrifice"),
        ("What I became was born from my own funeral.", "Unknown", "Transformation", "rebirth,death"),
        ("It hurts to die into someone you're not.", "Unknown", "Identity", "authenticity,pain"),
        ("Why should I fear death when death was the only person kind with me.", "Unknown", "Death", "acceptance,kindness"),
        ("The tragedy of fate is it steals what you love the most.", "Unknown", "Fate", "loss,tragedy"),
        ("Time is the greatest teacher; but unfortunately it kills its own pupils.", "Hector Berlioz", "Time", "wisdom,mortality"),
        ("What we want most is often never ours.", "Unknown", "Desire", "longing,acceptance"),
        ("Sometimes, the hardest thing is letting go of what you wanted.", "Unknown", "Acceptance", "release,growth"),
        ("The past will always haunt, but you can choose to run or face it.", "Unknown", "Past", "courage,memory"),
        ("You only love once—second time, the heart turns cold.", "Unknown", "Love", "first love,heartbreak"),
        ("When a child can't find home in light, he makes darkness home.", "Unknown", "Belonging", "childhood,darkness"),
        ("Lies are comfort, until they start to suffocate you.", "Unknown", "Truth", "deception,reality"),
        ("Humans are designed to create. That's why you get depressed when all you do is consume.", "Unknown", "Purpose", "creativity,meaning"),
        ("Accept people as they are but place them where they belong.", "Unknown", "Relationships", "boundaries,acceptance"),
        ("You spend your life gathering guests for your funeral.", "Unknown", "Life", "relationships,mortality"),
        ("Some storms break trees. Some break people.", "Unknown", "Adversity", "resilience,breaking"),
        ("They said storms pass—but some stay inside you.", "Unknown", "Trauma", "healing,pain"),
        ("No one notices when you're crying in the rain—or in life.", "Unknown", "Isolation", "invisibility,pain"),
        ("I don't cry anymore. I let the sky do it for me.", "Unknown", "Grief", "nature,numbness"),
        ("I watch the rain like I watch my life—falling, and can't stop it.", "Unknown", "Helplessness", "rain,control"),
        ("I can't tell if the rain makes me feel alive or empty.", "Unknown", "Ambivalence", "rain,emotion"),
        ("The cold rain is a reminder—nothing ever stays warm for long.", "Unknown", "Impermanence", "rain,cold"),
        ("Even the sky knows—sometimes it's better to break than to hold it in.", "Unknown", "Release", "rain,emotion"),
        ("Life's like rain—some run, some dance. You choose.", "Unknown", "Choice", "rain,attitude"),
        ("I expected little too much so life gifted me reality", "Unknown", "Expectations", "disappointment,reality"),
        ("Nothing is permanent in this world, people you love most will one day leave you either by tragedy or choice", "Unknown", "Impermanence", "loss,change"),
        ("When you stay with something long enough you start loving it, even tragedy", "Unknown", "Adaptation", "attachment,suffering"),
        ("Wisdom is the reward for surviving hell.", "Unknown", "Wisdom", "suffering,growth"),
        ("Time is greatest teacher; but sadly, it kills its own pupils", "Hector Berlioz", "Time", "wisdom,mortality"),
        ("Love was my sweetest sin, now it's my greatest regret", "Unknown", "Love", "regret,past"),
        ("Betrayal is the sharpest weapon, for it wounds the soul.", "Unknown", "Betrayal", "trust,pain"),
        ("Blood is the ink with which history is written.", "Unknown", "History", "violence,legacy"),
        ("She loved the rain; So when she died, it Never stopped.", "Unknown", "Loss", "rain,grief"),
        ("Rain soaked my jacket, but it couldn't reach the part of her", "Unknown", "Memory", "rain,loss"),
        ("Monsters aren't always scary- some just look like you at 3am", "Unknown", "Self", "darkness,reflection"),
        ("Freedom comes at a cost. Cost of everything.", "Unknown", "Freedom", "sacrifice,price"),
        ("Love is fire, but whether it will warm or burn, no one knows", "Unknown", "Love", "risk,uncertainty"),
        ("Price of Anything is the Amount of life you exchange for it.", "Henry David Thoreau", "Value", "time,cost"),
        ("Solitude births a demon or breaks a brittle man.", "Unknown", "Solitude", "transformation,isolation"),
        ("In saving others, we destroyed ourselves.", "Unknown", "Sacrifice", "heroism,cost"),
        ("You fear monsters. They fear becoming human.", "Unknown", "Humanity", "monsters,fear"),
        ("The dead don't haunt us. It's our memory that does.", "Unknown", "Memory", "grief,past"),
        ("You don't miss them--you miss who you were with them", "Unknown", "Loss", "identity,relationships"),
        ("People grow stronger only when they have something to protect", "Unknown", "Strength", "purpose,protection"),
        ("Thoughts too cruel for hell dwell in my head", "Unknown", "Dark", "thoughts,suffering"),
        ("And dangerous of them all is the memory that never fades.", "Unknown", "Memory", "danger,past"),
        ("Pain teaches you to love the things that break you", "Unknown", "Pain", "attachment,trauma"),
        ("It's not others' thoughts; It's your effort that defines you", "Unknown", "Identity", "effort,opinion"),
        ("Die for your passion, and regret won't haunt your grave.", "Unknown", "Purpose", "passion,regret"),
        ("Your battle is for what you love, not for what world loves", "Unknown", "Purpose", "authenticity,passion"),
        ("If you're there for you, no one else matters", "Unknown", "Self-reliance", "independence,strength"),
        ("Its your refusal to go insane that holds you back not talent", "Unknown", "Sanity", "limitations,madness"),
        ("Life without purpose is easy. That's why it feels empty", "Unknown", "Purpose", "meaning,emptiness"),
        ("Who you were must die for who you must become", "Unknown", "Transformation", "growth,sacrifice"),
        ("Sometimes we wish for the past, but it's already long gone.", "Unknown", "Nostalgia", "past,longing"),
        ("You only matter as much as what you can provide", "Unknown", "Value", "utility,worth"),
        
        # Additional quotes
        ("A Reason for living is often a reason to die", "Unknown", "Purpose", "life,death,meaning"),
        ("Life's gift is time; Its curse is taking it back.", "Unknown", "Time", "mortality,gift"),
        ("you need oceans of hate to finally drown in void of silence", "Unknown", "Dark", "hate,silence"),
        ("Be So Obsessed-Sacrifice Life, Youth, and soul to get it", "Unknown", "Obsession", "sacrifice,dedication"),
        ("To reach anything high, Be obsessed to the point of madness", "Unknown", "Obsession", "success,madness"),
        ("To change society, one must start with themselves.", "Unknown", "Change", "self-improvement,society"),
        ("with \"WILL\" alone, you can change the course of destiny", "Unknown", "Determination", "will,destiny"),
        ("The hardest part is starting; The rest becomes easy.", "Unknown", "Beginning", "action,momentum"),
        ("I see faces shaped like humans but hearts shaped like knives.", "Unknown", "Humanity", "deception,cruelty"),
        ("Some grow rich in gold, but remain poor in heart-thats there misery.", "Unknown", "Wealth", "materialism,emptiness"),
        ("some live a hundred years without living a day", "Unknown", "Life", "existence,meaning"),
        ("growth is the process of dying many times untill you rise to your best self", "Unknown", "Growth", "transformation,death"),
        ("Saying \"YES\" to everyone is to say \"NO\" to your inner peace", "Unknown", "Boundaries", "peace,people-pleasing"),
        ("it rains hardest on the people that deserve sunshine the most", "Unknown", "Injustice", "rain,unfairness"),
        ("every business is legal if you have political support", "Unknown", "Politics", "corruption,business"),
        ("hate always come from below, not above", "Unknown", "Hate", "envy,hierarchy"),
        ("if you can dream it, you can do it", "Walt Disney", "Motivation", "dreams,achievement"),
        ("to be trusted is greater compliment than being loved", "George MacDonald", "Trust", "respect,love"),
        ("you can be depressed and can still get the work done, its called being a man", "Unknown", "Masculinity", "depression,duty"),
        ("A child who spent life in darkness finds no solace in light", "Unknown", "Darkness", "childhood,adaptation"),
        ("past will be carried forever but it wont chain your future", "Unknown", "Past", "future,freedom"),
        ("the only journey that feels impossible. is the one you refuse to start", "Unknown", "Beginning", "fear,action"),
        ("its on you to get where you want to be", "Unknown", "Responsibility", "self-reliance,goals"),
        ("he who lost all hope also lost all fear", "Unknown", "Hope", "fear,loss"),
        ("maturity is when you realize, Mard ki khubsurati paisa hai", "Unknown", "Reality", "maturity,money"),
        ("never asked for help but i remember all who offered forever", "Unknown", "Gratitude", "help,memory"),
        ("Dear Fear not the Dark but rather light, people and memories", "Unknown", "Fear", "darkness,light"),
        ("Darling Night is beautiful yet full of hidden demons like-us", "Unknown", "Night", "darkness,humanity"),
        ("Horses that go in war, Never dances in wedding", "Unknown", "War", "transformation,purpose"),
        ("Death is terrible for anyone. Young or old, good or evil, it's all the same. Death is impartial.", "Unknown", "Death", "equality,mortality"),
        ("Everything eventually faces destruction. Everything eventually disappears.", "Unknown", "Impermanence", "destruction,time"),
        ("You can be human and still be a monster; You can be a monster and still be human", "Unknown", "Humanity", "duality,nature"),
        ("Nothing lasts; all that exists sinks into time's abyss", "Unknown", "Time", "impermanence,void"),
        ("There is humanity in monsters, and monstrosity in men.", "Unknown", "Humanity", "duality,nature"),
        ("It doesn't matter who you are. The silence finds you all.", "Unknown", "Death", "equality,silence"),
        
        # New quotes to add
        ("The night was young, but I was already old.", "Unknown", "Time", "age,night,weariness"),
        ("The more you care for someone, the more they will hurt you.", "Unknown", "Love", "vulnerability,pain"),
        ("To get what you love, be patient with what you hate.", "Unknown", "Patience", "endurance,reward"),
        ("The world is not for the good ones, but for those who play it well.", "Unknown", "Reality", "survival,strategy"),
        ("Sometimes, silence protects you from the problems that words may invite.", "Unknown", "Wisdom", "silence,protection"),
        ("Obsession and discipline crush talent every time.", "Unknown", "Success", "discipline,obsession"),
        ("Beneath the sweetness, it is decay. That is why it is beautiful.", "Unknown", "Beauty", "decay,duality"),
        ("Our scars have the power to remind us that the past was real.", "Unknown", "Scars", "past,memory"),
        ("Cruelty is a gift humanity has given itself.", "Unknown", "Humanity", "cruelty,nature"),
        ("Learn to tell no one anything—and all will go well.", "Unknown", "Wisdom", "silence,privacy"),
        ("We run from ourselves in the hopes of finding ourself. What kind of irony is this?", "Unknown", "Identity", "irony,search"),
        ("If you trust too much, betrayal is your fault.", "Unknown", "Trust", "betrayal,responsibility"),
        ("Your life is your story, make sure to give it a beautiful ending.", "Unknown", "Life", "story,ending"),
        ("Truth is poison for people who live in their own imagination.", "Unknown", "Truth", "reality,delusion"),
        ("The more awake you are, the less human contact matters.", "Unknown", "Awakening", "solitude,consciousness"),
        ("In her glow, he saw the beauty of what was, and the pain of what could never be again.", "Unknown", "Loss", "memory,beauty"),
        ("Then it passed, like all things do.", "Unknown", "Impermanence", "time,passing"),
        ("Death is certain, life is not.", "Unknown", "Death", "certainty,life"),
        ("If a goodbye hurts, it means you've spent your time well.", "Unknown", "Farewell", "goodbye,meaning"),
        ("Nothing is heavier than a thought you forgot to forget.", "Unknown", "Memory", "thoughts,burden"),
        ("Every human wears two skins: silk and sin.", "Unknown", "Humanity", "duality,facade"),
        ("If I stand with you, I fall with you—that's my way of loyalty.", "Unknown", "Loyalty", "sacrifice,commitment"),
        ("I am alive, and what greater punishment could there be?", "Unknown", "Existence", "suffering,life"),
        ("Peace begins within you. Trust yourself and let go.", "Unknown", "Peace", "inner-peace,trust"),
        
        # Classic Philosophy
        ("The unexamined life is not worth living.", "Socrates", "Philosophy", "self-awareness,meaning"),
        ("I think, therefore I am.", "René Descartes", "Philosophy", "existence,consciousness"),
        ("Hell is other people.", "Jean-Paul Sartre", "Philosophy", "relationships,existentialism"),
        ("Man is condemned to be free.", "Jean-Paul Sartre", "Philosophy", "freedom,responsibility"),
        ("God is dead. God remains dead. And we have killed him.", "Friedrich Nietzsche", "Philosophy", "religion,meaning"),
        ("What doesn't kill you makes you stronger.", "Friedrich Nietzsche", "Resilience", "strength,adversity"),
        ("He who has a why to live can bear almost any how.", "Friedrich Nietzsche", "Purpose", "meaning,endurance"),
        ("The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.", "Albert Camus", "Freedom", "rebellion,authenticity"),
        ("In the depth of winter, I finally learned that there was in me an invincible summer.", "Albert Camus", "Resilience", "strength,hope"),
        ("The struggle itself toward the heights is enough to fill a man's heart.", "Albert Camus", "Purpose", "struggle,meaning"),
        
        # Stoicism
        ("You have power over your mind—not outside events. Realize this, and you will find strength.", "Marcus Aurelius", "Stoicism", "control,strength"),
        ("The best revenge is not to be like your enemy.", "Marcus Aurelius", "Stoicism", "integrity,revenge"),
        ("What we cannot bear removes us from life; what remains can be borne.", "Marcus Aurelius", "Stoicism", "endurance,suffering"),
        ("The universe is change; our life is what our thoughts make it.", "Marcus Aurelius", "Stoicism", "perception,change"),
        ("It is not death that a man should fear, but never beginning to live.", "Marcus Aurelius", "Life", "death,living"),
        ("Wealth consists not in having great possessions, but in having few wants.", "Epictetus", "Stoicism", "contentment,desire"),
        ("No man is free who is not master of himself.", "Epictetus", "Freedom", "self-control,discipline"),
        ("We suffer more often in imagination than in reality.", "Seneca", "Stoicism", "anxiety,perception"),
        ("Every new beginning comes from some other beginning's end.", "Seneca", "Change", "endings,beginnings"),
        ("It is the power of the mind to be unconquerable.", "Seneca", "Stoicism", "mind,strength"),
        
        # Eastern Philosophy
        ("The flame that burns twice as bright burns half as long.", "Lao Tzu", "Taoism", "intensity,duration"),
        ("When I let go of what I am, I become what I might be.", "Lao Tzu", "Transformation", "letting go,potential"),
        ("The journey of a thousand miles begins with a single step.", "Lao Tzu", "Action", "beginning,journey"),
        ("Those who know do not speak. Those who speak do not know.", "Lao Tzu", "Wisdom", "silence,knowledge"),
        ("Empty your mind, be formless, shapeless, like water.", "Bruce Lee", "Adaptability", "flexibility,zen"),
        ("The mind is everything. What you think you become.", "Buddha", "Buddhism", "mind,transformation"),
        ("Three things cannot be long hidden: the sun, the moon, and the truth.", "Buddha", "Truth", "inevitability,revelation"),
        ("Pain is inevitable. Suffering is optional.", "Buddhist Saying", "Buddhism", "pain,choice"),
        ("The wound is the place where the Light enters you.", "Rumi", "Spirituality", "pain,growth"),
        ("Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself.", "Rumi", "Wisdom", "change,growth"),
        
        # Psychology & Shadow Work
        ("Everything that irritates us about others can lead us to an understanding of ourselves.", "Carl Jung", "Psychology", "projection,self-awareness"),
        ("Until you make the unconscious conscious, it will direct your life and you will call it fate.", "Carl Jung", "Psychology", "awareness,unconscious"),
        ("The most terrifying thing is to accept oneself completely.", "Carl Jung", "Self-acceptance", "fear,authenticity"),
        ("People will do anything, no matter how absurd, to avoid facing their own souls.", "Carl Jung", "Avoidance", "soul,denial"),
        ("Knowing your own darkness is the best method for dealing with the darknesses of other people.", "Carl Jung", "Shadow", "self-knowledge,understanding"),
        ("The privilege of a lifetime is to become who you truly are.", "Carl Jung", "Authenticity", "identity,privilege"),
        ("We cannot change anything until we accept it.", "Carl Jung", "Acceptance", "change,psychology"),
        ("Your vision will become clear only when you can look into your own heart.", "Carl Jung", "Clarity", "introspection,vision"),
        ("Show me a sane man and I will cure him for you.", "Carl Jung", "Sanity", "psychology,normalcy"),
    ]
    
    # Insert all quotes
    inserted = 0
    skipped = 0
    
    # Skip inserting quotes for mode 1 (empty database)
    if mode != 1:
        for quote_data in quotes_data:
            try:
                cursor.execute('''
                    INSERT INTO quotes (quote_text, author, category, tags)
                    VALUES (?, ?, ?, ?)
                ''', quote_data)
                inserted += 1
            except sqlite3.IntegrityError:
                # Quote already exists (duplicate)
                skipped += 1
    
    # REMOVED: No automatic favorite marking
    # All quotes start with favorite = 0 (false)
    
    conn.commit()
    
    # Show summary
    cursor.execute('SELECT COUNT(*) FROM quotes')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT category) FROM quotes')
    categories = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT author) FROM quotes WHERE author != "Unknown"')
    authors = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM quotes WHERE favorite = 1')
    favorites = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n" + "="*60)
    print("DATABASE INITIALIZATION COMPLETE!")
    print("="*60)
    print(f"Total Quotes: {total}")
    print(f"Newly Added: {inserted}")
    print(f"Skipped (duplicates): {skipped}")
    print(f"Categories: {categories}")
    print(f"Known Authors: {authors}")
    print(f"Favorites Marked: {favorites}")
    print("="*60)
    
    return total

def main():
    """Main function to initialize database"""
    print("="*60)
    print("QUOTES DATABASE INITIALIZER")
    print("="*60)
    
    # Check if database already exists
    db_exists = os.path.exists('quotes.db')
    
    if db_exists:
        print("\nDatabase 'quotes.db' already exists!")
        print("Options:")
        print("1. Delete and create EMPTY database (structure only)")
        print("2. Use My quotes database (clear existing and add my quotes)")
        print("3. Merge current database with my quotes (keep existing, add new)")
        
        choice = input("\nChoose (1/2/3): ").strip()
        
        if choice == '1':
            os.remove('quotes.db')
            print("Old database deleted. Creating empty database...")
            mode = 1
        elif choice == '2':
            mode = 2
        elif choice == '3':
            mode = 3
        else:
            print("Invalid choice. Using option 3 (Merge).")
            mode = 3
    else:
        print("\nNo existing database found.")
        print("Options:")
        print("1. Create EMPTY database (structure only)")
        print("2. Create database with My quotes")
        
        choice = input("\nChoose (1/2): ").strip()
        
        if choice == '1':
            mode = 1
        else:
            mode = 2  # Default to adding quotes if no existing database
    
    # Initialize database
    total = initialize_database(mode)
    
    if mode == 1:
        print("\nEmpty database structure created!")
        print("Run 'python QuotesManager.py' to start adding quotes.")
    elif total > 0:
        print("\nYour quotes collection is ready!")
        print("Run 'python QuotesManager.py' to start using it.")
    else:
        print("\nNo quotes were added. Something went wrong.")

if __name__ == "__main__":
    main()