# Day 2: Building the News Entity Extractor
## Complete 50-Minute Lesson Plan with Teacher Script

---

## **Pre-Class Setup (5 minutes before class)**

### **Materials Checklist:**
- [ ] Student computers with spaCy installed (test on teacher machine)
- [ ] Create folder on each computer: `ner_project`
- [ ] Sample news articles saved as `.txt` files
- [ ] Code editor open (VS Code recommended)
- [ ] Project starter template ready
- [ ] Handout: "Project Building Checklist"

### **Files to Create Before Class:**
```
news_article1.txt - Technology article
news_article2.txt - Sports article  
news_article3.txt - Politics article
starter_code.py - Template for students
```

### **Slide Deck Setup:**
- Slide 1: "Welcome Back, NER Detectives!"
- Slide 2: Project goals overview
- Slide 3: Step-by-step building plan
- Slide 4: Code structure diagram
- Slide 5: File handling demo
- Slide 6: Entity organization concept

---

## **MINUTE-BY-MINUTE LESSON BREAKDOWN**

### **Opening & Homework Review (0:00-0:10)**

**[Teacher enters with enthusiasm, displays Slide 1]**

**Teacher:** "Welcome back, NER detectives! Yesterday you became entity identification experts, and today we're building something awesome - a program that can analyze entire news articles automatically!"

**Teacher:** "First, let's see what you discovered for homework. Who found an interesting article and tried to identify entities manually?"

**[Allow 2-3 students to share - 2 minutes total]**

**Student Sharing Prompts:**
- "What article did you choose and why?"
- "What was the most interesting entity you found?"
- "Were there any entities you weren't sure how to classify?"

**Teacher:** "Excellent! I heard some great examples. Now, what if I told you that by the end of today, your computer will be able to read your articles and find ALL those entities in about 2 seconds? Let's build that program!"

**Quick Review Questions:**
**Teacher:** "Before we code, let's do a lightning round review. I'll say an entity, you shout out the type:"

- "Barack Obama" → **PERSON**
- "Microsoft" → **ORG** 
- "Chicago" → **GPE**
- "$50 million" → **MONEY**
- "next Tuesday" → **DATE**

**Teacher:** "Perfect! Your NER knowledge is solid. Now let's put it to work!"

---

### **Project Introduction & Goals (0:10-0:15)**

**[Display Slide 2: Project Goals]**

**Teacher:** "Today we're building the **News Entity Extractor 3000** - okay, maybe not the catchiest name, but it's going to be powerful! Here's what our program will do:"

**Project Features We're Building Today:**
1. **Read news articles from text files** (no more copy-pasting!)
2. **Extract and identify all entities** using spaCy
3. **Organize results by entity type** (all people together, all places together, etc.)
4. **Count how often each entity appears** (is this article mostly about one person?)
5. **Display results in a beautiful, readable format**

**Teacher:** "Think about it - news organizations probably have programs exactly like this to automatically tag and organize thousands of articles every day!"

**[Display Slide 3: Building Plan]**

**Teacher:** "We're going to build this step-by-step, like constructing a house. You don't start with the roof - you start with the foundation!"

**Our Building Steps:**
1. **Step 1**: Create our basic entity extraction function
2. **Step 2**: Add file reading capability  
3. **Step 3**: Organize entities by type and count them
4. **Step 4**: Make beautiful output formatting
5. **Step 5**: Test with real news articles

**Teacher:** "Everyone ready to code? Let's start building!"

---

### **Step 1: Basic Entity Extraction Function (0:15-0:25)**

**Teacher:** "First, we need to upgrade yesterday's basic code into a proper function. Open your code editor and create a new file called `news_analyzer.py`"

**[Project code on screen, type along with students]**

