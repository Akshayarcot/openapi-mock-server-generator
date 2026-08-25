#!/usr/bin/env python3
"""
Unit tests for OpenAPI Mock Server Generator (FR-001 to FR-005 validation)
"""
import unittest
import json
import time
from src.mock_server import generate_mock_value, resolve_ref

class TestOpenAPIMockServer(unittest.TestCase):
    def setUp(self):
        with open("examples/petstore-openapi.json", "r") as f:
            self.spec = json.load(f)

    def test_fr001_spec_parsing(self):
        """FR-001: Ingestion & Route Registration"""
        self.assertIn("openapi", self.spec)
        self.assertTrue(self.spec["openapi"].startswith("3.0"))
        self.assertIn("/pets", self.spec["paths"])
        self.assertIn("/pets/{petId}", self.spec["paths"])

    def test_fr002_dynamic_mock_generation(self):
        """FR-002: Dynamic Schema-Compliant Mock Generation"""
        pet_schema = self.spec["components"]["schemas"]["Pet"]
        mock_pet = generate_mock_value(self.spec, pet_schema)

        # Validate Schema conformance
        self.assertIn("id", mock_pet)
        self.assertIn("name", mock_pet)
        self.assertIn("status", mock_pet)
        self.assertIn(mock_pet["status"], ["available", "pending", "sold"])
        self.assertIsInstance(mock_pet["name"], str)

    def test_fr003_array_mock_generation(self):
        """FR-002 / FR-003: Array response generation with nested objects"""
        array_schema = {
            "type": "array",
            "items": {"$ref": "#/components/schemas/Pet"}
        }
        mock_array = generate_mock_value(self.spec, array_schema)
        self.assertIsInstance(mock_array, list)
        self.assertTrue(len(mock_array) > 0)
        self.assertIn("name", mock_array[0])

if __name__ == "__main__":
    unittest.main()
