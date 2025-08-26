import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from collections import Counter
import re

def setup_custom_entity_matcher(nlp):
    """
    Set up custom patterns to recognize PRODUCT and EVENT entities
    This extends spaCy's built-in capabilities!
    """
    matcher = Matcher(nlp.vocab)
    
    # PRODUCT patterns - common product naming conventions
    product_patterns = [
        # Tech products: "iPhone 15", "Galaxy S24", "MacBook Pro"
        [{"LOWER": {"IN": ["iphone", "ipad", "macbook", "imac", "airpods", "galaxy", "pixel"]}},
         {"IS_ALPHA": True, "IS_SPACE": False, "OP": "?"},  # Optional model number/name
         {"LIKE_NUM": True, "OP": "?"}],  # Optional number
        
        # Car models: "Tesla Model S", "Ford F-150"
        [{"LOWER": {"IN": ["model", "f-150", "mustang", "camry", "accord", "civic"]}},
         {"IS_ALPHA": True, "OP": "*"}],
        
        # Software: "Windows 11", "iOS 17", "Android 14"
        [{"LOWER": {"IN": ["windows", "ios", "android", "macos", "linux"]}},
         {"LIKE_NUM": True, "OP": "?"}],
        
        # Gaming: "PlayStation 5", "Xbox Series X", "Nintendo Switch"
        [{"LOWER": {"IN": ["playstation", "xbox", "nintendo"]}},
         {"IS_ALPHA": True, "OP": "*"}],
        
        # Generic product pattern: "Brand Name + Product"
        [{"ENT_TYPE": "ORG"},  # Company name
         {"IS_ALPHA": True, "LENGTH": {">=": 3}},  # Product name
         {"LIKE_NUM": True, "OP": "?"}]  # Optional version number
    ]
    
    # EVENT patterns - common event naming conventions  
    event_patterns = [
        # Sports events: "Super Bowl", "World Cup", "Olympics"
        [{"LOWER": {"IN": ["super", "world", "winter", "summer"]}},
         {"LOWER": {"IN": ["bowl", "cup", "olympics", "games", "series", "championship"]}}],
        
        # Conferences: "WWDC 2024", "CES 2024", "E3"
        [{"IS_UPPER": True, "LENGTH": {">=": 2, "<=": 5}},  # Acronym
         {"LIKE_NUM": True, "OP": "?"}],  # Optional year
        
        # Awards: "Academy Awards", "Emmy Awards", "Grammy Awards"
        [{"LOWER": {"IN": ["academy", "emmy", "grammy", "golden", "nobel"]}},
         {"LOWER": {"IN": ["awards", "prize", "ceremony", "globes"]}}],
        
        # Elections: "2024 Presidential Election", "Midterm Elections"
        [{"LIKE_NUM": True, "OP": "?"},  # Optional year
         {"LOWER": {"IN": ["presidential", "midterm", "general", "primary"]}},
         {"LOWER": {"IN": ["election", "elections", "race"]}}],
        
        # General events with keywords
        [{"LOWER": {"IN": ["festival", "conference", "summit", "expo", "fair"]}},
         {"LIKE_NUM": True, "OP": "?"}]
    ]
    
    # Add patterns to matcher
    matcher.add("PRODUCT", product_patterns)
    matcher.add("EVENT", event_patterns)
    
    return matcher

def add_custom_entities(doc, matcher):
    """
    Add custom PRODUCT and EVENT entities to the document
    """
    matches = matcher(doc)
    new_ents = []
    
    # Keep existing entities
    existing_ents = [(ent.start, ent.end, ent.label_) for ent in doc.ents]
    
    # Add custom matches
    for match_id, start, end in matches:
        label = doc.vocab.strings[match_id]  # Get label name (PRODUCT or EVENT)
        
        # Check for overlaps with existing entities
        span = doc[start:end]
        overlaps = False
        for ent_start, ent_end, _ in existing_ents:
            if not (end <= ent_start or start >= ent_end):  # Check overlap
                overlaps = True
                break
        
        if not overlaps:
            new_ents.append((start, end, label))
    
    # Combine existing and new entities
    all_ents = existing_ents + new_ents
    all_ents = sorted(set(all_ents))  # Remove duplicates and sort
    
    # Create new entity spans
    entities = []
    for start, end, label in all_ents:
        entities.append(Span(doc, start, end, label=label))
    
    # Update document entities
    doc.ents = entities
    return doc

def extract_entities_enhanced(text):
    """
    Enhanced entity extraction with PRODUCT and EVENT recognition
    """
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    
    # Set up custom matcher
    matcher = setup_custom_entity_matcher(nlp)
    
    # Process text
    doc = nlp(text)
    
    # Add custom entities
    doc = add_custom_entities(doc, matcher)
    
    # Extract all entities (built-in + custom)
    entities = []
    for ent in doc.ents:
        # Get description for custom entities
        if ent.label_ in ["PRODUCT", "EVENT"]:
            description = f"Custom {ent.label_.lower()} recognition"
        else:
            description = spacy.explain(ent.label_)
            
        entities.append({
            'text': ent.text,
            'label': ent.label_,
            'description': description,
            'is_custom': ent.label_ in ["PRODUCT", "EVENT"]
        })
    
    return entities