```python
import spacy
from collections import Counter

def extract_entities(text):
    """
    Extract entities from text using spaCy
    This is our core function - the brain of our program!
    """
    # Load our smart NER model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the text
    doc = nlp(text)
    
    # Create a list to store our findings
    entities = []
    
    # Go through each entity spaCy found
    for ent in doc.ents:
        entities.append({
            'text': ent.text,           # The actual entity (like "Barack Obama")
            'label': ent.label_,        # The type (like "PERSON")
            'description': spacy.explain(ent.label_)  # Human-readable description
        })
    
    return entities

# Let's test it with some text!
sample_article = """
President Biden met with European leaders in Brussels yesterday. 
The meeting, held at NATO headquarters, focused on Ukraine and 
climate change. Apple Inc. announced a $2 billion investment 
in renewable energy projects across California and Texas.
"""

print("Testing our entity extractor...")
entities = extract_entities(sample_article)

for entity in entities:
    print(f"Found: '{entity['text']}' ({entity['label']}) - {entity['description']}")
```

**Teacher:** "Let's run this together - everyone type this code and run it!"

**[Walk around helping students - expect 3-4 minutes for typing and running]**

**Expected Output:**
```
Testing our entity extractor...
Found: 'Biden' (PERSON) - People, including fictional
Found: 'European' (NORP) - Nationalities or religious or political groups
Found: 'Brussels' (GPE) - Countries, cities, states
Found: 'yesterday' (DATE) - Absolute or relative dates or periods
Found: 'NATO' (ORG) - Companies, agencies, institutions
Found: 'Ukraine' (GPE) - Countries, cities, states
Found: 'Apple Inc.' (ORG) - Companies, agencies, institutions
Found: '$2 billion' (MONEY) - Monetary values, including unit
Found: 'California' (GPE) - Countries, cities, states
Found: 'Texas' (GPE) - Countries, cities, states
```

**Teacher:** "Wow! Look at all the entities our function found! Notice how spaCy even identified 'European' as NORP - that's 'Nationalities or Religious/Political groups'. It's incredibly smart!"

**Quick Check:** "Everyone got output similar to this? Raise your hand if you see entities being extracted!"

---

### **Step 2: Reading Articles from Files (0:25-0:32)**

**Teacher:** "Great! Now instead of having text hard-coded in our program, let's make it read articles from files. This way we can analyze any article just by putting it in a text file!"

**[Add to existing code]**

```python
def read_article(filename):
    """
    Read article content from a text file
    Returns the text if successful, None if there's an error
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"Successfully loaded article from {filename}")
            print(f"Article length: {len(content.split())} words")
            return content
    except FileNotFoundError:
        print(f"Oops! File '{filename}' not found!")
        print("Make sure the file exists and the name is spelled correctly.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Let's test reading a file
print("\n" + "="*50)
print("TESTING FILE READING")
print("="*50)

# First, let's create a test file
test_article = """
Tesla CEO Elon Musk announced yesterday that the company will build 
a new Gigafactory in Austin, Texas. The $5 billion facility will 
create 10,000 jobs and produce batteries for Tesla vehicles. Governor 
Greg Abbott praised the decision, saying it will boost Texas's economy 
by 15% over the next decade. Construction begins in March 2025.
"""

# Save it to a file
with open("test_article.txt", "w") as f:
    f.write(test_article)

# Now read it back
article_content = read_article("test_article.txt")

if article_content:
    print("File reading successful! Now analyzing entities...")
    entities = extract_entities(article_content)
    
    print(f"\nFound {len(entities)} entities:")
    for entity in entities:
        print(f"  • {entity['text']} ({entity['label']})")
```

**Teacher:** "Run this code! What we're doing here is:"
1. **Creating a function** that can read any text file
2. **Adding error handling** so our program doesn't crash if a file doesn't exist
3. **Testing it** by creating a test file and reading it back

**[Students run code - walk around helping]**

**Teacher:** "Everyone see how we can now read articles from files? This means you can take any news article, save it as a .txt file, and our program can analyze it!"

---

### **Step 3: Organizing and Counting Entities (0:32-0:42)**

