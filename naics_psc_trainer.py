import spacy
from spacy.training import Example
from spacy.util import minibatch
import random
import re
import json
from pathlib import Path

class NAICSPSCTrainer:
    """
    Custom trainer for recognizing NAICS codes and PSC codes in business/government text
    
    NAICS: 6-digit codes for business classification (e.g., 541511 - Custom Computer Programming)
    PSC: 4-character codes for government products/services (e.g., 7030 - Information Technology)
    """
    
    def __init__(self):
        """Initialize with blank English model for specialized training"""
        print("🏛️ Initializing NAICS/PSC Code Recognition Trainer...")
        
        # Start with blank model for specialized domain
        self.nlp = spacy.blank("en")
        
        # Add required pipeline components
        self.nlp.add_pipe("tok2vec")
        self.ner = self.nlp.add_pipe("ner")
        
        # Add our custom labels
        self.ner.add_label("NAICS")
        self.ner.add_label("PSC")
        
        print("✅ Blank model initialized with NAICS and PSC entity recognition")
    
    def create_naics_psc_database(self):
        """
        Create reference database of real NAICS and PSC codes
        This helps with training data generation and validation
        """
        # Sample of real NAICS codes with descriptions
        naics_codes = {
            "541511": "Custom Computer Programming Services",
            "541512": "Computer Systems Design Services", 
            "541513": "Computer Facilities Management Services",
            "541519": "Other Computer Related Services",
            "518210": "Data Processing, Hosting, and Related Services",
            "334111": "Electronic Computer Manufacturing",
            "423430": "Computer and Computer Peripheral Equipment Wholesalers",
            "443142": "Electronics Stores",
            "611420": "Computer Training",
            "811212": "Computer and Office Machine Repair",
            "236220": "Commercial and Institutional Building Construction",
            "238210": "Electrical Contractors and Other Wiring Installation",
            "541330": "Engineering Services",
            "541310": "Architectural Services",
            "722511": "Full-Service Restaurants",
            "722513": "Limited-Service Restaurants",
            "561320": "Temporary Help Services",
            "621111": "Offices of Physicians",
            "484110": "General Freight Trucking, Local",
            "336411": "Aircraft Manufacturing"
        }
        
        # Sample of real PSC codes with descriptions  
        psc_codes = {
            "7030": "Information Technology Software",
            "7035": "Information Technology Support Services",
            "D302": "IT and Telecom- IT and Telecom Solutions",
            "D307": "IT and Telecom- Cyber Security and Data Protection",
            "R425": "Professional Services- Engineering/Technical",
            "R408": "Professional Services- Program Management/Support Services",
            "J015": "Maintenance of Real Property- General Services",
            "Z2A1": "Facilities Related Services- Lease/Rental of Equipment",
            "W152": "Transportation/Travel/Relocation- Aircraft and Airframe Structural Components",
            "5945": "Aviation Ground Support Equipment",
            "7045": "Training Services",
            "6515": "Medical/Surgical Instruments and Supplies",
            "8810": "Construction Services",
            "2840": "Cleaning Compounds and Toilet Preparations",
            "7540": "Equipment Rental and Leasing Services",
            "R413": "Professional Services- Information Services",
            "4240": "Safety and Rescue Equipment",
            "1560": "Airframe Structural Components",
            "C211": "Architectural and Engineering Services- Architectural Services",
            "Q201": "Fire Protection Services"
        }
        
        self.naics_db = naics_codes
        self.psc_db = psc_codes
        return naics_codes, psc_codes
    
    def generate_training_data(self):
        """
        Generate comprehensive training data for NAICS and PSC recognition
        """
        print("📊 Generating training data for NAICS and PSC codes...")
        
        # Initialize code databases
        naics_codes, psc_codes = self.create_naics_psc_database()
        
        training_data = []
        
        # NAICS Code Training Examples
        naics_templates = [
            "Company operates under NAICS code {code} for {description}",
            "Primary business classification is NAICS {code} ({description})", 
            "The contractor's NAICS code {code} indicates {description}",
            "Vendor specializes in NAICS {code} - {description}",
            "Business category NAICS {code}: {description}",
            "Industry classification {code} covers {description}",
            "NAICS {code} businesses provide {description}",
            "The firm is registered under {code} for {description}",
            "Small business set-aside for NAICS code {code}",
            "Competition restricted to {code} classified businesses",
            "Contractor must have experience in NAICS {code}",
            "Primary NAICS: {code}",
            "NAICS Code: {code}",
            "{code} - {description}"
        ]
        
        # Generate NAICS training examples
        for code, description in naics_codes.items():
            for template in naics_templates[:8]:  # Use subset to avoid overfitting
                if random.random() < 0.7:  # 70% chance to include each example
                    text = template.format(code=code, description=description)
                    
                    # Find position of NAICS code in text
                    code_start = text.find(code)
                    if code_start != -1:
                        code_end = code_start + len(code)
                        training_data.append((
                            text, 
                            {"entities": [(code_start, code_end, "NAICS")]}
                        ))
        
        # PSC Code Training Examples
        psc_templates = [
            "Product Service Code {code} covers {description}",
            "PSC {code}: {description}",
            "Government procurement under PSC {code} for {description}",
            "Contract requires {code} certified vendors for {description}",
            "Service category PSC {code} - {description}", 
            "Federal acquisition of {code} services ({description})",
            "PSC Code: {code}",
            "Product code {code} encompasses {description}",
            "Supplies under PSC {code} include {description}",
            "Services classification {code} covers {description}",
            "The RFP specifies PSC code {code}",
            "Contract vehicle for {code} - {description}",
            "SEWP contract covers PSC {code}",
            "GSA Schedule for {code} services"
        ]
        
        # Generate PSC training examples
        for code, description in psc_codes.items():
            for template in psc_templates[:8]:  # Use subset to avoid overfitting
                if random.random() < 0.7:  # 70% chance to include each example
                    text = template.format(code=code, description=description)
                    
                    # Find position of PSC code in text
                    code_start = text.find(code)
                    if code_start != -1:
                        code_end = code_start + len(code)
                        training_data.append((
                            text,
                            {"entities": [(code_start, code_end, "PSC")]}
                        ))
        
        # Mixed examples with both NAICS and PSC
        mixed_examples = [
            ("The contractor specializes in NAICS 541511 services and has experience with PSC 7030 requirements", 
             {"entities": [(35, 41, "NAICS"), (85, 89, "PSC")]}),
            
            ("Small business under NAICS code 541512 seeking PSC D302 opportunities",
             {"entities": [(32, 38, "NAICS"), (54, 58, "PSC")]}),
            
            ("RFP for PSC 7035 services, open to NAICS 541513 classified businesses",
             {"entities": [(8, 12, "PSC"), (36, 42, "NAICS")]}),
            
            ("Contract combines NAICS 518210 data services with PSC R425 engineering support",
             {"entities": [(18, 24, "NAICS"), (52, 56, "PSC")]}),
            
            ("Vendor capabilities: NAICS 334111, PSC codes 7030 and D307",
             {"entities": [(21, 27, "NAICS"), (40, 44, "PSC"), (49, 53, "PSC")]}),
        ]
        
        training_data.extend(mixed_examples)
        
        # Add negative examples (text without codes) for better training
        negative_examples = [
            ("The company provides excellent software development services", {"entities": []}),
            ("Government contracting requires careful attention to regulations", {"entities": []}),
            ("Small business administration supports veteran-owned enterprises", {"entities": []}),
            ("Information technology solutions for federal agencies", {"entities": []}),
            ("Professional consulting services available nationwide", {"entities": []}),
        ]
        
        training_data.extend(negative_examples)
        
        print(f"✅ Generated {len(training_data)} training examples")
        print(f"   📋 NAICS examples: ~{len(naics_codes) * 6}")
        print(f"   📋 PSC examples: ~{len(psc_codes) * 6}")  
        print(f"   📋 Mixed examples: {len(mixed_examples)}")
        print(f"   📋 Negative examples: {len(negative_examples)}")
        
        return training_data
    
    def train_model(self, training_data, iterations=50):
        """
        Train the model to recognize NAICS and PSC codes
        """
        print(f"\n🎓 Training model for {iterations} iterations...")
        print("Training specialized model for government/business codes...")
        
        # Initialize the model
        self.nlp.begin_training()
        
        # Training loop
        for iteration in range(iterations):
            random.shuffle(training_data)
            losses = {}
            
            # Process in batches
            for batch in minibatch(training_data, size=8):
                examples = []
                for text, annotations in batch:
                    doc = self.nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    examples.append(example)
                
                self.nlp.update(examples, losses=losses)
            
            # Progress reporting
            if iteration % 10 == 0:
                print(f"  Iteration {iteration + 1}/{iterations} - Loss: {losses.get('ner', 0):.4f}")
        
        print("✅ Training completed!")
    
    def create_validation_patterns(self):
        """
        Create regex patterns to validate detected codes
        """
        patterns = {
            "NAICS": re.compile(r'^\d{6}$'),  # Exactly 6 digits
            "PSC": re.compile(r'^[A-Z0-9]{4}$')  # 4 alphanumeric characters
        }
        return patterns
    
    def validate_entity(self, entity_text, entity_label):
        """
        Validate that detected entities match expected patterns
        """
        patterns = self.create_validation_patterns()
        
        if entity_label in patterns:
            return patterns[entity_label].match(entity_text.strip())
        return True
    
    def test_model(self, test_texts):
        """
        Test the trained model with validation
        """
        print("\n🧪 TESTING NAICS/PSC CODE RECOGNITION")
        print("=" * 80)
        
        total_entities = 0
        valid_entities = 0
        
        for text in test_texts:
            doc = self.nlp(text)
            print(f"\n📄 Text: '{text}'")
            
            if doc.ents:
                print("   🎯 Detected Codes:")
                for ent in doc.ents:
                    is_valid = self.validate_entity(ent.text, ent.label_)
                    validity_mark = "✅" if is_valid else "❌"
                    
                    # Get description if available
                    description = ""
                    if ent.label_ == "NAICS" and ent.text in self.naics_db:
                        description = f" ({self.naics_db[ent.text]})"
                    elif ent.label_ == "PSC" and ent.text in self.psc_db:
                        description = f" ({self.psc_db[ent.text]})"
                    
                    print(f"      {validity_mark} {ent.label_}: '{ent.text}'{description}")
                    
                    total_entities += 1
                    if is_valid:
                        valid_entities += 1
            else:
                print("   ℹ️  No codes detected")
        
        # Summary statistics
        print(f"\n📊 VALIDATION SUMMARY:")
        print(f"   Total entities detected: {total_entities}")
        print(f"   Valid entities: {valid_entities}")
        if total_entities > 0:
            accuracy = (valid_entities / total_entities) * 100
            print(f"   Validation accuracy: {accuracy:.1f}%")
        print("=" * 80)
    
    def save_model_with_metadata(self, path="./naics_psc_model"):
        """
        Save model with metadata about codes
        """
        print(f"💾 Saving NAICS/PSC model to {path}...")
        
        # Save the model
        Path(path).mkdir(exist_ok=True)
        self.nlp.to_disk(path)
        
        # Save code databases as metadata
        metadata = {
            "model_type": "NAICS_PSC_Recognition",
            "entities": ["NAICS", "PSC"],
            "naics_codes": self.naics_db,
            "psc_codes": self.psc_db,
            "validation_patterns": {
                "NAICS": "6 digits (e.g., 541511)",
                "PSC": "4 alphanumeric characters (e.g., 7030, D302)"
            }
        }
        
        with open(f"{path}/metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Model and metadata saved successfully!")
        print(f"📁 Model files saved to: {path}")
    
    def load_model_with_metadata(self, path="./naics_psc_model"):
        """
        Load model with metadata
        """
        print(f"📂 Loading NAICS/PSC model from {path}...")
        
        try:
            self.nlp = spacy.load(path)
            
            # Load metadata
            metadata_path = f"{path}/metadata.json"
            if Path(metadata_path).exists():
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                self.naics_db = metadata.get("naics_codes", {})
                self.psc_db = metadata.get("psc_codes", {})
                print("✅ Model and metadata loaded successfully!")
            else:
                print("⚠️ Model loaded, but metadata not found")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")

