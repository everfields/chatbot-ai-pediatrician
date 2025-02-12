from typing import Optional, List, Dict, Literal
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv
import urllib.parse

# Setup
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

# --------------------------------------------------------------
# Step 1: Define conversation state models
# --------------------------------------------------------------

class InitialAssessment(BaseModel):
    """Initial symptom assessment"""
    main_symptom: str = Field(description="Primary symptom reported by user")
    symptom_duration: str = Field(description="How long symptoms have persisted")
    fever_present: bool = Field(description="Whether fever is present")
    fever_temperature: Optional[float] = Field(description="Maximum temperature recorded")

class SymptomDetails(BaseModel):
    """Detailed symptom follow-up"""
    symptom_location: Optional[str] = Field(description="Location of symptoms on body")
    symptom_appearance: Optional[str] = Field(description="Visual characteristics")
    symptom_triggers: Optional[str] = Field(description="Factors that worsen symptoms")
    contact_with_sick: Optional[bool] = Field(description="Contact with sick individuals")

class PatientBackground(BaseModel):
    """Patient medical background"""
    age: float = Field(description="Patient age in years")
    weight: Optional[float] = Field(description="Patient weight in kilograms")
    chronic_conditions: List[str] = Field(description="Existing medical conditions")
    medications: List[str] = Field(description="Current medications")

class DiagnosisResult(BaseModel):
    """Final diagnosis output"""
    condition: str = Field(description="Diagnosed medical condition")
    urgency: Literal["emergency", "urgent_care", "routine", "monitor"] = Field(description="Required care level")
    confidence: float = Field(description="Diagnosis confidence score 0-1")
    red_flags: List[str] = Field(description="Danger signs to watch for")

class TreatmentPlan(BaseModel):
    """Recommended treatment plan"""
    medications: List[Dict[str, str]] = Field(description="Recommended medications with dosage")
    home_care: List[str] = Field(description="Home care instructions")
    follow_up: str = Field(description="Follow-up recommendations")

# --------------------------------------------------------------
# Step 2: Define workflow components
# --------------------------------------------------------------

class PediatricianWorkflow:
    def __init__(self):
        self.state = {}
        self.current_step = 0
        self.required_steps = [
            self.assess_initial_symptoms,
            self.gather_patient_background,
            self.detail_symptoms,
            self.perform_diagnosis,
            self.create_treatment_plan,
            self.generate_recommendations
        ]

    def generate_amazon_link(self, search_term: str) -> str:
        """Generate Amazon affiliate link for product recommendations"""
        encoded_term = urllib.parse.quote(search_term)
        return f"https://www.amazon.com/s?k={encoded_term}&tag=intelranking-20&linkCode=ll1&language=en_US"

    async def ask_question(self, prompt: str) -> str:
        """Simulated user input handler (replace with actual IO in production)"""
        return input(prompt)

    # --------------------------------------------------------------
    # Step 3: Define conversation steps
    # --------------------------------------------------------------

    async def assess_initial_symptoms(self):
        """Initial symptom assessment"""
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[{
                "role": "system",
                "content": "Generate the first question to assess the child's condition."
            }],
            response_format={"type": "text"}
        )
        question = completion.choices[0].message.content
        answer = await self.ask_question(question)
        
        # Parse structured data from response
        parse_completion = client.beta.chat.completions.parse(
            model=model,
            messages=[{
                "role": "system",
                "content": "Extract medical details from: " + answer
            }],
            response_format=InitialAssessment
        )
        self.state.update(parse_completion.choices[0].message.parsed.model_dump())

    async def gather_patient_background(self):
        """Collect patient medical history"""
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[{
                "role": "system",
                "content": f"Generate background questions based on: {self.state}"
            }],
            response_format={"type": "text"}
        )
        question = completion.choices[0].message.content
        answer = await self.ask_question(question)
        
        parse_completion = client.beta.chat.completions.parse(
            model=model,
            messages=[{
                "role": "system",
                "content": "Extract medical history from: " + answer
            }],
            response_format=PatientBackground
        )
        self.state.update(parse_completion.choices[0].message.parsed.model_dump())

    async def detail_symptoms(self):
        """Detailed symptom follow-up"""
        while True:
            completion = client.beta.chat.completions.parse(
                model=model,
                messages=[{
                    "role": "system",
                    "content": f"Generate next symptom question based on: {self.state}"
                }],
                response_format={"type": "text"}
            )
            question = completion.choices[0].message.content
            if "?" not in question:  # Stop condition
                break
                
            answer = await self.ask_question(question)
            parse_completion = client.beta.chat.completions.parse(
                model=model,
                messages=[{
                    "role": "system",
                    "content": "Extract symptom details from: " + answer
                }],
                response_format=SymptomDetails
            )
            self.state.update(parse_completion.choices[0].message.parsed.model_dump())

    # --------------------------------------------------------------
    # Step 4: Analysis and recommendations
    # --------------------------------------------------------------

    async def perform_diagnosis(self):
        """Generate final diagnosis"""
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[{
                "role": "system",
                "content": f"Diagnose based on: {self.state}"
            }],
            response_format=DiagnosisResult
        )
        self.diagnosis = completion.choices[0].message.parsed

    async def create_treatment_plan(self):
        """Generate treatment plan"""
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[{
                "role": "system",
                "content": f"Create treatment plan for {self.diagnosis.condition}"
            }],
            response_format=TreatmentPlan
        )
        self.treatment = completion.choices[0].message.parsed

    async def generate_recommendations(self):
        """Generate product recommendations"""
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[{
                "role": "system",
                "content": f"Suggest 3 Amazon product categories related to {self.state}"
            }],
            response_format={"type": "json_object"}
        )
        self.recommendations = [
            self.generate_amazon_link(product) 
            for product in completion.choices[0].message.content["products"]
        ]

    # --------------------------------------------------------------
    # Step 5: Main workflow execution
    # --------------------------------------------------------------

    async def run_workflow(self):
        """Execute full conversation workflow"""
        logger.info("Starting pediatric assessment workflow")
        
        for step in self.required_steps:
            await step()
            logger.info(f"Completed step: {step.__name__}")
        
        logger.info("Workflow completed successfully")
        return self.format_output()

    def format_output(self) -> str:
        """Format final output with markdown"""
        return f"""
**Diagnosis**
Condition: {self.diagnosis.condition}
Urgency: {self.diagnosis.urgency}
Confidence: {self.diagnosis.confidence:.0%}

**Treatment**
Medications:
{"".join(f"- {m['name']} ({m['dosage']}) {'(Prescription required)' if m['prescription'] else ''}\n" for m in self.treatment.medications)}

Home Care:
{"".join(f"- {item}\n" for item in self.treatment.home_care)}

**Product Recommendations**
{"".join(f"[{product}]({link}){{:target='_blank'}}\n\n" for product, link in self.recommendations)}
        """

# --------------------------------------------------------------
# Step 6: Example usage
# --------------------------------------------------------------

async def main():
    workflow = PediatricianWorkflow()
    result = await workflow.run_workflow()
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())