**Teacher:** "Now comes the really cool part - organizing our entities! Instead of just listing them, let's group them by type and count how many times each entity appears."

**[Add to existing code]**

```python
def organize_entities(entities):
    """
    Organize entities by type and count frequencies
    This makes our results much more useful!
    """
    organized = {}
    
    # Group entities by their label (PERSON, ORG, etc.)
    for entity in entities:
        label = entity['label']
        entity_text = entity['text']
        
        # If this is the first entity of this type, create a new group
        if label not in organized:
            organized[label] = []
        
        # Add the entity to the appropriate group
        organized[label].append(entity_text)
    
    # Now count how many times each entity appears
    for label in organized:
        entity_counts = Counter(organized[label])
        organized[label] = dict(entity_counts)
    
    return organized

def display_results(organized_entities, filename=""):
    """
    Display results in a beautiful, readable format
    """
    print("\n" + "="*60)
    print(f"NEWS ARTICLE ENTITY ANALYSIS")
    if filename:
        print(f"Article: {filename}")
    print("="*60)
    
    # Sort entity types for consistent display
    for label in sorted(organized_entities.keys()):
        entities = organized_entities[label]
        description = spacy.explain(label)
        
        print(f"\n🏷️  {label} ({description}):")
        print("-" * 40)
        
        # Sort entities by frequency (most mentioned first)
        sorted_entities = sorted(entities.items(), key=lambda x: x[1], reverse=True)
        
        for entity, count in sorted_entities:
            if count == 1:
                print(f"   • {entity}")
            else:
                print(f"   • {entity} (mentioned {count} times)")

# Test our new functions!
print("\n" + "="*60)
print("TESTING ENTITY ORGANIZATION")
print("="*60)

if article_content:
    entities = extract_entities(article_content)
    organized = organize_entities(entities)
    display_results(organized, "test_article.txt")
```

**Teacher:** "This is where the magic happens! Run this code and watch our program transform a messy list of entities into a beautifully organized report!"

**[Students run code - allow 2-3 minutes]**

**Expected Output:**
```
🏷️  DATE (Absolute or relative dates or periods):
----------------------------------------
   • yesterday
   • March 2025
   • next decade

🏷️  GPE (Countries, cities, states):
----------------------------------------
   • Texas (mentioned 2 times)
   • Austin

🏷️  MONEY (Monetary values, including unit):
----------------------------------------
   • $5 billion

🏷️  ORG (Companies, agencies, institutions):
----------------------------------------
   • Tesla (mentioned 2 times)

🏷️  PERCENT (Percentage, including "%"):
----------------------------------------
   • 15%

🏷️  PERSON (People, including fictional):
----------------------------------------
   • Elon Musk
   • Greg Abbott
```

**Teacher:** "Look at that! Our program automatically figured out that 'Tesla' was mentioned twice, organized everything by category, and even sorted by frequency. This is exactly what professional news analysis tools do!"

---

### **Step 4: Complete Analysis Function (0:42-0:48)**

**Teacher:** "Let's put it all together into one complete analysis function that we can use on any news article!"

```python
def analyze_article(filename):
    """
    Complete article analysis - this is our main function!
    """
    print(f"\n🔍 Analyzing: {filename}")
    print("="*70)
    
    # Step 1: Read the article
    article_text = read_article(filename)
    if not article_text:
        return None
    
    # Step 2: Basic article stats
    words = article_text.split()
    sentences = article_text.split('.')
    print(f"📊 Article Statistics:")
    print(f"   • Word count: {len(words)}")
    print(f"   • Sentence count: {len(sentences)}")
    
    # Step 3: Extract entities
    print(f"\n🤖 Extracting entities...")
    entities = extract_entities(article_text)
    
    # Step 4: Organize and display
    organized = organize_entities(entities)
    display_results(organized, filename)
    
    # Step 5: Summary statistics
    total_mentions = sum(sum(ents.values()) for ents in organized.values())
    unique_entities = len(entities)
    entity_types = len(organized)
    
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"   • Total entity mentions: {total_mentions}")
    print(f"   • Unique entities found: {unique_entities}")
    print(f"   • Entity types found: {entity_types}")
    
    return organized

# Test our complete analyzer!
print("\n" + "🎉"*20)
print("TESTING COMPLETE ANALYZER")
print("🎉"*20)

result = analyze_article("test_article.txt")
```

