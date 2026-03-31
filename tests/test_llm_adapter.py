import pytest
from src.llm.llm_adapter import LLMAdapter


class MockResponse:
    def __init__(self, text):
        self.output_text = text


class MockResponsesAPI:
    def __init__(self, text):
        self.text = text
        self.called = False
        self.last_input = None

    def create(self, model, input):
        self.called = True
        self.last_input = input
        return MockResponse(self.text)


class MockLLMClient:
    def __init__(self, response="SELECT name FROM pipelines"):
        self.responses = MockResponsesAPI(response)
    
class TestStep1_BuildPrompt:
    def test_prompt_contains_user_query(self):
        client = MockLLMClient()
        adapter = LLMAdapter(client)

        schema = {
            "pipelines": {
                "columns": {
                    "id": "INTEGER",
                    "name": "TEXT",
                    "daily_oil_flow": "INTEGER"
                }
            }
        }

        prompt = adapter.build_prompt("Show pipeline names", schema)

        assert "Show pipeline names" in prompt

    def test_prompt_contains_schema_information(self):
        client = MockLLMClient()
        adapter = LLMAdapter(client)

        schema = {
            "pipelines": {
                "columns": {
                    "id": "INTEGER",
                    "name": "TEXT",
                    "daily_oil_flow": "INTEGER"
                }
            }
        }

        prompt = adapter.build_prompt("Show pipeline names", schema)

        assert "pipelines" in prompt
        assert "id" in prompt
        assert "name" in prompt
        assert "daily_oil_flow" in prompt

class TestStep2_GenerateSQL:
    def test_generate_sql_calls_llm_client(self):
        client = MockLLMClient(response="SELECT name FROM pipelines")
        adapter = LLMAdapter(client)

        schema = {
            "pipelines": {
                "columns": {
                    "id": "INTEGER",
                    "name": "TEXT",
                    "daily_oil_flow": "INTEGER"
                }
            }
        }

        adapter.generate_sql("Show pipeline names", schema)

        assert client.responses.called is True

    def test_generate_sql_returns_llm_response(self):
        client = MockLLMClient(response="SELECT name FROM pipelines")
        adapter = LLMAdapter(client)

        schema = {
            "pipelines": {
                "columns": {
                    "id": "INTEGER",
                    "name": "TEXT",
                    "daily_oil_flow": "INTEGER"
                }
            }
        }

        result = adapter.generate_sql("Show pipeline names", schema)

        assert result == "SELECT name FROM pipelines"