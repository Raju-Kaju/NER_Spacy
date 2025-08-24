# Named Entity Recognition (NER) Lesson Plan
## Building a News Article Entity Extractor with Python and spaCy

### **Course Information**
- **Subject**: Python Programming / Computer Science
- **Grade Level**: Middle School (6-8) / High School (9-12)
- **Duration**: 3-4 class periods (50 minutes each)
- **Prerequisites**: Basic Python knowledge (variables, functions, loops)

---

## **Learning Objectives**

By the end of this lesson, students will be able to:
1. Explain what Named Entity Recognition (NER) is and why it's useful
2. Install and use the spaCy library in Python
3. Identify different types of entities (PERSON, ORG, GPE, etc.) in text
4. Build a program that extracts entities from news articles
5. Create a simple visualization of extracted entities
6. Understand real-world applications of NER in technology

---

## **Materials Needed**
- Computers with Python 3.7+ installed
- Internet access for package installation
- Code editor (VS Code, PyCharm, or Jupyter Notebooks)
- Sample news articles (provided)
- Project handout

---

## **Lesson Structure**

### **Day 1: Introduction to NER (50 minutes)**

#### **Opening Hook (10 minutes)**
Start with an engaging question: *"How do you think Google News knows which articles are about specific people or places?"*

Show students a news article and ask them to identify:
- People mentioned
- Places mentioned  
- Organizations mentioned
- Dates and times

Explain that computers can do this automatically using NER!

#### **What is Named Entity Recognition? (15 minutes)**

**Definition**: NER is a subtask of information extraction that identifies and classifies named entities in text into predefined categories.

**Common Entity Types**:
- **PERSON**: Names of people (e.g., "Barack Obama", "Taylor Swift")
- **ORG**: Organizations (e.g., "NASA", "Apple Inc.")
- **GPE**: Geopolitical entities - countries, cities, states (e.g., "New York", "Japan")
- **DATE**: Dates and times (e.g., "January 2024", "yesterday")
- **MONEY**: Monetary values (e.g., "$100", "five dollars")
- **PERCENT**: Percentages (e.g., "25%", "half")

**Real-World Applications**:
- News aggregation and categorization
- Social media monitoring
- Content recommendation systems
- Chatbots and virtual assistants
- Financial analysis
- Medical record processing

#### **Introduction to spaCy (15 minutes)**

**What is spaCy?**
- Industrial-strength Natural Language Processing library
- Fast, accurate, and easy to use
- Pre-trained models available for many languages

**Installation Demo**:
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

**Basic spaCy Example**:
```python
import spacy

# Load the English model
nlp = spacy.load("en_core_web_sm")

# Process text
text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
doc = nlp(text)

# Extract entities
for ent in doc.ents:
    print(f"{ent.text} - {ent.label_}")
```

#### **Hands-On Practice (10 minutes)**
Students run the basic example and experiment with their own sentences.

---

### **Day 2: Building the News Entity Extractor (50 minutes)**

#### **Project Introduction (10 minutes)**
**Project Goal**: Build a program that can read news articles and automatically extract all the people, places, organizations, and other entities mentioned.

**Project Features**:
1. Read news articles from text files
2. Extract and categorize entities
3. Display results in a user-friendly format
4. Count entity frequencies
5. Generate a simple report

#### **Step 1: Basic Entity Extraction (15 minutes)**

```python
import spacy
from collections import Counter

def extract_entities(text):
    """Extract entities from text using spaCy"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    entities = []
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'label': ent.label_,
            'description': spacy.explain(ent.label_)
        })
    
    return entities

# Test with sample text
sample_article = """
President Biden met with European leaders in Brussels yesterday. 
The meeting, held at NATO headquarters, focused on Ukraine and 
climate change. Apple Inc. announced a $2 billion investment 
in renewable energy projects across California and Texas.
"""

entities = extract_entities(sample_article)
for entity in entities:
    print(f"{entity['text']} ({entity['label']}): {entity['description']}")
```

#### **Step 2: Reading News Articles from Files (10 minutes)**

```python
def read_article(filename):
    """Read article content from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return None

# Example usage
article_text = read_article("news_article1.txt")
if article_text:
    entities = extract_entities(article_text)
```

#### **Step 3: Organizing Results by Entity Type (15 minutes)**

