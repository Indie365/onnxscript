# DO NOT EDIT! This file was generated by jschema_to_python version 0.0.1.dev29,
# with extension for dataclasses and type annotation.

from __future__ import annotations

import dataclasses
from typing import List, Optional

from onnxscript.diagnostics.infra.sarif import (
    _artifact_location,
    _message,
    _property_bag,
    _rectangle,
    _region,
)


@dataclasses.dataclass
class Attachment:
    """An artifact relevant to a result."""

    artifact_location: _artifact_location.ArtifactLocation = dataclasses.field(
        metadata={"schema_property_name": "artifactLocation"}
    )
    description: Optional[_message.Message] = dataclasses.field(
        default=None, metadata={"schema_property_name": "description"}
    )
    properties: Optional[_property_bag.PropertyBag] = dataclasses.field(
        default=None, metadata={"schema_property_name": "properties"}
    )
    rectangles: Optional[List[_rectangle.Rectangle]] = dataclasses.field(
        default=None, metadata={"schema_property_name": "rectangles"}
    )
    regions: Optional[List[_region.Region]] = dataclasses.field(
        default=None, metadata={"schema_property_name": "regions"}
    )


# flake8: noqa
