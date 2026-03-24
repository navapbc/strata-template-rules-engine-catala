"""OpenTelemetry configuration for distributed tracing and metrics."""

import os

from opentelemetry import metrics, trace
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


def configure_telemetry() -> None:
    """Configure OpenTelemetry tracing and metrics.

    Trace IDs are propagated via W3C TraceContext headers (traceparent / tracestate).
    Telemetry is exported via OTLP when OTEL_EXPORTER_OTLP_ENDPOINT is set.
    """
    service_name = os.getenv("OTEL_SERVICE_NAME", "{{ app_name }}")
    resource = Resource.create({SERVICE_NAME: service_name})

    _configure_tracing(resource)
    _configure_metrics(resource)
    _configure_propagator()


def _configure_tracing(resource: Resource) -> None:
    tracer_provider = TracerProvider(resource=resource)

    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if otlp_endpoint:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

    trace.set_tracer_provider(tracer_provider)


def _configure_metrics(resource: Resource) -> None:
    readers = []

    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if otlp_endpoint:
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

        readers.append(PeriodicExportingMetricReader(OTLPMetricExporter()))

    meter_provider = MeterProvider(resource=resource, metric_readers=readers)
    metrics.set_meter_provider(meter_provider)


def _configure_propagator() -> None:
    # W3C TraceContext carries trace-id/span-id; W3C Baggage carries key-value pairs.
    set_global_textmap(
        CompositePropagator(
            [
                TraceContextTextMapPropagator(),
                W3CBaggagePropagator(),
            ]
        )
    )
