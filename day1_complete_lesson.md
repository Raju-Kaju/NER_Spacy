# Day 1: Introduction to Named Entity Recognition (NER)
## Complete 50-Minute Lesson Plan with Teacher Script

---

## **Pre-Class Setup (5 minutes before class)**

### **Materials Checklist:**
- [ ] Projector/screen ready
- [ ] Sample news article printed/displayed
- [ ] Student computers logged in
- [ ] Code editor open (VS Code recommended)
- [ ] Terminal/command prompt ready
- [ ] Highlighters or colored pens (optional)
- [ ] Handout: "NER Entity Types Reference Sheet"

### **Slide Deck Setup:**
- Slide 1: "How Does Google Know?" (hook question)
- Slide 2: Sample news article for annotation
- Slide 3: NER definition
- Slide 4: Entity types with examples
- Slide 5: Real-world applications
- Slide 6: spaCy introduction
- Slide 7: Installation commands
- Slide 8: Basic code example

---

## **MINUTE-BY-MINUTE LESSON BREAKDOWN**

### **Opening Hook & Attention Grabber (0:00-0:10)**

**[Teacher enters with energy, displays Slide 1]**

**Teacher:** "Good morning, everyone! Before we start, I want you to think about something you probably do every day. How many of you check the news online - maybe Google News, Apple News, or social media?"

**[Wait for hands, acknowledge responses]**

**Teacher:** "Here's a fascinating question that's going to blow your mind: **How does Google News automatically know that this article is about Elon Musk, Tesla, and California without a human reading it?**"

**[Display news article on Slide 2]**

```
SAMPLE ARTICLE TO DISPLAY:
"Tesla CEO Elon Musk announced yesterday that the company will build 
a new Gigafactory in Austin, Texas. The $5 billion facility will 
create 10,000 jobs and produce batteries for Tesla vehicles. Governor 
Greg Abbott praised the decision, saying it will boost Texas's economy 
by 15% over the next decade. Construction begins in March 2025."
```

**Teacher:** "Take 30 seconds - turn to your neighbor and see how many different types of 'things' you can identify in this article. Go!"

**[Students discuss for 30 seconds]**

**Teacher:** "Okay, what did you find? I'm hearing 'Elon Musk' - that's a person. 'Tesla' - that's a company. 'Austin, Texas' - that's a place. '$5 billion' - that's money. 'March 2025' - that's a date."

**[Write categories on board: PEOPLE, PLACES, COMPANIES, MONEY, DATES]**

**Teacher:** "What if I told you that computers can automatically identify ALL of these things in ANY piece of text, in milliseconds, and that by the end of this week, you'll build a program that does exactly this? That's what we're learning today - it's called **Named Entity Recognition**, and it's one of the coolest things in computer science!"

---

### **What is Named Entity Recognition? (0:10-0:25)**

**[Display Slide 3: NER Definition]**

**Teacher:** "Named Entity Recognition - let's break this down word by word:"

- **Named**: We're looking for things that have names
- **Entity**: A 'thing' or object that exists
- **Recognition**: The computer identifies and categorizes them

**[Write definition on board]**

**Definition:** "Named Entity Recognition (NER) is like teaching a computer to be a really good detective. It reads text and automatically finds and labels important 'things' - people, places, organizations, dates, money amounts, and more."

**Teacher:** "Let's go back to our Tesla article. I'm going to give you each a copy and some colored highlighters. Here's your mission:"

**[Distribute article copies and highlighters]**

**Activity Instructions:**
- **Yellow**: Highlight all PEOPLE (names of actual people)
- **Green**: Highlight all PLACES (cities, states, countries)  
- **Blue**: Highlight all ORGANIZATIONS (companies, government agencies)
- **Red**: Highlight all MONEY amounts
- **Orange**: Highlight all DATES and TIMES

**[Give students 3 minutes to highlight]**

**Teacher:** "Alright, let's compare! What people did you find?"

**Expected Student Responses:**
- "Elon Musk"
- "Greg Abbott"

**Teacher:** "Perfect! What about places?"

**Expected Student Responses:**
- "Austin"
- "Texas"

**Teacher:** "Organizations?"

**Expected Student Responses:**
- "Tesla"

**Teacher:** "Excellent! Money?"

**Expected Student Responses:**
- "$5 billion"

**Teacher:** "And dates?"

**Expected Student Responses:**
- "yesterday"
- "March 2025"
- "next decade"

**[Display Slide 4: Official Entity Types]**