def demonstrate_naics_psc_training():
    """
    Complete demonstration of NAICS/PSC code recognition training
    """
    print("🏛️ NAICS AND PSC CODE RECOGNITION TRAINING")
    print("=" * 80)
    print("Training AI to recognize:")
    print("📊 NAICS: North American Industry Classification System codes")
    print("🛒 PSC: Product Service Codes for government procurement")
    print("=" * 80)
    
    # Initialize trainer
    trainer = NAICSPSCTrainer()
    
    # Generate training data
    training_data = trainer.generate_training_data()
    
    # Train the model
    trainer.train_model(training_data, iterations=40)
    
    # Comprehensive test cases
    test_cases = [
        # NAICS code examples
        "The contractor operates under NAICS code 541511 for custom programming",
        "Primary business classification is NAICS 334111 for computer manufacturing",
        "Small business set-aside for NAICS code 722511 restaurants",
        
        # PSC code examples  
        "RFP requires PSC 7030 software development services",
        "Government contract for PSC D302 IT solutions",
        "Procurement under Product Service Code R425 for engineering",
        
        # Mixed examples
        "Vendor with NAICS 541512 experience seeks PSC 7035 opportunities",
        "Contract combines NAICS 518210 services with PSC codes 7030 and D307",
        "The RFP specifies NAICS code 541513 and PSC R408 requirements",
        
        # Edge cases
        "NAICS: 484110 and PSC: 5945 for transportation equipment",
        "Invalid code 12345 should not be detected as NAICS",
        "PSC XYZ1 and NAICS 999999 are not valid format",
        
        # Real-world examples
        "Boeing operates under NAICS 336411 for aircraft manufacturing and targets PSC W152 contracts",
        "IT contractor certified for NAICS 541519 and experienced with PSC 7045 training services",
        "The solicitation is open to businesses classified under NAICS 541330 with PSC C211 capabilities"
    ]
    
    # Test the model
    trainer.test_model(test_cases)
    
    # Save the trained model
    trainer.save_model_with_metadata()
    
    print("\n🎉 TRAINING COMPLETE!")
    print("\nYour model can now recognize:")
    print("✅ NAICS codes: 6-digit business classification codes")
    print("✅ PSC codes: 4-character government product/service codes") 
    print("✅ Validates code formats automatically")
    print("✅ Includes database of real codes with descriptions")
    
    return trainer