**Teacher:** "Run this final version! This is now a professional-quality entity extraction tool!"

**[Students run - walk around celebrating successes]**

---

### **Step 5: Testing with Real Articles (0:48-0:50)**

**Teacher:** "For our final test, let's use the homework articles you brought! Save your article as a .txt file and run our analyzer on it!"

**Instructions for Students:**
1. Copy your homework article text
2. Save it as `my_article.txt` 
3. Run: `analyze_article("my_article.txt")`

**Teacher:** "Who wants to share what entities their program found in their article?"

**[Allow 1-2 quick shares]**

---

### **Wrap-Up and Preview (0:50-0:52)**

**Teacher:** "Incredible work today! You've built a complete news entity extraction system. Tomorrow, we're going to add even cooler features - comparing multiple articles, creating visualizations, and building an interactive tool that lets users analyze articles in real-time!

**Tonight's homework**: Find 2-3 more articles on different topics and test our program on them. Keep notes about:
- What entities does it find really well?
- Are there any entities it misses?
- What's the most interesting pattern you notice?

You're becoming real NLP engineers!"

---

## **TEACHER NOTES & TROUBLESHOOTING**

### **Common Issues & Solutions:**
1. **File not found errors**: Make sure students save files in the same folder as their Python script
2. **Encoding issues**: Some students may need to specify encoding explicitly
3. **spaCy model not loaded**: Check yesterday's installation
4. **Indentation errors**: Python is picky - help students with proper indentation

### **Extension Activities:**
- Challenge advanced students to add other entity types (PRODUCT, EVENT)
- Have them experiment with different news sources
- Try articles in different languages if spaCy models are available

### **Assessment Checkpoints:**
1. Can students successfully run the basic extraction function?
2. Do they understand the file reading concept?
3. Can they explain what the organization function does?
4. Are they excited about testing on real articles?

---

## **MATERIALS TO PREPARE**

### **Sample News Articles (save as .txt files):**

**news_article1.txt (Technology):**
```
Apple Inc. announced record quarterly earnings yesterday, with CEO Tim Cook 
crediting strong iPhone sales in China and India. The Cupertino-based company 
reported revenue of $89.5 billion for Q2 2024. Microsoft and Google also 
reported strong earnings this quarter, with Microsoft's cloud services Azure 
growing by 25% year-over-year. The tech earnings come as the Federal Reserve 
considers interest rate changes next month.
```

**news_article2.txt (Sports):**
```
LeBron James scored 35 points as the Los Angeles Lakers defeated the Boston 
Celtics 112-108 last night at Staples Center. The victory moves the Lakers 
closer to a playoff spot in the Western Conference. James, who turned 39 in 
December, continues to play at an elite level in his 21st NBA season. The 
Lakers will next face the Golden State Warriors in San Francisco on Friday.
```

### **Project Building Checklist (Handout):**
```
NEWS ENTITY EXTRACTOR - BUILDING CHECKLIST

□ Step 1: Basic entity extraction function working
□ Step 2: File reading function working  
□ Step 3: Entity organization and counting working
□ Step 4: Beautiful display formatting working
□ Step 5: Complete analyzer function working
□ Step 6: Successfully tested on real news article

DEBUGGING TIPS:
• File not found? Check spelling and file location
• No entities found? Check if article has enough text
• Program crashing? Check for proper indentation
• Strange results? Try a different article

SUCCESS INDICATORS:
✓ Your program reads articles from files
✓ Entities are organized by type
✓ Counts show how often entities appear
✓ Output is easy to read and understand
```