**Teacher:** "You just did what we call Named Entity Recognition! But computers use specific labels. Let me show you the official categories:"

**Common NER Entity Types:**
- **PERSON**: People's names → "Elon Musk", "Greg Abbott"
- **ORG**: Organizations, companies → "Tesla"
- **GPE**: Geo-political entities (places) → "Austin", "Texas"  
- **MONEY**: Monetary values → "$5 billion"
- **DATE**: Dates and times → "yesterday", "March 2025"
- **PERCENT**: Percentages → "15%"
- **CARDINAL**: Numbers that aren't money/percent → "10,000 jobs"

**Teacher:** "Think of it like this - you're teaching a computer to read like a human, but with perfect consistency and incredible speed."

---

### **Real-World Applications (0:25-0:35)**

**[Display Slide 5: Applications]**

**Teacher:** "Now here's where it gets really cool. Raise your hand if you've ever:"
- "Used Google to search for news about a specific person?" **[Wait for hands]**
- "Gotten friend suggestions on social media?" **[Wait for hands]**
- "Seen 'People also ask' suggestions when searching?" **[Wait for hands]**
- "Used Siri, Alexa, or Google Assistant?" **[Wait for hands]**

**Teacher:** "ALL of these use Named Entity Recognition! Let me show you how:"

**Real-World Applications:**

1. **News Aggregation**: 
   - "Google News finds all articles mentioning 'Taylor Swift' by using NER to identify her name in millions of articles"

2. **Social Media Monitoring**: 
   - "Companies use NER to track mentions of their brand across Twitter, Instagram, Facebook"

3. **Chatbots & Virtual Assistants**: 
   - "When you ask Siri 'What's the weather in Chicago?', NER identifies 'Chicago' as a location"

4. **Financial Analysis**: 
   - "Banks use NER to automatically extract company names and dollar amounts from financial reports"

5. **Medical Records**: 
   - "Hospitals use NER to identify medication names, dosages, and patient symptoms in doctor's notes"

6. **Content Recommendation**: 
   - "Netflix might use NER to understand that you like movies about 'New York' or featuring 'Tom Hanks'"

**Teacher:** "Think about this - every time you interact with technology and it 'understands' what you're talking about, there's probably some form of NER happening behind the scenes!"

**Quick Check Question:** "Can anyone think of another place where NER might be useful?"

**[Allow 2-3 student responses, affirm creative thinking]**

---

### **Introduction to spaCy Library (0:35-0:45)**

**[Display Slide 6: spaCy Introduction]**

**Teacher:** "Okay, so how do we actually DO this? We're going to use a Python library called spaCy. Think of spaCy as a really smart toolkit that someone else built and shared with the world."

**What is spaCy?**
- Industrial-strength Natural Language Processing
- Used by major companies like Netflix, Airbnb, Microsoft
- Fast, accurate, and (most importantly for us) easy to learn!
- Has pre-trained models that already know thousands of entities

**Teacher:** "It's like having a really smart friend who's already read millions of articles and learned to identify entities, and now they're going to help you!"

**[Display Slide 7: Installation]**

**Teacher:** "First, we need to install spaCy on your computers. Everyone open your terminal or command prompt."

**Installation Steps:**
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

**Teacher:** "The first command installs spaCy. The second downloads a pre-trained English model - that's our 'smart friend' I mentioned!"

**[Walk around room helping with installation - budget 3-4 minutes for this]**

**Teacher:** "While that's installing, let me show you how simple the code is:"

**[Display Slide 8: Basic Code Example]**

```python
import spacy

# Load the English model (our smart friend!)
nlp = spacy.load("en_core_web_sm")

# Give it some text to analyze
text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."

# Process the text
doc = nlp(text)

# Look at what it found!
for ent in doc.ents:
    print(f"{ent.text} - {ent.label_}")
```

**Teacher:** "That's it! Just 5 lines of actual code, and the computer can identify entities in any text you give it!"

---

### **Hands-On Practice Session (0:45-0:50)**

**Teacher:** "Alright, everyone should have spaCy installed now. Let's try it! Open your code editor and type in this exact code:"

**[Project code on screen, walk around helping students]**

**Practice Code:**
```python
import spacy

# Load the model
nlp = spacy.load("en_core_web_sm")

# Our test sentence
text = "Barack Obama visited Google headquarters in Mountain View, California last Tuesday."

# Process it
doc = nlp(text)

# See what we found
print("Entities found:")
for ent in doc.ents:
    print(f"'{ent.text}' is a {ent.label_}")
```