```python
def organize_entities(entities):
    """Organize entities by type"""
    organized = {}
    
    for entity in entities:
        label = entity['label']
        if label not in organized:
            organized[label] = []
        organized[label].append(entity['text'])
    
    # Remove duplicates and count frequencies
    for label in organized:
        entity_counts = Counter(organized[label])
        organized[label] = dict(entity_counts)
    
    return organized

def display_results(organized_entities):
    """Display results in a readable format"""
    print("=" * 50)
    print("NEWS ARTICLE ENTITY ANALYSIS")
    print("=" * 50)
    
    for label, entities in organized_entities.items():
        description = spacy.explain(label)
        print(f"\n{label} ({description}):")
        print("-" * 30)
        
        for entity, count in entities.items():
            print(f"  • {entity}: {count} time(s)")
```

---

### **Day 3: Enhanced Features and Visualization (50 minutes)**

#### **Step 4: Advanced Features (20 minutes)**

```python
def analyze_article(filename):
    """Complete article analysis function"""
    print(f"Analyzing: {filename}")
    print("=" * 60)
    
    # Read article
    article_text = read_article(filename)
    if not article_text:
        return
    
    # Basic stats
    word_count = len(article_text.split())
    print(f"Word count: {word_count}")
    
    # Extract entities
    entities = extract_entities(article_text)
    organized = organize_entities(entities)
    
    # Display results
    display_results(organized)
    
    # Summary statistics
    total_entities = sum(len(ents) for ents in organized.values())
    unique_entities = len(entities)
    print(f"\nSUMMARY:")
    print(f"Total entity mentions: {total_entities}")
    print(f"Unique entities found: {unique_entities}")
    print(f"Entity types found: {len(organized)}")
    
    return organized

# Multi-article analysis
def compare_articles(filenames):
    """Compare entities across multiple articles"""
    all_results = {}
    
    for filename in filenames:
        print(f"\n{'='*60}")
        results = analyze_article(filename)
        all_results[filename] = results
    
    return all_results
```

#### **Step 5: Simple Data Visualization (15 minutes)**

```python
def create_entity_chart(organized_entities):
    """Create a simple text-based chart"""
    print(f"\n{'='*50}")
    print("ENTITY FREQUENCY CHART")
    print(f"{'='*50}")
    
    # Get all entities with counts
    all_entities = []
    for label, entities in organized_entities.items():
        for entity, count in entities.items():
            all_entities.append((entity, count, label))
    
    # Sort by frequency
    all_entities.sort(key=lambda x: x[1], reverse=True)
    
    # Display top 10
    print("\nTop 10 Most Mentioned Entities:")
    print("-" * 40)
    
    for i, (entity, count, label) in enumerate(all_entities[:10], 1):
        bar = "█" * min(count, 20)  # Visual bar
        print(f"{i:2}. {entity:<20} {bar} ({count})")
```

#### **Step 6: Interactive Features (15 minutes)**

```python
def interactive_ner_tool():
    """Interactive NER analysis tool"""
    print("Welcome to the News Entity Extractor!")
    print("-" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Analyze a news article file")
        print("2. Analyze custom text")
        print("3. Compare multiple articles")
        print("4. Quit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            filename = input("Enter filename: ")
            analyze_article(filename)
        
        elif choice == "2":
            text = input("Enter text to analyze: ")
            entities = extract_entities(text)
            organized = organize_entities(entities)
            display_results(organized)
        
        elif choice == "3":
            files = input("Enter filenames (comma-separated): ").split(",")
            files = [f.strip() for f in files]
            compare_articles(files)
        
        elif choice == "4":
            print("Thanks for using the News Entity Extractor!")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Run the interactive tool
if __name__ == "__main__":
    interactive_ner_tool()
```

---

### **Day 4: Project Completion and Presentation (50 minutes)**

#### **Final Integration and Testing (20 minutes)**
Students combine all components into a complete program and test with provided news articles.

#### **Extension Challenges (15 minutes)**
For advanced students:
1. **Sentiment Analysis Integration**: Determine if entities are mentioned positively or negatively
2. **Entity Linking**: Try to link entities to Wikipedia or other knowledge bases
3. **Custom Entity Training**: Research how to train spaCy to recognize custom entity types
4. **Web Scraping**: Automatically fetch news articles from websites
5. **Data Export**: Save results to CSV files for further analysis

