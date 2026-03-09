"""FastAPI wrapper for Catala-generated rules engine."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Rules Engine API",
    description="API for evaluating rules compiled from Catala legislative specifications.",
)


class IndividualInput(BaseModel):
    age: int
    income: float
    is_resident: bool


class BenefitResult(BaseModel):
    eligible: bool
    monthly_amount: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/evaluate/benefit-eligibility", response_model=BenefitResult)
def evaluate_benefit_eligibility(individual: IndividualInput) -> BenefitResult:
    """Evaluate benefit eligibility using Catala-compiled rules.

    Replace this stub with a call to the Catala-generated Python module
    once you have compiled your .catala_en files to Python.
    """
    try:
        # TODO: Replace with import from src.generated module once Catala
        # files are compiled. Example:
        #
        #   from src.generated.example_benefit import BenefitEligibility
        #   result = BenefitEligibility(individual=...)
        #
        # For now, this is a placeholder that mirrors the Catala rule logic.
        eligible = (
            individual.age >= 18
            and individual.income < 30_000
            and individual.is_resident
        )
        if individual.income < 15_000:
            monthly_amount = 500.0
        elif individual.income < 25_000:
            monthly_amount = 300.0
        else:
            monthly_amount = 150.0

        return BenefitResult(
            eligible=eligible,
            monthly_amount=monthly_amount if eligible else 0.0,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
