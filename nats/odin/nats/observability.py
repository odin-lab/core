from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracing(module_name: str):
    resource = Resource.create({"service.name": module_name})
    trace.set_tracer_provider(TracerProvider(resource=resource))

    span_processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint="http://localhost:4318/v1/traces",
        )
    )
    trace.get_tracer_provider().add_span_processor(span_processor)