#### **Student Presentations (15 minutes)**
Students demonstrate their programs and share interesting findings from their analysis.

---

## **Sample News Articles for Testing**

### **Article 1: Technology News**
```
Apple Inc. announced record quarterly earnings yesterday, with CEO Tim Cook 
crediting strong iPhone sales in China and India. The Cupertino-based company 
reported revenue of $89.5 billion for Q2 2024. Microsoft and Google also 
reported strong earnings this quarter, with Microsoft's cloud services Azure 
growing by 25% year-over-year. The tech earnings come as the Federal Reserve 
considers interest rate changes next month.
```

### **Article 2: Sports News**  
```
LeBron James scored 35 points as the Los Angeles Lakers defeated the Boston 
Celtics 112-108 last night at Staples Center. The victory moves the Lakers 
closer to a playoff spot in the Western Conference. James, who turned 39 in 
December, continues to play at an elite level in his 21st NBA season. The 
Lakers will next face the Golden State Warriors in San Francisco on Friday.
```

---

## **Assessment Rubric**

### **Knowledge Understanding (25 points)**
- **Excellent (23-25)**: Clearly explains NER concepts and applications
- **Good (20-22)**: Shows solid understanding with minor gaps
- **Satisfactory (17-19)**: Basic understanding demonstrated
- **Needs Improvement (0-16)**: Limited understanding shown

### **Code Implementation (35 points)**
- **Excellent (32-35)**: Clean, well-commented, functional code
- **Good (28-31)**: Code works with minor issues
- **Satisfactory (24-27)**: Basic functionality achieved
- **Needs Improvement (0-23)**: Code has significant problems

### **Project Completion (25 points)**
- **Excellent (23-25)**: All features implemented plus extensions
- **Good (20-22)**: Core features working well
- **Satisfactory (17-19)**: Basic requirements met
- **Needs Improvement (0-16)**: Incomplete project

### **Presentation (15 points)**
- **Excellent (14-15)**: Clear explanation and demonstration
- **Good (12-13)**: Good presentation with minor issues
- **Satisfactory (10-11)**: Basic presentation completed
- **Needs Improvement (0-9)**: Poor or incomplete presentation

---

## **Differentiation Strategies**

### **For Advanced Learners**
- Implement additional NER libraries (NLTK, Transformers)
- Create web interface using Flask
- Integrate with news APIs for real-time analysis
- Explore multilingual NER capabilities

### **For Struggling Learners**
- Provide completed code templates
- Focus on understanding concepts rather than implementation
- Pair programming opportunities
- Step-by-step guided practice

### **For English Language Learners**
- Provide vocabulary lists for technical terms
- Use visual aids and diagrams
- Allow analysis of articles in native languages
- Glossary of NER terminology

---

## **Extension Activities**

1. **Cross-Curricular Connections**:
   - Social Studies: Analyze historical documents
   - English: Extract characters and settings from literature
   - Science: Identify scientific terms and researchers in articles

2. **Real-World Applications**:
   - Contact local news organizations about their use of NER
   - Research how social media platforms use NER
   - Explore NER in accessibility tools

3. **Advanced Projects**:
   - Build a news aggregator that groups articles by entities
   - Create a fact-checking tool that tracks entity claims
   - Develop a personal assistant that extracts key information from emails

---

## **Resources and References**

### **Technical Resources**
- [spaCy Documentation](https://spacy.io/)
- [spaCy Entity Recognition Guide](https://spacy.io/usage/linguistic-features#named-entities)
- [Python Programming Tutorial](https://www.python.org/about/gettingstarted/)

### **Educational Resources**
- Natural Language Processing concepts for beginners
- Ethics in AI and text analysis
- Data privacy considerations in text processing

### **Sample Datasets**
- News articles from various sources
- Social media posts (anonymized)
- Historical documents and speeches
- Product reviews and descriptions

---

## **Homework Assignment**

**Individual Project**: Students choose a topic of personal interest (sports, entertainment, politics, science) and collect 3-5 articles about that topic. They then use their NER tool to:

1. Analyze all articles and identify common entities
2. Create a summary report of their findings
3. Reflect on what they learned about their chosen topic
4. Present one interesting discovery to the class

**Deliverables**:
- Python code file with their NER implementation
- Text files with their chosen articles  
- Written report (1-2 pages) with analysis and reflection
- 2-minute presentation of their most interesting finding