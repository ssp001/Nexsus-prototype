import asyncio
import unittest
from unittest.mock import Mock

from app.document_processing.document_processing import DocumentProcessing


class DocumentProcessingTests(unittest.TestCase):
    def test_retrive_answer_returns_text_response(self):
        client = DocumentProcessing.__new__(DocumentProcessing)
        client.logging = type(
            "Logger",
            (),
            {"info": lambda *args, **kwargs: None,
                "error": lambda *args, **kwargs: None},
        )()
        client.client = type("Client", (), {})()
        client.client.chat_completions = Mock(
            return_value={"choices": [
                {"message": {"content": "hello from doc"}}]}
        )

        result = asyncio.run(client.retrive_answer("doc-123", "question"))

        self.assertEqual(result, "hello from doc")
