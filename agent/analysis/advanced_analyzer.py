"""
Advanced Code Analyzer - Deep code analysis with pattern recognition
Supports performance analysis, security scanning, and complexity metrics
"""

import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict
import re

logger = logging.getLogger(__name__)

class AdvancedAnalyzer:
    """Advanced code analysis engine"""

    def __init__(self):
        self.complexity_patterns = {
            'nested_loops': r'for\s+.*\s+for\s+',
            'deep_recursion': r'def\s+\w+\(.*\):\s*.*\1\(',
            'large_function': r'def\s+\w+\([^)]*\):',
            'multiple_conditions': r'if.*and.*and.*or',
        }

        self.security_issues = {
            'sql_injection': r"execute\s*\(\s*['\"].*\$\{",
            'xss': r"innerHTML\s*=|dangerouslySetInnerHTML",
            'hardcoded_password': r'(password|pwd|secret|api[_-]?key)\s*=\s*["\']',
            'eval_usage': r'\beval\s*\(',
            'unsafe_pickle': r'pickle\.loads',
        }

        self.performance_issues = {
            'n_plus_one': r'for.*in.*:\s*.*query\(',
            'inefficient_sort': r'sorted\(.*key=lambda.*\)',
            'regex_in_loop': r'for.*:\s*.*re\.(search|match)',
            'string_concatenation': r'\+.*\+.*\+.*\+',
        }

    async def analyze_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity"""
        logger.info("Analyzing code complexity...")

        metrics = {
            'cyclomatic_complexity': self._calculate_cyclomatic_complexity(code),
            'nested_level': self._find_max_nesting_level(code),
            'function_count': self._count_functions(code),
            'class_count': self._count_classes(code),
            'average_function_length': self._calc_avg_function_length(code),
            'cognitive_complexity': self._calculate_cognitive_complexity(code)
        }

        return {
            'metrics': metrics,
            'complexity_level': self._assess_complexity(metrics),
            'recommendations': self._get_complexity_recommendations(metrics)
        }

    async def security_scan(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Scan code for security vulnerabilities"""
        logger.info("Scanning for security issues...")

        vulnerabilities = []

        for issue_type, pattern in self.security_issues.items():
            matches = re.finditer(pattern, code, re.MULTILINE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                vulnerabilities.append({
                    'type': issue_type,
                    'severity': 'critical',
                    'line': line_num,
                    'description': self._get_vulnerability_description(issue_type),
                    'recommendation': self._get_security_recommendation(issue_type)
                })

        return {
            'vulnerabilities_found': len(vulnerabilities),
            'vulnerabilities': vulnerabilities,
            'security_score': max(0, 100 - len(vulnerabilities) * 10),
            'overall_risk': self._assess_security_risk(len(vulnerabilities))
        }

    async def performance_analysis(self, code: str) -> Dict[str, Any]:
        """Analyze code for performance issues"""
        logger.info("Analyzing performance...")

        issues = []

        for issue_type, pattern in self.performance_issues.items():
            matches = re.finditer(pattern, code, re.MULTILINE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                issues.append({
                    'type': issue_type,
                    'severity': 'warning',
                    'line': line_num,
                    'description': self._get_performance_description(issue_type),
                    'optimization': self._get_optimization_tip(issue_type)
                })

        return {
            'performance_issues': len(issues),
            'issues': issues,
            'efficiency_rating': self._rate_efficiency(len(issues)),
            'optimization_opportunities': self._get_optimization_opportunities(code)
        }

    def _calculate_cyclomatic_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        keywords = ['if', 'elif', 'for', 'while', 'except', 'and', 'or']

        for keyword in keywords:
            complexity += len(re.findall(rf'\b{keyword}\b', code))

        return complexity

    def _find_max_nesting_level(self, code: str) -> int:
        """Find maximum nesting level"""
        max_indent = 0
        current_max = 0

        for line in code.split('\n'):
            indent = len(line) - len(line.lstrip())
            if line.strip():
                current_max = max(current_max, indent // 4)

        return current_max

    def _count_functions(self, code: str) -> int:
        """Count functions in code"""
        return len(re.findall(r'def\s+\w+\s*\(', code)) + \
               len(re.findall(r'function\s+\w+\s*\(', code))

    def _count_classes(self, code: str) -> int:
        """Count classes in code"""
        return len(re.findall(r'class\s+\w+', code))

    def _calc_avg_function_length(self, code: str) -> int:
        """Calculate average function length"""
        functions = re.split(r'def\s+\w+\s*\(', code)
        if len(functions) <= 1:
            return 0

        total_lines = sum(len(f.split('\n')) for f in functions[1:])
        return total_lines // (len(functions) - 1)

    def _calculate_cognitive_complexity(self, code: str) -> int:
        """Estimate cognitive complexity"""
        complexity = 0

        # Count decision points
        complexity += len(re.findall(r'\bif\b', code))
        complexity += len(re.findall(r'\belse\b', code))
        complexity += len(re.findall(r'\belif\b', code))
        complexity += len(re.findall(r'\bfor\b', code))
        complexity += len(re.findall(r'\bwhile\b', code))

        # Add nesting penalty
        max_nesting = self._find_max_nesting_level(code)
        complexity += max_nesting * 2

        return complexity

    def _assess_complexity(self, metrics: Dict) -> str:
        """Assess overall complexity level"""
        complexity_score = (
            metrics['cyclomatic_complexity'] * 0.3 +
            metrics['nested_level'] * 0.2 +
            metrics['cognitive_complexity'] * 0.5
        )

        if complexity_score > 50:
            return "Very High"
        elif complexity_score > 30:
            return "High"
        elif complexity_score > 15:
            return "Medium"
        else:
            return "Low"

    def _get_complexity_recommendations(self, metrics: Dict) -> List[str]:
        """Get recommendations for complexity reduction"""
        recommendations = []

        if metrics['cyclomatic_complexity'] > 10:
            recommendations.append("Break down complex functions into smaller ones")

        if metrics['nested_level'] > 4:
            recommendations.append("Reduce nesting depth - consider extracting logic")

        if metrics['average_function_length'] > 50:
            recommendations.append("Functions are too long - break them into smaller pieces")

        if metrics['cognitive_complexity'] > 30:
            recommendations.append("Consider refactoring for improved readability")

        return recommendations

    def _get_vulnerability_description(self, vuln_type: str) -> str:
        """Get description for vulnerability type"""
        descriptions = {
            'sql_injection': 'Potential SQL injection vulnerability - use parameterized queries',
            'xss': 'XSS vulnerability risk - sanitize user input',
            'hardcoded_password': 'Hardcoded credentials found - use environment variables',
            'eval_usage': 'eval() usage is dangerous - use safer alternatives',
            'unsafe_pickle': 'Unsafe pickle usage - validate pickle source'
        }
        return descriptions.get(vuln_type, 'Unknown vulnerability')

    def _get_security_recommendation(self, vuln_type: str) -> str:
        """Get security recommendation"""
        recommendations = {
            'sql_injection': 'Use parameterized queries (prepared statements)',
            'xss': 'Use templating libraries that auto-escape output',
            'hardcoded_password': 'Load credentials from environment variables or config files',
            'eval_usage': 'Use json.loads() or ast.literal_eval() instead',
            'unsafe_pickle': 'Use json for untrusted data, or sign pickled data'
        }
        return recommendations.get(vuln_type, 'Review and fix this issue')

    def _assess_security_risk(self, vuln_count: int) -> str:
        """Assess overall security risk"""
        if vuln_count == 0:
            return "Safe"
        elif vuln_count < 3:
            return "Low Risk"
        elif vuln_count < 7:
            return "Medium Risk"
        else:
            return "High Risk"

    def _get_performance_description(self, issue_type: str) -> str:
        """Get description for performance issue"""
        descriptions = {
            'n_plus_one': 'N+1 query problem - may cause performance degradation',
            'inefficient_sort': 'Inefficient sorting - consider better algorithm',
            'regex_in_loop': 'Regex compilation in loop - compile once outside',
            'string_concatenation': 'String concatenation in loop - use list join'
        }
        return descriptions.get(issue_type, 'Performance issue detected')

    def _get_optimization_tip(self, issue_type: str) -> str:
        """Get optimization tip"""
        tips = {
            'n_plus_one': 'Use batch queries or eager loading',
            'inefficient_sort': 'Use built-in sorting with proper comparators',
            'regex_in_loop': 'Compile regex pattern once, reuse in loop',
            'string_concatenation': 'Use "".join(list) instead of += in loops'
        }
        return tips.get(issue_type, 'Optimize this code')

    def _rate_efficiency(self, issue_count: int) -> str:
        """Rate code efficiency"""
        if issue_count == 0:
            return "Excellent"
        elif issue_count < 2:
            return "Good"
        elif issue_count < 5:
            return "Fair"
        else:
            return "Needs Optimization"

    def _get_optimization_opportunities(self, code: str) -> List[str]:
        """Suggest optimization opportunities"""
        opportunities = []

        if 'for' in code and 'if' in code:
            opportunities.append("List comprehensions can be faster than loops with conditions")

        if '==' in code and 'list' in code:
            opportunities.append("Consider using set for O(1) lookup instead of list")

        if 'sort' in code:
            opportunities.append("Verify sorting is necessary - it's O(n log n)")

        return opportunities