def organize_entities_enhanced(entities):
    """
    Enhanced organization that handles custom entities
    """
    organized = {}
    
    for entity in entities:
        label = entity['label']
        entity_text = entity['text']
        
        if label not in organized:
            organized[label] = []
        
        organized[label].append(entity_text)
    
    # Count frequencies
    for label in organized:
        entity_counts = Counter(organized[label])
        organized[label] = dict(entity_counts)
    
    return organized

def display_results_enhanced(organized_entities, filename=""):
    """
    Enhanced display with special highlighting for custom entities
    """
    print("\n" + "="*70)
    print(f"📰 ENHANCED NEWS ARTICLE ENTITY ANALYSIS")
    if filename:
        print(f"Article: {filename}")
    print("="*70)
    
    # Separate custom and standard entities for better display
    standard_entities = {}
    custom_entities = {}
    
    for label, entities in organized_entities.items():
        if label in ["PRODUCT", "EVENT"]:
            custom_entities[label] = entities
        else:
            standard_entities[label] = entities
    
    # Display standard entities first
    if standard_entities:
        print("\n🔍 STANDARD ENTITIES:")
        print("-" * 50)
        for label in sorted(standard_entities.keys()):
            entities = standard_entities[label]
            description = spacy.explain(label)
            
            print(f"\n🏷️  {label} ({description}):")
            sorted_entities = sorted(entities.items(), key=lambda x: x[1], reverse=True)
            
            for entity, count in sorted_entities:
                if count == 1:
                    print(f"   • {entity}")
                else:
                    print(f"   • {entity} (mentioned {count} times)")
    
    # Display custom entities with special formatting
    if custom_entities:
        print(f"\n✨ CUSTOM ENTITIES (Enhanced Recognition):")
        print("-" * 50)
        
        for label in ["PRODUCT", "EVENT"]:  # Specific order
            if label in custom_entities:
                entities = custom_entities[label]
                emoji = "📱" if label == "PRODUCT" else "🎪"
                
                print(f"\n{emoji} {label}S:")
                sorted_entities = sorted(entities.items(), key=lambda x: x[1], reverse=True)
                
                for entity, count in sorted_entities:
                    if count == 1:
                        print(f"   ⭐ {entity}")
                    else:
                        print(f"   ⭐ {entity} (mentioned {count} times)")

def analyze_article_enhanced(filename):
    """
    Complete enhanced article analysis with PRODUCT and EVENT recognition
    """
    print(f"\n🔍 Enhanced Analysis: {filename}")
    print("="*80)
    
    # Read the article
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            article_text = file.read()
        print(f"✅ Successfully loaded article from {filename}")
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found!")
        return None
    
    # Basic statistics
    words = article_text.split()
    sentences = article_text.split('.')
    print(f"\n📊 Article Statistics:")
    print(f"   • Word count: {len(words)}")
    print(f"   • Sentence count: {len(sentences)}")
    
    # Enhanced entity extraction
    print(f"\n🤖 Extracting entities (including PRODUCTS and EVENTS)...")
    entities = extract_entities_enhanced(article_text)
    
    # Count custom vs standard entities
    custom_count = len([e for e in entities if e.get('is_custom', False)])
    standard_count = len(entities) - custom_count
    
    print(f"   • Found {len(entities)} total entities")
    print(f"   • Standard entities: {standard_count}")
    print(f"   • Custom entities (PRODUCT/EVENT): {custom_count}")
    
    # Organize and display
    organized = organize_entities_enhanced(entities)
    display_results_enhanced(organized, filename)
    
    # Summary
    total_mentions = sum(sum(ents.values()) for ents in organized.values())
    entity_types = len(organized)
    
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"   • Total entity mentions: {total_mentions}")
    print(f"   • Unique entities found: {len(entities)}")
    print(f"   • Entity types found: {entity_types}")
    if custom_count > 0:
        print(f"   ⭐ Custom entities detected: {custom_count}")
    
    return organized

# Test with sample article containing products and events
test_article_enhanced = """
Apple announced the new iPhone 15 Pro at their September event yesterday. 
CEO Tim Cook revealed that the iPhone 15 will feature a titanium design and 
improved camera system. The announcement came during Apple's annual WWDC conference 
in Cupertino, California. 

Meanwhile, Microsoft unveiled the new Xbox Series X console and Windows 11 
operating system updates. The company plans to showcase these products at CES 2024 
in Las Vegas next January. 

In sports news, the Super Bowl LVIII will be held in Las Vegas, featuring 
exciting halftime performances and the Grammy Awards ceremony following soon after. 
Tesla's Model S Plaid was chosen as the official vehicle for the Olympic Games 
torch relay in Paris.
"""

# Save test article
with open("enhanced_test_article.txt", "w") as f:
    f.write(test_article_enhanced)

# Run enhanced analysis
print("🚀 TESTING ENHANCED ENTITY EXTRACTOR")
print("="*80)

result = analyze_article_enhanced("enhanced_test_article.txt")

print("\n" + "🎉"*30)
print("SUCCESS! Your enhanced extractor can now recognize:")
print("• PRODUCTS: iPhone 15, Xbox Series X, Windows 11, Model S")  
print("• EVENTS: WWDC, CES 2024, Super Bowl, Grammy Awards, Olympic Games")
print("🎉"*30)