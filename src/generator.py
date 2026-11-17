import json
import logging
from pathlib import Path
from typing import List, Literal
from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class ExtractionOutput(BaseModel):
    vendor_name: str = Field(..., description="Name of the vendor extracted from the document.")
    invoice_date: str = Field(..., description="Date of the invoice in YYYY-MM-DD format.")
    total_amount: float = Field(..., ge=0.0, description="Total monetary amount.")
    category: Literal["Software", "Hardware", "Services", "Travel"] = Field(..., description="Expense category.")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Model's self-assessed confidence.")

class TrainingRecord(BaseModel):
    input_text: str
    output_json: ExtractionOutput

def process_real_traffic_dataset(raw_inputs: List[str], output_path: str):
    """
    Ensures training data is ingested strictly from real production input distributions
    rather than synthetic prompts to prevent OOD failure.
    """
    logger.info("Processing real historical inputs through teacher...")
