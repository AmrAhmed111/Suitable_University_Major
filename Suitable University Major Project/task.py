import tkinter as tk
from tkinter import ttk, messagebox
import clips
import os

class AcademicRecommenderSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Field Recommender System")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Initialize CLIPS environment
        self.env = clips.Environment()
        
        # Load knowledge base from external .clp file
        self.load_clips_knowledge_base()
        
        # Initialize questions
        self.questions = [
            "Do you enjoy solving complex mathematical problems?",
            "Are you interested in understanding how computers work at a fundamental level?",
            "Do you enjoy building websites or mobile applications?",
            "Are you fascinated by how data can be used to make predictions?",
            "Do you enjoy thinking about system security and potential vulnerabilities?",
            "Do you prefer working with practical applications over theoretical concepts?",
            "Are you interested in developing intelligent systems that can learn from data?",
            "Do you enjoy learning about network protocols and system architecture?",
            "Are you comfortable with programming?",
            "Do you enjoy working with databases and data structures?"
        ]
        self.setup_ui()
        
        self.answers = {}
        self.current_question = 0
        self.show_question()
    
    def load_clips_knowledge_base(self):
        """Load the CLIPS knowledge base from knowledge_base.clp file"""
        try:
            # Check if the file exists
            if os.path.exists("E:/Expert system task/knowledge_base.clp"):
                self.env.load("E:/Expert system task/knowledge_base.clp")
                print("Successfully loaded knowledge base from file")
            else:
                messagebox.showerror("Error", "knowledge_base.clp file not found. Make sure it's in the same directory as this script.")
                raise FileNotFoundError("knowledge_base.clp not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CLIPS knowledge base: {str(e)}")
            raise
    
    def setup_ui(self):
        # Title frame
        self.title_frame = tk.Frame(self.root, padx=10, pady=10)
        self.title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(self.title_frame, text="Academic Field Recommender System", 
                            font=("Arial", 18, "bold"))
        title_label.pack()
        
        subtitle_label = tk.Label(self.title_frame, 
                                text="Find your best fit: IT, Computer Science, Cyber Security, or AI",
                                font=("Arial", 12))
        subtitle_label.pack(pady=5)
        
        # Main content frame
        self.content_frame = tk.Frame(self.root, padx=20, pady=20)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Question frame
        self.question_frame = tk.Frame(self.content_frame)
        self.question_frame.pack(fill=tk.BOTH, expand=True)
        
        self.question_label = tk.Label(self.question_frame, text="", 
                                    font=("Arial", 14), wraplength=700)
        self.question_label.pack(pady=20)
        
        # Answer frame
        self.answer_frame = tk.Frame(self.question_frame)
        self.answer_frame.pack(pady=20)
        
        self.scale = tk.Scale(self.answer_frame, from_=1, to=5, orient=tk.HORIZONTAL, 
                            length=400, tickinterval=1, showvalue=True,
                            label="Strongly Disagree (1) to Strongly Agree (5)")
        self.scale.pack()
        
        # Navigation buttons
        self.nav_frame = tk.Frame(self.content_frame)
        self.nav_frame.pack(fill=tk.X, pady=20)
        
        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.prev_question, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT)
        
        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.next_question)
        self.next_button.pack(side=tk.RIGHT)
        
        # Results frame (initially hidden)
        self.results_frame = tk.Frame(self.content_frame)
        
        # Progress bar
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                        maximum=len(self.questions))
        self.progress_bar.pack(fill=tk.X)
        
        self.progress_label = tk.Label(self.progress_frame, text="Question 1/" + str(len(self.questions)))
        self.progress_label.pack(pady=5)
    
    def show_question(self):
        if 0 <= self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.config(text=question)
            
            # Update progress
            self.progress_var.set(self.current_question + 1)
            self.progress_label.config(text=f"Question {self.current_question + 1}/{len(self.questions)}")
            
            # Set scale to previous answer if it exists
            if self.current_question in self.answers:
                self.scale.set(self.answers[self.current_question])
            else:
                self.scale.set(3)  # Default to neutral
            
            # Enable/disable navigation buttons
            self.prev_button.config(state=tk.NORMAL if self.current_question > 0 else tk.DISABLED)
            self.next_button.config(text="Next" if self.current_question < len(self.questions) - 1 else "Finish")
    
    def next_question(self):
        # Save current answer
        self.answers[self.current_question] = self.scale.get()
        
        # Move to next question or finish
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.show_question()
        else:
            self.analyze_answers()
    
    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.show_question()
    
    def analyze_answers(self):
        # Hide question frame and show results
        self.question_frame.pack_forget()
        self.nav_frame.pack_forget()
        
        # Map answers to CLIPS facts
        math_aptitude = self.answers[0]  # Math problems
        programming_interest = self.answers[8]  # Programming comfort
        security_interest = self.answers[4]  # Security interest
        ai_interest = self.answers[6]  # AI systems
        practical_preference = self.answers[5]  # Practical vs theoretical
        network_interest = self.answers[7]  # Network protocols
        web_mobile_interest = self.answers[2]  # Web/mobile apps
        data_interest = (self.answers[3] + self.answers[9]) // 2  # Data prediction + databases (avg)
        
        # Insert student fact into CLIPS using clipspy template
        try:
            template = self.env.find_template('student')
            fact = template.assert_fact(
    **{
        "math-aptitude": math_aptitude,
        "programming-interest": programming_interest,
        "security-interest": security_interest,
        "ai-interest": ai_interest,
        "practical-preference": practical_preference,
        "network-interest": network_interest,
        "web-mobile-interest": web_mobile_interest,
        "data-interest": data_interest
    }
)
            
            # Run CLIPS rules
            self.env.run()
            
            self.display_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")
    
    def display_results(self):
        # Get results
        fields = {
            "Computer Science": {
                "description": "Computer Science focuses on the theoretical foundations of computation and practical techniques for implementing computer systems.",
                "courses": ["Algorithms", "Data Structures", "Programming Languages", "Operating Systems", "Database Systems"],
                "careers": ["Software Developer", "System Architect", "Database Administrator", "Research Scientist"]
            },
            "Information Technology": {
                "description": "IT involves the application, implementation, and maintenance of computer systems, networks, and technology infrastructure.",
                "courses": ["Network Administration", "System Integration", "Web Development", "IT Project Management", "Technical Support"],
                "careers": ["Network Administrator", "System Administrator", "IT Support Specialist", "Web Developer"]
            },
            "Cyber Security": {
                "description": "Cyber Security specializes in protecting systems, networks, and data from digital attacks and unauthorized access.",
                "courses": ["Network Security", "Ethical Hacking", "Digital Forensics", "Security Risk Assessment", "Cryptography"],
                "careers": ["Security Analyst", "Penetration Tester", "Security Engineer", "Incident Responder"]
            },
            "Artificial Intelligence": {
                "description": "AI involves creating systems that can perform tasks requiring human intelligence, such as learning, reasoning, and decision-making.",
                "courses": ["Machine Learning", "Natural Language Processing", "Computer Vision", "Neural Networks", "Reinforcement Learning"],
                "careers": ["Machine Learning Engineer", "AI Researcher", "Data Scientist", "AI Systems Architect"]
            }
        }
        
        # Extract recommendations from CLIPS facts
        recommendations = []
        
        # Use clipspy's API to access facts
        for fact in self.env.facts():
            if fact.template.name == 'recommendation':
                field = fact['field']
                score = fact['score']
                confidence = fact['confidence'] if 'confidence' in fact else 0.0
                if field:
                    recommendations.append((field, score, confidence))
        
        # Sort recommendations by score
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        # Display results
        self.results_frame = tk.Frame(self.content_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        result_title = tk.Label(self.results_frame, text="Your Academic Field Recommendations", 
                            font=("Arial", 16, "bold"))
        result_title.pack(pady=10)
        
        # Create notebook for tabbed results
        notebook = ttk.Notebook(self.results_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # If no recommendations found, provide general advice
        if not recommendations:
            recommendations = [
                ("Computer Science", 0, 0.0),
                ("Information Technology", 0, 0.0),
                ("Cyber Security", 0, 0.0),
                ("Artificial Intelligence", 0, 0.0)
            ]
            
            no_match_label = tk.Label(self.results_frame, 
                                    text="Based on your answers, we couldn't make a strong recommendation.\nHere's information about all fields:",
                                    font=("Arial", 12))
            no_match_label.pack(before=notebook, pady=10)
        
        # Create a tab for each recommendation
        for field, score, confidence in recommendations:
            field_info = fields.get(field, {"description": "No information available", "courses": [], "careers": []})
            
            # Create frame for this field
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=field)
            
            # Field description
            desc_frame = ttk.LabelFrame(tab_frame, text="Overview")
            desc_frame.pack(fill=tk.X, padx=10, pady=10, expand=False)
            
            desc_label = tk.Label(desc_frame, text=field_info["description"], wraplength=700, justify=tk.LEFT)
            desc_label.pack(padx=10, pady=10, anchor=tk.W)
            
            # Score indicator if score > 0
            if score > 0:
                match_frame = ttk.LabelFrame(tab_frame, text="Match Score")
                match_frame.pack(fill=tk.X, padx=10, pady=10, expand=False)
                
                match_text = f"Your profile has a good match with {field}. Match score: {score}/15"
                if confidence > 0:
                    match_text += f" (Confidence: {confidence*100:.1f}%)"
                
                match_label = tk.Label(match_frame, text=match_text, wraplength=700)
                match_label.pack(padx=10, pady=10)
            
            # Common courses
            courses_frame = ttk.LabelFrame(tab_frame, text="Common Courses")
            courses_frame.pack(fill=tk.X, padx=10, pady=10, expand=False)
            
            for course in field_info["courses"]:
                course_label = tk.Label(courses_frame, text=f"• {course}", anchor=tk.W)
                course_label.pack(fill=tk.X, padx=10, anchor=tk.W)
            
            # Career paths
            careers_frame = ttk.LabelFrame(tab_frame, text="Potential Career Paths")
            careers_frame.pack(fill=tk.X, padx=10, pady=10, expand=False)
            
            for career in field_info["careers"]:
                career_label = tk.Label(careers_frame, text=f"• {career}", anchor=tk.W)
                career_label.pack(fill=tk.X, padx=10, anchor=tk.W)
        
        # Reset button
        reset_button = tk.Button(self.results_frame, text="Start Over", command=self.reset_system)
        reset_button.pack(pady=20)
    
    def reset_system(self):
        # Clear CLIPS environment
        self.env.clear()  # In clipspy, use clear() instead of reset()
        self.load_clips_knowledge_base()  # Reload the knowledge base
        
        # Reset UI
        self.results_frame.destroy()
        self.question_frame.pack(fill=tk.BOTH, expand=True)
        self.nav_frame.pack(fill=tk.X, pady=20)
        
        # Reset answers and questions
        self.answers = {}
        self.current_question = 0
        self.show_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicRecommenderSystem(root)
    root.mainloop()