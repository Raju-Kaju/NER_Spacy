import spacy
from spacy.training import Example
from spacy.util import minibatch
import random
import json
from pathlib import Path

class CustomEntityTrainer:
    """
    A class to train spaCy models with custom entities
    Perfect for recognizing school-specific, local, or domain-specific entities!
    """
    
    def __init__(self, model_name="en_core_web_sm"):
        """Initialize the trainer with a base spaCy model"""
        print("🤖 Initializing Custom Entity Trainer...")
        try:
            self.nlp = spacy.load(model_name)
            print(f"✅ Loaded base model: {model_name}")
        except OSError:
            print(f"❌ Model {model_name} not found. Creating blank model...")
            self.nlp = spacy.blank("en")
        
        # Get or create the NER component
        if "ner" not in self.nlp.pipe_names:
            ner = self.nlp.add_pipe("ner", last=True)
        else:
            ner = self.nlp.get_pipe("ner")
        
        self.ner = ner
        
    def prepare_training_data(self):
        """
        Prepare training data for custom entities
        This is where students define what they want the model to learn!
        """
        print("📚 Preparing training data for custom entities...")
        
        # Example: Training data for school-specific entities
        # Format: (text, {"entities": [(start, end, label)]})
        training_data = [
            # SCHOOL entities - local schools
            ("Washington High School won the state championship", 
             {"entities": [(0, 21, "SCHOOL")]}),
            
            ("Students from Lincoln Elementary are participating", 
             {"entities": [(13, 30, "SCHOOL")]}),
            
            ("Roosevelt Middle School announced new programs", 
             {"entities": [(0, 22, "SCHOOL")]}),
            
            ("The Jefferson Academy basketball team", 
             {"entities": [(4, 21, "SCHOOL")]}),
            
            ("Madison High and Roosevelt Middle will compete", 
             {"entities": [(0, 12, "SCHOOL"), (17, 33, "SCHOOL")]}),
            
            # LOCAL_BUSINESS entities - local businesses
            ("Joe's Pizza serves the best food in town", 
             {"entities": [(0, 10, "LOCAL_BUSINESS")]}),
            
            ("I bought supplies at Corner Hardware Store", 
             {"entities": [(20, 41, "LOCAL_BUSINESS")]}),
            
            ("Main Street Cafe is hiring new workers", 
             {"entities": [(0, 16, "LOCAL_BUSINESS")]}),
            
            ("The Downtown Library and City Park", 
             {"entities": [(4, 21, "LOCAL_BUSINESS")]}),
            
            # SPORTS_TEAM entities - local teams
            ("The Eagles defeated the Lions 21-14", 
             {"entities": [(4, 10, "SPORTS_TEAM"), (24, 29, "SPORTS_TEAM")]}),
            
            ("Tigers are playing against Warriors tonight", 
             {"entities": [(0, 6, "SPORTS_TEAM"), (26, 34, "SPORTS_TEAM")]}),
            
            ("The Panthers had an amazing season", 
             {"entities": [(4, 12, "SPORTS_TEAM")]}),
            
            # COURSE entities - school subjects/courses
            ("Advanced Python Programming is my favorite class", 
             {"entities": [(0, 26, "COURSE")]}),
            
            ("Students excel in AP Biology and Chemistry", 
             {"entities": [(18, 28, "COURSE"), (33, 42, "COURSE")]}),
            
            ("Introduction to Data Science starts Monday", 
             {"entities": [(0, 27, "COURSE")]}),
            
            # Mixed examples for better training
            ("Washington High School students study AP Biology at Main Street Cafe", 
             {"entities": [(0, 21, "SCHOOL"), (37, 47, "COURSE"), (51, 67, "LOCAL_BUSINESS")]}),
            
            ("The Eagles from Roosevelt Middle won their Chemistry competition", 
             {"entities": [(4, 10, "SPORTS_TEAM"), (16, 32, "SCHOOL"), (47, 56, "COURSE")]}),
        ]
        
        return training_data
    
    def add_custom_labels(self, labels):
        """Add custom entity labels to the NER model"""
        print(f"🏷️  Adding custom labels: {labels}")
        for label in labels:
            self.ner.add_label(label)
    
    def train_model(self, training_data, iterations=30):
        """
        Train the model with custom entity data
        This is where the magic happens!
        """
        print(f"🎓 Training model for {iterations} iterations...")
        print("This might take a few minutes - grab a snack! ☕")
        
        # Add labels from training data
        labels = set()
        for text, annotations in training_data:
            for start, end, label in annotations["entities"]:
                labels.add(label)
        
        self.add_custom_labels(labels)
        
        # Disable other pipes during training for efficiency
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        with self.nlp.disable_pipes(*other_pipes):
            
            # Initialize the model's weights randomly
            self.nlp.begin_training()
            
            for iteration in range(iterations):
                print(f"  Iteration {iteration + 1}/{iterations}...")
                
                # Shuffle training data
                random.shuffle(training_data)
                losses = {}
                
                # Create training batches
                for batch in minibatch(training_data, size=2):
                    examples = []
                    for text, annotations in batch:
                        # Create Example objects
                        doc = self.nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        examples.append(example)
                    
                    # Update the model
                    self.nlp.update(examples, losses=losses)
                
                # Print progress every 10 iterations
                if (iteration + 1) % 10 == 0:
                    print(f"    Losses: {losses}")
        
        print("✅ Training completed!")
    
    def save_model(self, path="./custom_ner_model"):
        """Save the trained model"""
        print(f"💾 Saving model to {path}...")
        self.nlp.to_disk(path)
        print("✅ Model saved successfully!")
    
    def load_custom_model(self, path="./custom_ner_model"):
        """Load a previously trained model"""
        print(f"📂 Loading custom model from {path}...")
        self.nlp = spacy.load(path)
        print("✅ Custom model loaded!")
    
    def test_model(self, test_texts):
        """Test the trained model on new text"""
        print("🧪 Testing custom entity recognition...")
        print("=" * 60)
        
        for text in test_texts:
            doc = self.nlp(text)
            print(f"\nText: '{text}'")
            print("Entities found:")
            
            if doc.ents:
                for ent in doc.ents:
                    # Check if this is a custom entity
                    is_custom = ent.label_ in ["SCHOOL", "LOCAL_BUSINESS", "SPORTS_TEAM", "COURSE"]
                    marker = "⭐ CUSTOM" if is_custom else "📍 STANDARD"
                    
                    print(f"  {marker}: '{ent.text}' → {ent.label_}")
            else:
                print("  No entities detected")
        print("=" * 60)

