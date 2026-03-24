"""FastAPI wrapper for Catala-generated rules engine."""

import time

from opentelemetry import metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.generated.Paidleave import (
    LeaveBalanceIn,
    LeaveType,
    LeaveType_Code,
    LeavePeriod,
    leave_balance,
)
from src.generated.catala_runtime import Integer


app = FastAPI(
    title="Rules Engine API",
    description="API for evaluating rules compiled from Catala legislative specifications.",
)

FastAPIInstrumentor.instrument_app(app)

_meter = metrics.get_meter(__name__)
_evaluation_counter = _meter.create_counter(
    name="rules_engine.evaluations",
    unit="{evaluation}",
    description="Number of rule evaluations performed.",
)
_evaluation_duration = _meter.create_histogram(
    name="rules_engine.evaluation.duration",
    unit="ms",
    description="Duration of rule evaluations in milliseconds.",
)


class LeavePeriodInput(BaseModel):
    length_in_weeks: int


class LeaveBalanceInput(BaseModel):
    leave_type: str
    leave_periods: list[LeavePeriodInput]
    leave_taken_in_benefit_year: int
    total_leave_taken_all_types: int


class LeaveBalanceResult(BaseModel):
    max_entitlement: int
    leave_balance: int
    total_requested: int
    has_sufficient_leave_balance: bool


LEAVE_TYPE_MAP = {
    "medical_leave": LeaveType_Code.MedicalLeave,
    "bonding_leave": LeaveType_Code.BondingLeave,
    "care_for_family": LeaveType_Code.CareForFamily,
    "care_for_family_service_member": LeaveType_Code.CareForFamilyServiceMember,
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/evaluate/leave-balance", response_model=LeaveBalanceResult)
def evaluate_leave_balance(input: LeaveBalanceInput) -> LeaveBalanceResult:
    """Evaluate leave balance sufficiency using Catala-compiled rules."""
    leave_type_code = LEAVE_TYPE_MAP.get(input.leave_type)
    if leave_type_code is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid leave_type '{input.leave_type}'. "
            f"Must be one of: {', '.join(LEAVE_TYPE_MAP.keys())}",
        )

    metric_attrs = {"leave_type": input.leave_type}
    start_ms = time.monotonic() * 1000
    try:
        catala_leave_type = LeaveType(code=leave_type_code, value=None)
        catala_periods = [
            LeavePeriod(length_in_weeks=Integer(p.length_in_weeks)) for p in input.leave_periods
        ]

        scope_result = leave_balance(
            LeaveBalanceIn(
                application_leave_type_in=catala_leave_type,
                leave_periods_in=catala_periods,
                leave_taken_in_benefit_year_in=Integer(input.leave_taken_in_benefit_year),
                total_leave_taken_all_types_in=Integer(input.total_leave_taken_all_types),
            )
        )

        result = LeaveBalanceResult(
            max_entitlement=int(scope_result.max_entitlement.value),
            leave_balance=int(scope_result.leave_balance.value),
            total_requested=int(scope_result.total_requested.value),
            has_sufficient_leave_balance=scope_result.has_sufficient_leave_balance,
        )
        _evaluation_counter.add(1, {**metric_attrs, "outcome": "success"})
        _evaluation_duration.record(time.monotonic() * 1000 - start_ms, metric_attrs)
        return result
    except Exception as e:
        _evaluation_counter.add(1, {**metric_attrs, "outcome": "error"})
        raise HTTPException(status_code=500, detail=str(e)) from e
