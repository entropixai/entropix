"""Tests for agent adapters."""

import pytest


class TestHTTPAgentAdapter:
    """Tests for HTTP agent adapter."""

    def test_adapter_creation(self):
        """Test adapter can be created."""
        from flakestorm.core.protocol import HTTPAgentAdapter

        adapter = HTTPAgentAdapter(
            endpoint="http://localhost:8000/chat",
            timeout=30000,  # 30 seconds in milliseconds
        )
        assert adapter is not None
        assert adapter.endpoint == "http://localhost:8000/chat"

    def test_adapter_has_invoke_method(self):
        """Adapter has invoke method."""
        from flakestorm.core.protocol import HTTPAgentAdapter

        adapter = HTTPAgentAdapter(endpoint="http://localhost:8000/chat")
        assert hasattr(adapter, "invoke")
        assert callable(adapter.invoke)

    def test_timeout_conversion(self):
        """Timeout is converted to seconds."""
        from flakestorm.core.protocol import HTTPAgentAdapter

        adapter = HTTPAgentAdapter(
            endpoint="http://localhost:8000/chat",
            timeout=30000,
        )
        # Timeout should be stored in seconds
        assert adapter.timeout == 30.0

    def test_custom_headers(self):
        """Custom headers can be set."""
        from flakestorm.core.protocol import HTTPAgentAdapter

        headers = {"Authorization": "Bearer token123"}
        adapter = HTTPAgentAdapter(
            endpoint="http://localhost:8000/chat",
            headers=headers,
        )
        assert adapter.headers == headers


class TestPythonAgentAdapter:
    """Tests for Python function adapter."""

    def test_adapter_creation_with_callable(self):
        """Test adapter can be created with a callable."""
        from flakestorm.core.protocol import PythonAgentAdapter

        def my_agent(input: str) -> str:
            return f"Response to: {input}"

        adapter = PythonAgentAdapter(my_agent)
        assert adapter is not None
        assert adapter.agent == my_agent

    def test_adapter_has_invoke_method(self):
        """Adapter has invoke method."""
        from flakestorm.core.protocol import PythonAgentAdapter

        def my_agent(input: str) -> str:
            return f"Response to: {input}"

        adapter = PythonAgentAdapter(my_agent)
        assert hasattr(adapter, "invoke")
        assert callable(adapter.invoke)


class TestLangChainAgentAdapter:
    """Tests for LangChain agent adapter."""

    @pytest.fixture
    def langchain_config(self):
        """Create a test LangChain agent config."""
        from flakestorm.core.config import AgentConfig, AgentType

        return AgentConfig(
            endpoint="my_agent:chain",
            type=AgentType.LANGCHAIN,
            timeout=60000,  # 60 seconds in milliseconds
        )

    def test_adapter_creation(self, langchain_config):
        """Test adapter can be created."""
        from flakestorm.core.protocol import LangChainAgentAdapter

        adapter = LangChainAgentAdapter(langchain_config)
        assert adapter is not None


class TestAgentAdapterFactory:
    """Tests for adapter factory function."""

    def test_creates_http_adapter(self):
        """Factory creates HTTP adapter for HTTP type."""
        from flakestorm.core.config import AgentConfig, AgentType
        from flakestorm.core.protocol import HTTPAgentAdapter, create_agent_adapter

        config = AgentConfig(
            endpoint="http://localhost:8000/chat",
            type=AgentType.HTTP,
        )
        adapter = create_agent_adapter(config)
        assert isinstance(adapter, HTTPAgentAdapter)

    def test_creates_python_adapter(self):
        """Python adapter can be created with a callable."""
        from flakestorm.core.protocol import PythonAgentAdapter

        def my_agent(input: str) -> str:
            return f"Response: {input}"

        adapter = PythonAgentAdapter(my_agent)
        assert isinstance(adapter, PythonAgentAdapter)

    def test_creates_langchain_adapter(self):
        """Factory creates LangChain adapter for LangChain type."""
        from flakestorm.core.config import AgentConfig, AgentType
        from flakestorm.core.protocol import LangChainAgentAdapter, create_agent_adapter

        config = AgentConfig(
            endpoint="my_agent:chain",
            type=AgentType.LANGCHAIN,
        )
        adapter = create_agent_adapter(config)
        assert isinstance(adapter, LangChainAgentAdapter)


class TestAgentResponse:
    """Tests for AgentResponse data class."""

    def test_response_creation(self):
        """Test AgentResponse can be created."""
        from flakestorm.core.protocol import AgentResponse

        response = AgentResponse(
            output="Hello, world!",
            latency_ms=150.5,
        )
        assert response.output == "Hello, world!"
        assert response.latency_ms == 150.5

    def test_response_with_error(self):
        """Test AgentResponse with error."""
        from flakestorm.core.protocol import AgentResponse

        response = AgentResponse(
            output="",
            latency_ms=100.0,
            error="Connection timeout",
        )
        assert response.error == "Connection timeout"
        assert not response.success

    def test_response_success_property(self):
        """Test AgentResponse success property."""
        from flakestorm.core.protocol import AgentResponse

        # Success case
        success_response = AgentResponse(
            output="Response",
            latency_ms=100.0,
        )
        assert success_response.success is True

        # Error case
        error_response = AgentResponse(
            output="",
            latency_ms=100.0,
            error="Failed",
        )
        assert error_response.success is False