def quick_usage_example():
    """
    Quick example showing how to use the trained model
    """
    print("\n" + "="*60)
    print("QUICK USAGE EXAMPLE")
    print("="*60)
    
    # Train a simple model
    trainer = NAICSPSCTrainer()
    training_data = trainer.generate_training_data()
    trainer.train_model(training_data[:100], iterations=20)  # Quick training
    
    # Test on sample business text
    business_text = """
    Our company is classified under NAICS code 541511 for custom computer 
    programming services. We have extensive experience with government 
    contracts, particularly PSC 7030 software development and PSC D302 
    IT solutions. We also work with NAICS 541512 system design projects.
    """
    
    print("Analyzing business text for NAICS and PSC codes...")
    trainer.test_model([business_text])
    
if __name__ == "__main__":
    print("Choose training mode:")
    print("1. Complete demonstration (recommended)")
    print("2. Quick usage example")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "2":
        quick_usage_example()
    else:
        trainer = demonstrate_naics_psc_training()
    
    print("\n🚀 NEXT STEPS:")
    print("1. Use the trained model to analyze business documents")
    print("2. Add more NAICS/PSC codes to the training database") 
    print("3. Fine-tune with domain-specific text (contracts, RFPs)")
    print("4. Integrate with document processing pipelines")
    print("\nYou now have a specialized NLP model for government/business codes! 🎯")