# Archkeel
# Copyright (c) 2026 Rapiddweller Asia Co., Ltd.
# SPDX-License-Identifier: MIT
"""Strict stdin/stdout entry point for the Python source collector."""

import sys

from archkeel.analyzer.bootstrap import is_direct_entrypoint
from archkeel.ir.facts_codec import decode_request, encode_response
from archkeel.ir.protocol import CollectionResponse, PythonCollectionPhase, PythonSettings

from .collect import collect, provider_sources


def main() -> int:
    request = decode_request(sys.stdin.buffer.read())
    if not isinstance(request.resolver, PythonSettings):
        raise ValueError("Python collector requires the Python resolver")
    facts = collect(request)
    providers = (
        provider_sources(request, facts)
        if request.resolver.phase is PythonCollectionPhase.PROVIDERS
        else ()
    )
    response = CollectionResponse(facts, request.protocol_version, providers)
    sys.stdout.buffer.write(encode_response(response))
    return 0


if is_direct_entrypoint(__name__):
    raise SystemExit(main())