**Expected Output:**
```
Entities found:
'Barack Obama' is a PERSON
'Google' is a ORG
'Mountain View' is a GPE
'California' is a GPE
'last Tuesday' is a DATE
```

**Teacher:** "Wow! Look at that! The computer automatically figured out that 'Barack Obama' is a person, 'Google' is an organization, and 'Mountain View' and 'California' are places!"

**Challenge for Fast Finishers:**
"Try changing the sentence to include your own name and your school. What does spaCy identify?"

**Example:**
```python
text = "Sarah Johnson studies at Lincoln High School in Springfield, Illinois."
```

---

### **Wrap-Up and Preview (0:50-0:52)**

**Teacher:** "In just 50 minutes, you've learned what Named Entity Recognition is, seen how it powers the technology you use every day, and written your first NER program! 

Tomorrow, we're going to build something really cool - a program that can read entire news articles and extract ALL the people, places, and organizations mentioned, then organize them into a nice report.

**For homework tonight**: Find a news article online about something you're interested in - sports, music, technology, whatever. Read it and try to identify all the people, places, and organizations mentioned. Tomorrow, we'll feed your article into our program and see how well the computer does compared to you!

Any questions about what we learned today?"

**[Answer 1-2 quick questions]**

**Teacher:** "Excellent work today, everyone. You're now officially NER detectives!"

---

## **TEACHER NOTES & TROUBLESHOOTING**

### **Common Installation Issues:**
- **Python not found**: Check if Python is properly installed and in PATH
- **Permission errors**: May need to use `pip3` instead of `pip`
- **Network issues**: Have backup offline installer ready
- **Model download fails**: Can be downloaded manually if needed

### **Differentiation During Class:**
- **Advanced students**: Give them the spaCy documentation link to explore other entity types
- **Struggling students**: Pair them with stronger programmers, focus on understanding concepts over coding
- **Non-native English speakers**: Show them that spaCy works with other languages too

### **Assessment Checkpoints:**
1. **During highlighting activity**: Walk around, check if students are correctly identifying entity types
2. **During coding**: Ensure everyone can run the basic example
3. **Exit ticket**: "Name one real-world application of NER that interests you"

### **Extension Activities:**
If you finish early:
- Show students spaCy's visualization tool: `displacy`
- Demonstrate other entity types like PRODUCT, EVENT, WORK_OF_ART
- Let them experiment with different text samples

### **Homework Collection Strategy:**
- Have students email you their chosen article
- Create a shared folder where they can upload articles  
- Use their articles as examples in tomorrow's lesson

---

## **MATERIALS TO PREPARE**

### **Handout: NER Entity Types Reference Sheet**
```
NAMED ENTITY RECOGNITION - QUICK REFERENCE

PERSON - Names of people, including fictional characters
Examples: "Barack Obama", "Harry Potter", "Dr. Smith"

ORG - Companies, agencies, institutions, etc.
Examples: "Apple Inc.", "NASA", "Harvard University"

GPE - Countries, cities, states (Geo-Political Entities)
Examples: "New York", "Japan", "California"

DATE - Absolute or relative dates or periods
Examples: "January 1st", "tomorrow", "last year"

TIME - Times smaller than a day
Examples: "3 PM", "morning", "midnight"

MONEY - Monetary values, including unit
Examples: "$50", "twenty dollars", "€100"

PERCENT - Percentage values
Examples: "25%", "fifty percent"

CARDINAL - Numerals that don't fall under other types
Examples: "three", "100", "dozens"

ORDINAL - "First", "second", etc.
Examples: "1st", "twenty-third"

QUANTITY - Measurements, as of weight or distance
Examples: "5 miles", "20 pounds"
```

### **Sample Articles for Student Practice:**
Keep 3-4 different articles ready covering different topics (sports, technology, politics, entertainment) in case students need inspiration.

---

## **LESSON REFLECTION QUESTIONS**

**For Teacher Self-Assessment:**
1. Did students successfully identify entities in the manual exercise?
2. How many students successfully installed spaCy?
3. Were students engaged during the real-world applications section?
4. What questions did students ask that I should address tomorrow?
5. Which students might need extra support in Day 2?

**Student Exit Ticket:**
"On a scale of 1-5, how confident do you feel about:
- Understanding what NER is? ___
- Seeing how NER is used in real life? ___
- Writing basic Python code with spaCy? ___

What's one thing from today that you found most interesting?"