def create_training_data_template():
    """
    Create a template file for students to add their own training data
    """
    template = {
        "instructions": "Add your own training examples below. Follow the format exactly!",
        "format_example": {
            "text": "Your example sentence here",
            "entities": [
                {"start": 0, "end": 10, "label": "YOUR_CUSTOM_LABEL", "description": "What this entity represents"}
            ]
        },
        "your_custom_entities": [
            {
                "text": "Central Valley High School is having a bake sale",
                "entities": [
                    {"start": 0, "end": 22, "label": "SCHOOL", "description": "Local school name"}
                ]
            },
            {
                "text": "The Wildcats beat the Storm 3-1 in soccer",
                "entities": [
                    {"start": 4, "end": 12, "label": "SPORTS_TEAM", "description": "Local team name"},
                    {"start": 22, "end": 27, "label": "SPORTS_TEAM", "description": "Local team name"}
                ]
            }
        ]
    }
    
    with open("training_data_template.json", "w") as f:
        json.dump(template, f, indent=2)
    
    print("📝 Created training_data_template.json")
    print("Students can edit this file to add their own examples!")

def main_demo():
    """
    Main demonstration of custom entity training
    Perfect for showing students the complete process!
    """
    print("🚀 CUSTOM ENTITY TRAINING DEMONSTRATION")
    print("=" * 80)
    
    # Step 1: Initialize trainer
    trainer = CustomEntityTrainer()
    
    # Step 2: Prepare training data
    training_data = trainer.prepare_training_data()
    print(f"📊 Prepared {len(training_data)} training examples")
    
    # Step 3: Train the model
    trainer.train_model(training_data, iterations=20)  # Reduced for demo
    
    # Step 4: Test the trained model
    test_sentences = [
        "Washington High School students are excited",  # Should detect SCHOOL
        "The Eagles won against Lincoln Elementary",    # Should detect SPORTS_TEAM and SCHOOL
        "Joe's Pizza is hiring for summer jobs",        # Should detect LOCAL_BUSINESS  
        "Advanced Python Programming class starts soon", # Should detect COURSE
        "Roosevelt Middle School Tigers practice daily",  # Should detect SCHOOL and SPORTS_TEAM
        "Students bought lunch at Corner Hardware Store", # Should detect LOCAL_BUSINESS
        "The meeting is at Apple headquarters in California" # Standard entities (no custom)
    ]
    
    trainer.test_model(test_sentences)
    
    # Step 5: Save the model
    trainer.save_model()
    
    # Step 6: Create template for students
    create_training_data_template()
    
    print("\n🎉 TRAINING COMPLETE!")
    print("Your custom model can now recognize:")
    print("⭐ SCHOOL - Local schools and educational institutions")  
    print("⭐ LOCAL_BUSINESS - Local businesses and services")
    print("⭐ SPORTS_TEAM - Local sports teams")
    print("⭐ COURSE - Academic subjects and courses")
    print("\nPlus all the standard spaCy entities!")

