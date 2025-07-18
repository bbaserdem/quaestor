"""Simplified template processor for rendering markdown templates with project data."""

import re
from pathlib import Path
from typing import Any

from quaestor.utils import detect_project_type, get_project_complexity_indicators, load_yaml


def get_project_data(project_dir: Path) -> dict[str, Any]:
    """Gather project-specific data for template rendering.

    Args:
        project_dir: Path to project directory

    Returns:
        Dictionary with project data for template processing
    """
    # Get basic project info
    project_type = detect_project_type(project_dir)
    complexity_info = get_project_complexity_indicators(project_dir, project_type)

    # Load language-specific configuration
    config_path = Path(__file__).parent.parent / "assets" / "configuration" / "languages.yaml"
    language_configs = load_yaml(config_path, {})

    # Get config for this project type, fallback to unknown
    lang_config = language_configs.get(project_type, language_configs.get("unknown", {}))

    # Calculate derived values
    strict_mode = complexity_info.get("total_files", 0) > 50 or complexity_info.get("max_directory_depth", 0) > 5
    project_name = project_dir.name

    # Combine all data
    return {
        "project_name": project_name,
        "project_type": project_type,
        "strict_mode": strict_mode,
        **lang_config,
        **complexity_info,
    }


def process_template(template_path: Path, project_data: dict[str, Any]) -> str:
    """Process a template file with project data using simple variable substitution.

    Args:
        template_path: Path to template file
        project_data: Project-specific data for substitution

    Returns:
        Processed template content
    """
    content = template_path.read_text(encoding="utf-8")

    # Process simple variable substitutions: {{ variable_name }}
    for key, value in project_data.items():
        if value is None:
            value = ""
        elif isinstance(value, bool):
            value = "true" if value else "false"

        # Replace {{ key }} patterns
        content = re.sub(rf"\{{\{{\s*{re.escape(key)}\s*\}}\}}", str(value), content)

    # Process conditional patterns
    content = _process_conditionals(content, project_data)

    # Clean up any remaining template variables
    content = re.sub(r"\{\{\s*[^}]+\s*\}\}", "", content)

    return content


def _process_conditionals(content: str, data: dict[str, Any]) -> str:
    """Process conditional template patterns.

    Args:
        content: Template content
        data: Project data

    Returns:
        Content with conditionals processed
    """
    # Pattern: {{ "text" if condition else "other" }}
    conditional_pattern = r'\{\{\s*"([^"]*?)"\s+if\s+(\w+)\s+else\s+"([^"]*?)"\s*\}\}'

    def replace_conditional(match):
        true_text = match.group(1)
        condition_var = match.group(2)
        false_text = match.group(3)

        condition_value = data.get(condition_var, False)
        if isinstance(condition_value, str):
            condition_value = condition_value.lower() in ("true", "1", "yes", "on")

        return true_text if condition_value else false_text

    content = re.sub(conditional_pattern, replace_conditional, content)

    # Pattern: {{ value if condition else "default" }}
    value_conditional_pattern = r'\{\{\s*(\w+)\s+if\s+(\w+)\s+else\s+"([^"]*?)"\s*\}\}'

    def replace_value_conditional(match):
        value_var = match.group(1)
        condition_var = match.group(2)
        default_text = match.group(3)

        condition_value = data.get(condition_var, False)
        if isinstance(condition_value, str):
            condition_value = condition_value.lower() in ("true", "1", "yes", "on")

        return str(data.get(value_var, "")) if condition_value else default_text

    content = re.sub(value_conditional_pattern, replace_value_conditional, content)

    # Handle specific patterns used in templates
    content = _process_specific_patterns(content, data)

    return content


def _process_specific_patterns(content: str, data: dict[str, Any]) -> str:
    """Process specific template patterns found in the codebase.

    Args:
        content: Template content
        data: Project data

    Returns:
        Content with specific patterns processed
    """
    # Handle coverage threshold patterns
    coverage_threshold = data.get("coverage_threshold")
    if coverage_threshold:
        # Pattern: {{ ">=" + coverage_threshold|string + "%" if coverage_threshold else "optional" }}
        content = re.sub(
            r'\{\{\s*">=" \+ coverage_threshold\|string \+ "%"\s+if\s+coverage_threshold\s+else\s+"optional"\s*\}\}',
            f">={coverage_threshold}%",
            content,
        )

        # Pattern: {{ coverage_threshold|string + "%" if coverage_threshold else "80%" }}
        content = re.sub(
            r'\{\{\s*coverage_threshold\|string \+ "%"\s+if\s+coverage_threshold\s+else\s+"80%"\s*\}\}',
            f"{coverage_threshold}%",
            content,
        )
    else:
        content = re.sub(
            r'\{\{\s*">=" \+ coverage_threshold\|string \+ "%"\s+if\s+coverage_threshold\s+else\s+"optional"\s*\}\}',
            "optional",
            content,
        )
        content = re.sub(
            r'\{\{\s*coverage_threshold\|string \+ "%"\s+if\s+coverage_threshold\s+else\s+"80%"\s*\}\}', "80%", content
        )

    # Handle project type specific patterns
    project_type = data.get("project_type", "unknown")

    # Pattern: {{ "true" if project_type == "web" else "false" }}
    is_web = "true" if project_type == "web" else "false"
    content = re.sub(r'\{\{\s*"true"\s+if\s+project_type\s*==\s*"web"\s+else\s+"false"\s*\}\}', is_web, content)

    # Handle performance target patterns
    performance_target = data.get("performance_target_ms", 200)
    content = re.sub(
        r'\{\{\s*performance_target_ms\s+if\s+performance_target_ms\s+else\s+"200"\s*\}\}',
        str(performance_target),
        content,
    )

    return content


def render_template_string(template_str: str, project_data: dict[str, Any]) -> str:
    """Render a template string with project data.

    Args:
        template_str: Template string content
        project_data: Project-specific data

    Returns:
        Rendered string
    """
    # Create a temporary file to use existing process_template function
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
        tf.write(template_str)
        temp_path = Path(tf.name)

    try:
        result = process_template(temp_path, project_data)
        return result
    finally:
        temp_path.unlink()


def validate_template(template_path: Path) -> tuple[bool, list[str]]:
    """Validate a template for common issues.

    Args:
        template_path: Path to template file

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    if not template_path.exists():
        errors.append(f"Template file does not exist: {template_path}")
        return False, errors

    try:
        content = template_path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"Cannot read template file: {e}")
        return False, errors

    # Check for common template issues

    # Unmatched braces
    open_braces = content.count("{{")
    close_braces = content.count("}}")
    if open_braces != close_braces:
        errors.append(f"Unmatched template braces: {open_braces} opening, {close_braces} closing")

    # Invalid variable names (should be alphanumeric + underscore)
    invalid_vars = re.findall(r'\{\{\s*([^}]*[^a-zA-Z0-9_\s|"\'+-]+[^}]*)\s*\}\}', content)
    for var in invalid_vars:
        if not any(keyword in var for keyword in ["if", "else", "string", "+", '"']):  # Skip conditionals
            errors.append(f"Invalid variable name: {var}")

    return len(errors) == 0, errors
