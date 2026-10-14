# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Compatible entry points for the IR wire-format codecs."""

from archkeel.ir.codec_contract import (
    CONTRACT_SCHEMA_VERSION as CONTRACT_SCHEMA_VERSION,
)
from archkeel.ir.codec_contract import (
    ContractVersionError as ContractVersionError,
)
from archkeel.ir.codec_contract import (
    _rule_payload as _rule_payload,
)
from archkeel.ir.codec_contract import (
    absent_contract_digest as absent_contract_digest,
)
from archkeel.ir.codec_contract import (
    contract_bytes as contract_bytes,
)
from archkeel.ir.codec_contract import (
    contract_digest as contract_digest,
)
from archkeel.ir.codec_contract import (
    parse_contract as parse_contract,
)
from archkeel.ir.codec_contract import (
    parse_required_component as parse_required_component,
)
from archkeel.ir.codec_delta import (
    delta_payload as delta_payload,
)
from archkeel.ir.codec_delta import (
    parse_delta as parse_delta,
)
from archkeel.ir.codec_governance import (
    absent_baseline_digest as absent_baseline_digest,
)
from archkeel.ir.codec_governance import (
    amendment_bytes as amendment_bytes,
)
from archkeel.ir.codec_governance import (
    baseline_bytes as baseline_bytes,
)
from archkeel.ir.codec_governance import (
    baseline_digest as baseline_digest,
)
from archkeel.ir.codec_governance import (
    parse_amendment as parse_amendment,
)
from archkeel.ir.codec_governance import (
    parse_baseline as parse_baseline,
)
from archkeel.ir.codec_governance import (
    parse_lock as parse_lock,
)
from archkeel.ir.codec_governance import (
    parse_measurements as parse_measurements,
)
from archkeel.ir.codec_governance import (
    parse_validation_baseline as parse_validation_baseline,
)
from archkeel.ir.codec_inside import (
    contract_provenance_paths as contract_provenance_paths,
)
from archkeel.ir.codec_inside import (
    declaration_paths as declaration_paths,
)
from archkeel.ir.codec_inside import (
    load_inside_contract_tree as load_inside_contract_tree,
)
from archkeel.ir.codec_observation import (
    canonical_report_bytes as canonical_report_bytes,
)
from archkeel.ir.codec_observation import (
    decode_canonical_model as decode_canonical_model,
)
from archkeel.ir.codec_observation import (
    encode_canonical_model as encode_canonical_model,
)
from archkeel.ir.codec_observation import (
    observation_payload as observation_payload,
)
from archkeel.ir.codec_observation import (
    parse_observation as parse_observation,
)
from archkeel.ir.codec_result import (
    _architecture_component_payload as _architecture_component_payload,
)
from archkeel.ir.codec_result import (
    result_bytes as result_bytes,
)
from archkeel.ir.codec_result import (
    result_payload as result_payload,
)
from archkeel.ir.codec_wire import (
    canonical_json_bytes as canonical_json_bytes,
)
from archkeel.ir.codec_wire import (
    decode_json as decode_json,
)
from archkeel.ir.codec_wire import (
    value_bytes as value_bytes,
)
from archkeel.ir.facts_codec import (
    parse_evidence as parse_evidence,
)
from archkeel.ir.facts_codec import (
    parse_record as parse_record,
)
from archkeel.ir.model import (
    ContractInputError as ContractInputError,
)
from archkeel.ir.model import (
    InsideContractIssue as InsideContractIssue,
)
from archkeel.ir.model import (
    InsideContractMount as InsideContractMount,
)
from archkeel.ir.model import (
    InsideContractTree as InsideContractTree,
)
from archkeel.ir.model import (
    RawJson as RawJson,
)

# Ordinary-module reexports need one literal declaration for proven facade routes.
__all__ = (
    "CONTRACT_SCHEMA_VERSION",
    "ContractInputError",
    "ContractVersionError",
    "InsideContractIssue",
    "InsideContractMount",
    "InsideContractTree",
    "RawJson",
    "absent_baseline_digest",
    "absent_contract_digest",
    "amendment_bytes",
    "baseline_bytes",
    "baseline_digest",
    "canonical_json_bytes",
    "canonical_report_bytes",
    "contract_bytes",
    "contract_digest",
    "contract_provenance_paths",
    "declaration_paths",
    "decode_canonical_model",
    "decode_json",
    "delta_payload",
    "encode_canonical_model",
    "load_inside_contract_tree",
    "observation_payload",
    "parse_amendment",
    "parse_baseline",
    "parse_contract",
    "parse_delta",
    "parse_evidence",
    "parse_lock",
    "parse_measurements",
    "parse_observation",
    "parse_record",
    "parse_required_component",
    "parse_validation_baseline",
    "result_bytes",
    "result_payload",
    "value_bytes",
)
