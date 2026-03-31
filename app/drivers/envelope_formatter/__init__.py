from typing import Dict

from app.interface.envelope_formatter import EnvelopeFormatterInterface
from app.settings import settings
from app.settings.envelope_formatter import EnvelopeFormatterBackend

envelope_formatters: Dict[EnvelopeFormatterBackend, EnvelopeFormatterInterface] = dict()

if settings.envelope_formatters.root.get(EnvelopeFormatterBackend.TOLL_FEATURE):
    from .toll_feature.envelope_formatter import TollFeatureEnvelopeFormatter

    envelope_formatters[EnvelopeFormatterBackend.TOLL_FEATURE] = (
        TollFeatureEnvelopeFormatter()
    )
if settings.envelope_formatters.root.get(EnvelopeFormatterBackend.DITTO_THING):
    from .ditto_thing.envelope_formatter import DittoThingEnvelopeFormatter

    envelope_formatters[EnvelopeFormatterBackend.DITTO_THING] = (
        DittoThingEnvelopeFormatter()
    )


def get_envelope_formatters() -> Dict[
    EnvelopeFormatterBackend, EnvelopeFormatterInterface
]:
    return envelope_formatters
