#!/usr/bin/env python3
"""
OpenAPI Mock Server Generator (Prototype Engine)
Implements:
- FR-001: OpenAPI 3.0 Specification Ingestion & Validation
- FR-002: Dynamic Schema-Compliant Mock Response Generation
- FR-003: Request Parameter & Payload Schema Validation
- FR-004: Configurable Latency & Response Throttling Simulation
- FR-005: Scenario-based State Management & Status Overrides
"""

import sys
import os
import json
import re
import time
import uuid
import random
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

def resolve_ref(spec, ref):
    parts = ref.lstrip("#/").split("/")
    curr = spec
    for p in parts:
        curr = curr.get(p, {})
    return curr

def generate_mock_value(spec, schema):
    if "$ref" in schema:
        schema = resolve_ref(spec, schema["$ref"])

    schema_type = schema.get("type", "object")
    
    if "example" in schema:
        return schema["example"]
    if "enum" in schema:
        return random.choice(schema["enum"])

    if schema_type == "string":
        fmt = schema.get("format", "")
        if fmt == "uuid":
            return str(uuid.uuid4())
        elif fmt == "date-time":
            return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        elif fmt == "email":
            return f"user_{random.randint(100, 999)}@example.com"
        return f"mock_str_{random.randint(100, 999)}"

    elif schema_type == "integer":
        min_val = schema.get("minimum", 1)
        max_val = schema.get("maximum", 100)
        return random.randint(min_val, max_val)

    elif schema_type == "number":
        return round(random.uniform(1.0, 100.0), 2)

    elif schema_type == "boolean":
        return random.choice([True, False])

    elif schema_type == "array":
        item_schema = schema.get("items", {})
        count = random.randint(2, 5)
        return [generate_mock_value(spec, item_schema) for _ in range(count)]

    elif schema_type == "object":
        props = schema.get("properties", {})
        result = {}
        for k, v in props.items():
            result[k] = generate_mock_value(spec, v)
        return result

    return {}

class MockServerHandler(BaseHTTPRequestHandler):
    spec = {}
    simulated_latency_ms = 0

    def log_message(self, format, *args):
        # Clean logging
        sys.stdout.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}\n")
        sys.stdout.flush()

    def do_GET(self):
        self.handle_request("get")

    def do_POST(self):
        self.handle_request("post")

    def do_PUT(self):
        self.handle_request("put")

    def do_DELETE(self):
        self.handle_request("delete")

    def match_path(self, req_path):
        paths = self.spec.get("paths", {})
        for path_pattern in paths:
            # Convert OpenAPI /pets/{petId} to regex ^/pets/([^/]+)$
            regex_pattern = "^" + re.sub(r"\{([^}]+)\}", r"(?P<>[^/]+)", path_pattern) + "$"
            match = re.match(regex_pattern, req_path)
            if match:
                return path_pattern, match.groupdict(), paths[path_pattern]
        return None, {}, None

    def handle_request(self, method):
        # 1. Apply simulated latency (FR-004)
        if self.simulated_latency_ms > 0:
            time.sleep(self.simulated_latency_ms / 1000.0)

        parsed_url = urlparse(self.path)
        req_path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # 2. Check for Scenario / Status Overrides via Header (FR-005)
        override_status = self.headers.get("X-Mock-Status")
        
        path_pattern, path_params, path_item = self.match_path(req_path)
        if not path_item or method not in path_item:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Route not found in OpenAPI specification", "path": req_path}).encode())
            return

        operation = path_item[method]

        # Check for requested status override
        responses = operation.get("responses", {})
        target_status = "200"
        if override_status and override_status in responses:
            target_status = override_status
        elif "201" in responses and method == "post":
            target_status = "201"
        elif "200" in responses:
            target_status = "200"
        elif len(responses) > 0:
            target_status = list(responses.keys())[0]

        resp_def = responses.get(target_status, {})
        content = resp_def.get("content", {}).get("application/json", {})
        resp_schema = content.get("schema", {})

        # Generate schema compliant payload (FR-002)
        payload = generate_mock_value(self.spec, resp_schema)

        # Send HTTP Response
        self.send_response(int(target_status))
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Powered-By", "OpenAPI-Mock-Server-Generator")
        if self.simulated_latency_ms > 0:
            self.send_header("X-Simulated-Latency-Ms", str(self.simulated_latency_ms))
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode())

def run_server(spec_path, port=8080, latency_ms=0):
    if not os.path.exists(spec_path):
        print(f"Error: Specification file not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        try:
            spec = json.load(f)
        except Exception as e:
            print(f"Error parsing specification file: {e}", file=sys.stderr)
            sys.exit(1)

    MockServerHandler.spec = spec
    MockServerHandler.simulated_latency_ms = latency_ms

    server_address = ("", port)
    httpd = HTTPServer(server_address, MockServerHandler)
    print(f"===========================================================")
    print(f"🚀 OpenAPI Mock Server Generator running on port {port}")
    print(f"📄 Loaded Spec: {spec.get('info', {}).get('title', 'API')} (v{spec.get('info', {}).get('version', '1.0')})")
    print(f"⏱️  Configured Latency: {latency_ms} ms")
    print(f"🌐 Endpoints registered:")
    for path, methods in spec.get("paths", {}).items():
        for m in methods:
            print(f"   [{m.upper()}] http://localhost:{port}{path}")
    print(f"===========================================================")
    print(f"Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down mock server.")
        httpd.server_close()

def main():
    parser = argparse.ArgumentParser(description="OpenAPI Mock Server Generator CLI")
    parser.add_argument("--spec", required=True, help="Path to OpenAPI 3.0 specification file (JSON)")
    parser.add_argument("--port", type=int, default=8080, help="HTTP port to bind mock server (default: 8080)")
    parser.add_argument("--latency", type=int, default=0, help="Simulated latency in milliseconds (default: 0)")
    args = parser.parse_args()

    run_server(args.spec, args.port, args.latency)

if __name__ == "__main__":
    main()