def student_friendly_trainer():
    """
    Simplified version for students to customize easily
    """
    print("👨‍🎓 STUDENT-FRIENDLY CUSTOM ENTITY TRAINER")
    print("=" * 60)
    
    # Easy customization area
    YOUR_CUSTOM_ENTITIES = [
        # Add your own examples here!
        # Format: ("sentence with entity", start_pos, end_pos, "LABEL")
        ("Kennedy High School won the championship", 0, 19, "SCHOOL"),
        ("Pizza Palace has great food", 0, 12, "LOCAL_BUSINESS"),
        ("The Rockets played amazing defense", 4, 11, "SPORTS_TEAM"),
        ("Calculus class is challenging", 0, 8, "COURSE"),
        
        # Students can add more examples here:
        ("Lincoln Elementary students are reading", 0, 18, "SCHOOL"),
        ("Burger Barn serves breakfast all day", 0, 11, "LOCAL_BUSINESS"),
        ("The Lions defeated the Bears", 4, 9, "SPORTS_TEAM"),
        ("Chemistry lab starts at 2pm", 0, 9, "COURSE"),
    ]
    
    # Convert to proper format
    training_data = []
    for text, start, end, label in YOUR_CUSTOM_ENTITIES:
        training_data.append((text, {"entities": [(start, end, label)]}))
    
    # Train and test
    trainer = CustomEntityTrainer()
    trainer.train_model(training_data, iterations=15)
    
    # Test with student examples
    test_texts = [
        "Kennedy High School has a new principal",
        "The Rockets are practicing at Pizza Palace", 
        "Students are struggling with Calculus class"
    ]
    
    trainer.test_model(test_texts)
    trainer.save_model("./student_custom_model")
    
    print("🎓 Great job! Your custom model is ready to use!")

if __name__ == "__main__":
    print("Choose your training mode:")
    print("1. Full demonstration (recommended)")
    print("2. Student-friendly version")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "2":
        student_friendly_trainer()
    else:
        main_demo()
    
    print("\n🔥 NEXT STEPS:")
    print("1. Try adding your own training examples")
    print("2. Experiment with different entity types")
    print("3. Test on articles from your local newspaper")
    print("4. Share your custom model with classmates!")
    print("\nYou're now a custom NLP model trainer! 🚀")