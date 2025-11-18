"""
Code Analyzer - Advanced code analysis for multiple languages
"""

import logging
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class CodeAnalyzer:
    """Analyzes code for quality, security, and structure"""

    def __init__(self):
        self.file_patterns = {
            "python": r"\.py$",
            "javascript": r"\.(js|jsx)$",
            "typescript": r"\.(ts|tsx)$",
            "java": r"\.java$",
            "cpp": r"\.(cpp|cc|cxx|h|hpp)$",
            "c": r"\.(c|h)$",
            "go": r"\.go$",
            "rust": r"\.rs$",
            "sql": r"\.sql$",
            "html": r"\.html?$",
            "css": r"\.css$",
            "json": r"\.json$",
            "yaml": r"\.(yml|yaml)$",
        }

    async def analyze(self, code: str, filename: str = "unknown") -> Dict[str, Any]:
        """Analyze single code file"""
        logger.info(f"Analyzing {filename}...")

        language = self._detect_language(filename)

        analysis = {
            "filename": filename,
            "language": language,
            "metrics": self._calculate_metrics(code),
            "issues": self._find_issues(code, language),
            "quality_score": 0,
            "suggestions": self._get_suggestions(code, language),
            "summary": ""
        }

        # Calculate quality score
        analysis["quality_score"] = self._calculate_quality_score(analysis)
        analysis["summary"] = self._generate_summary(analysis)

        return analysis

    async def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze entire project"""
        logger.info(f"Analyzing project: {project_path}")

        path = Path(project_path)
        if not path.exists():
            return {"status": "error", "message": f"Path not found: {project_path}"}

        files_analyzed = 0
        total_lines = 0
        issues_found = []
        language_breakdown = {}

        for file_path in path.rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    analysis = await self.analyze(content, file_path.name)
                    files_analyzed += 1
                    total_lines += len(content.split('\n'))

                    language = analysis["language"]
                    if language not in language_breakdown:
                        language_breakdown[language] = 0
                    language_breakdown[language] += 1

                    # Collect issues
                    for issue in analysis["issues"]:
                        issue["file"] = str(file_path)
                        issues_found.append(issue)

                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {str(e)}")

        return {
            "status": "success",
            "project_path": project_path,
            "summary": {
                "files_analyzed": files_analyzed,
                "total_lines": total_lines,
                "languages": language_breakdown,
                "total_issues": len(issues_found),
            },
            "issues": issues_found,
            "recommendations": self._generate_project_recommendations(
                files_analyzed, total_lines, issues_found
            )
        }

    def _detect_language(self, filename: str) -> str:
        """Detect programming language from filename"""
        filename_lower = filename.lower()

        for lang, pattern in self.file_patterns.items():
            if re.search(pattern, filename_lower):
                return lang

        return "unknown"

    def _is_code_file(self, file_path: Path) -> bool:
        """Check if file is a code file"""
        return self._detect_language(file_path.name) != "unknown"

    def _calculate_metrics(self, code: str) -> Dict[str, Any]:
        """Calculate code metrics"""
        lines = code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        comment_lines = [l for l in lines if l.strip().startswith(('#', '//', '/*'))]

        return {
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_lines": len(comment_lines),
            "comment_ratio": len(comment_lines) / max(len(lines), 1),
            "average_line_length": sum(len(l) for l in lines) / max(len(lines), 1),
            "longest_line": max(len(l) for l in lines) if lines else 0,
        }

    def _find_issues(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Find issues in code"""
        issues = []

        lines = code.split('\n')

        for idx, line in enumerate(lines, 1):
            # Check for TODO/FIXME comments
            if "TODO" in line or "FIXME" in line:
                issues.append({
                    "line": idx,
                    "type": "todo",
                    "severity": "info",
                    "message": line.strip()[:50]
                })

            # Check for debugging statements
            if any(x in line.lower() for x in ["print(", "console.log", "println"]):
                issues.append({
                    "line": idx,
                    "type": "debug_statement",
                    "severity": "warning",
                    "message": "Debug statement found"
                })

            # Check for hardcoded passwords/secrets
            if any(x in line.lower() for x in ["password=", "apikey=", "secret="]):
                issues.append({
                    "line": idx,
                    "type": "security",
                    "severity": "critical",
                    "message": "Potential hardcoded secret detected"
                })

            # Check line length
            if len(line) > 120:
                issues.append({
                    "line": idx,
                    "type": "line_too_long",
                    "severity": "info",
                    "message": f"Line length: {len(line)} characters"
                })

        return issues

    def _get_suggestions(self, code: str, language: str) -> List[str]:
        """Generate code improvement suggestions"""
        suggestions = []

        if len(code.split('\n')) > 500:
            suggestions.append("Consider breaking this file into smaller modules")

        if "import " in code and code.count("import ") > 20:
            suggestions.append("Many imports detected - consider code organization")

        if '"""' not in code and "'''" not in code and language == "python":
            suggestions.append("Add docstrings to your functions and classes")

        if code.count("TODO") > 3:
            suggestions.append("Multiple TODO items - consider addressing technical debt")

        return suggestions

    def _calculate_quality_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall code quality score (0-100)"""
        score = 100.0

        # Deduct for issues
        critical_issues = len([i for i in analysis["issues"] if i.get("severity") == "critical"])
        warning_issues = len([i for i in analysis["issues"] if i.get("severity") == "warning"])
        info_issues = len([i for i in analysis["issues"] if i.get("severity") == "info"])

        score -= critical_issues * 10
        score -= warning_issues * 3
        score -= info_issues * 1

        # Bonus for documentation
        metrics = analysis["metrics"]
        if metrics["comment_ratio"] > 0.1:
            score += 5

        return max(0, min(100, score))

    def _generate_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate human-readable summary"""
        score = analysis["quality_score"]
        issues = len(analysis["issues"])

        if score >= 80:
            quality = "Good"
        elif score >= 60:
            quality = "Fair"
        elif score >= 40:
            quality = "Needs improvement"
        else:
            quality = "Poor"

        return f"{quality} code quality ({score:.0f}/100) with {issues} issues found"

    def _generate_project_recommendations(
        self,
        files: int,
        lines: int,
        issues: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate project-level recommendations"""
        recommendations = []

        critical_issues = [i for i in issues if i.get("severity") == "critical"]
        if critical_issues:
            recommendations.append(
                f"Address {len(critical_issues)} critical security issues immediately"
            )

        if lines > 100000:
            recommendations.append("Large codebase - consider refactoring and modularization")

        if files > 500:
            recommendations.append("Many files detected - review project structure")

        return recommendations
