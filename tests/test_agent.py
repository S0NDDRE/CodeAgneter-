"""
Unit tests for AI Code Agent
"""

import pytest
import asyncio
from agent.core.agent import CodeAgent
from agent.analysis.code_analyzer import CodeAnalyzer
from agent.core.security import SecurityManager

class TestCodeAgent:
    """Test suite for CodeAgent"""

    @pytest.fixture
    def agent(self):
        """Create agent instance"""
        return CodeAgent()

    @pytest.mark.asyncio
    async def test_process_message(self, agent):
        """Test basic message processing"""
        response = await agent.process_message("Hello, can you help?")
        assert response is not None
        assert len(response) > 0

    @pytest.mark.asyncio
    async def test_bug_fix_request(self, agent):
        """Test bug fix request handling"""
        response = await agent.process_message("Fix this bug in my code")
        assert "Bug Fix" in response or "help" in response.lower()

    @pytest.mark.asyncio
    async def test_code_analysis_request(self, agent):
        """Test code analysis request"""
        response = await agent.process_message("Analyze this code")
        assert "Analysis" in response or "analyze" in response.lower()

    def test_conversation_history(self, agent):
        """Test conversation history tracking"""
        history = agent.get_conversation_history()
        assert isinstance(history, list)
        assert len(history) >= 0

    @pytest.mark.asyncio
    async def test_code_fixing(self, agent):
        """Test code fixing functionality"""
        code = "x=1\ny=2\nz=x+y"
        result = await agent.fix_code(code)
        assert result['status'] == 'success'
        assert 'fixed_code' in result
        assert 'issues' in result

    def test_language_detection(self, agent):
        """Test language detection"""
        assert agent.supported_languages['python']['ext'] == '.py'
        assert agent.supported_languages['javascript']['ext'] == '.js'

class TestCodeAnalyzer:
    """Test suite for CodeAnalyzer"""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return CodeAnalyzer()

    @pytest.mark.asyncio
    async def test_analyze_python_code(self, analyzer):
        """Test analyzing Python code"""
        code = """
def hello_world():
    print("Hello, World!")

hello_world()
"""
        result = await analyzer.analyze(code, "test.py")
        assert result['language'] == 'python'
        assert 'metrics' in result
        assert 'quality_score' in result

    @pytest.mark.asyncio
    async def test_detect_issues(self, analyzer):
        """Test issue detection"""
        code = """
import os
import sys
import json

data = open("file.txt")
x=1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17+18+19+20
"""
        result = await analyzer.analyze(code, "test.py")
        assert len(result['issues']) > 0

    @pytest.mark.asyncio
    async def test_quality_scoring(self, analyzer):
        """Test quality scoring"""
        good_code = """
def calculate(a, b):
    '''Calculate sum of two numbers'''
    return a + b

result = calculate(1, 2)
"""
        bad_code = """
def calculate(a,b):
    return a+b
x=calculate(1,2)
y=calculate(3,4)
z=calculate(5,6)
"""
        good_result = await analyzer.analyze(good_code)
        bad_result = await analyzer.analyze(bad_code)

        assert good_result['quality_score'] > bad_result['quality_score']

class TestSecurityManager:
    """Test suite for SecurityManager"""

    @pytest.fixture
    def security(self):
        """Create security manager instance"""
        return SecurityManager()

    def test_permission_check(self, security):
        """Test permission checking"""
        assert security.check_permission('read_files') == True
        assert security.check_permission('write_files') == False
        assert security.check_permission('unknown_action') == False

    def test_dangerous_code_detection(self, security):
        """Test dangerous code detection"""
        dangerous_code = "rm -rf /"
        safe_code = "print('hello')"

        assert security.is_safe_code(dangerous_code) == False
        assert security.is_safe_code(safe_code) == True

    def test_path_sanitization(self, security):
        """Test path sanitization"""
        path = "/home/user/../../sensitive"
        sanitized = security.sanitize_path(path)
        assert "../" not in sanitized

    def test_approval_request(self, security):
        """Test approval request"""
        result = security.request_approval("write_files", {
            "file": "test.py",
            "action": "write"
        })
        assert result['status'] == 'pending'
        assert result['requires_user_approval'] == True

class TestIntegration:
    """Integration tests"""

    @pytest.mark.asyncio
    async def test_full_analysis_workflow(self):
        """Test complete analysis workflow"""
        agent = CodeAgent()
        analyzer = CodeAnalyzer()
        security = SecurityManager()

        code = """
def process_user_input(user_data):
    query = "SELECT * FROM users WHERE id=" + user_data
    result = db.execute(query)
    return result
"""

        # Check security
        is_safe = security.is_safe_code(code)
        assert is_safe == False  # SQL injection risk

        # Analyze code
        analysis = await analyzer.analyze(code)
        assert len(analysis['issues']) > 0

        # Get agent response
        response = await agent.process_message("Review this code for security issues")
        assert response is not None

    @pytest.mark.asyncio
    async def test_multi_file_project_analysis(self):
        """Test analyzing multiple files"""
        analyzer = CodeAnalyzer()

        files = {
            "main.py": "def main(): pass",
            "utils.py": "def helper(): pass",
            "config.py": "CONFIG = {}"
        }

        results = []
        for filename, content in files.items():
            result = await analyzer.analyze(content, filename)
            results.append(result)

        assert len(results) == 3
        assert all('quality_score' in r for r in results)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
