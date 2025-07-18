# Quaestor

> 🏛️ Context management for AI-assisted development

[![PyPI Version](https://img.shields.io/pypi/v/quaestor.svg)](https://pypi.org/project/quaestor/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Quaestor** provides intelligent context management and quality enforcement for AI assistants, with flexible modes for personal and team projects. Version 0.4.2 brings updated documentation and streamlined user experience.

## Why Quaestor?

AI assistants like Claude are powerful but need context. Quaestor provides:
- 🧠 **Smart Context** - Automatically adjusts rules based on project complexity
- 🎯 **Flexible Modes** - Personal mode for solo work, team mode for collaboration
- ⚙️ **Command Customization** - Override and configure commands per project
- 📊 **Progress Tracking** - Maintain project memory and milestones
- ✅ **Quality Enforcement** - Ambient rules that work outside commands

## Quick Start

```bash
# Personal mode (default) - Everything local to your project
uvx quaestor init

# Team mode - Shared commands, committed rules
uvx quaestor init --mode team
```

### Personal Mode (Default)
Creates a self-contained setup in your project:
```
project/
├── .claude/           # All AI files (gitignored)
│   ├── CLAUDE.md     # Context-aware rules
│   ├── commands/     # Local command copies
│   │   ├── task.md
│   │   ├── status.md
│   │   ├── analyze.md
│   │   ├── milestone.md
│   │   ├── check.md
│   │   ├── auto-commit.md
│   │   ├── milestone-pr.md
│   │   └── project-init.md
│   └── settings.json # Hooks configuration
├── .quaestor/        # Documentation & memory
│   ├── ARCHITECTURE.md
│   ├── MEMORY.md
│   ├── PATTERNS.md
│   ├── VALIDATION.md
│   └── AUTOMATION.md
└── .gitignore        # Auto-updated
```

### Team Mode
For shared projects with consistent standards:
```
project/
├── CLAUDE.md         # Team rules (committed)
├── .claude/          # Local hooks only
│   └── settings.json # Hooks configuration
├── .quaestor/        # Shared documentation (committed)
│   ├── QUAESTOR_CLAUDE.md
│   ├── CRITICAL_RULES.md
│   ├── ARCHITECTURE.md
│   ├── MEMORY.md
│   ├── PATTERNS.md
│   ├── VALIDATION.md
│   ├── AUTOMATION.md
│   └── manifest.json
├── ~/.claude/commands/  # Global commands
│   ├── task.md
│   ├── status.md
│   ├── analyze.md
│   ├── milestone.md
│   ├── check.md
│   ├── auto-commit.md
│   ├── milestone-pr.md
│   └── project-init.md
└── .gitignore        # Auto-updated
```

Now Claude can use commands with project-specific behavior:
```
/task: implement user authentication
/status
/configure
```

## Installation

```bash
# No install needed (recommended)
uvx quaestor init

# Or install globally
pip install quaestor
```

## Commands

**CLI Commands:**
- `quaestor init` - Initialize with smart defaults
  - `--mode personal` (default) - Local, self-contained setup
  - `--mode team` - Shared commands and rules
  - `--contextual` (default) - Analyze project complexity
- `quaestor configure` - Customize command behavior
  - `--init` - Create command configuration
  - `--command <name> --create-override` - Override specific commands
- `quaestor update` - Update while preserving your changes

**AI Assistant Commands**:
- `/task` - Implement features with orchestration
- `/status` - Show progress with velocity tracking
- `/analyze` - Code analysis across multiple dimensions
- `/milestone` - Manage phases with completion detection
- `/check` - Quality validation and fixing
- `/auto-commit` - Conventional commits for TODOs
- `/milestone-pr` - Automated PR creation
- `/project-init` - Framework detection and project setup

## Key Features

### 🧠 Context-Aware Commands
Quaestor commands use patterns for better Claude integration:
- **Auto-activation** → Context-aware triggers and thresholds
- **Performance profiling** → Standard, optimization, and complex execution modes  
- **Quality gates** → Error fixing with parallel agents
- **Token efficiency** → Reduction through symbol system

Rules work ambiently in CLAUDE.md, not just in commands!

### ⚙️ Command Customization
Configure commands per project with `.quaestor/command-config.yaml`:
```yaml
commands:
  task:
    enforcement: strict
    parameters:
      minimum_test_coverage: 90
      max_function_lines: 30
    custom_rules:
      - "All APIs must have OpenAPI specs"
      - "Database changes require migrations"
```

Or create full overrides in `.quaestor/commands/task.md`.

### 🎯 Flexible Modes

**Installation modes determine where files are stored:**

**Personal Mode (Default)**:
- Everything local in `.claude/`
- Perfect for solo developers
- Commands and context in one place
- Fully gitignored

**Team Mode**:
- Shared standards in `.quaestor/`
- Global commands in `~/.claude/`
- Consistent across team
- Version controlled rules

**Note**: Both modes support all command complexity levels. Mode choice is about file organization, not project complexity.

### 📊 Smart Project Analysis
- Auto-detects language (Python, Rust, JS/TS, Go, Java, etc.)
- Identifies test frameworks and CI/CD
- Recognizes team markers (CODEOWNERS, PR templates)
- Calculates complexity score

### 🔄 Workflow Orchestration
Adaptive workflow based on scope:
- **Direct execution**: <10 files → Read + Edit operations
- **Parallel agents**: 10-50 files → Multi-agent coordination  
- **Complex systems**: >50 files → Systematic agent delegation
- **Quality cycles**: Execute → Validate → Fix → Complete
- **Auto-escalation**: Complexity threshold triggers

### 📈 Command Complexity Thresholds
Commands adapt their behavior based on task complexity (0.0-1.0):
- **Standard (0.2-0.4)**: Quick, focused operations (e.g., `/status`, `/milestone`)
- **Optimization (0.4-0.6)**: Balanced efficiency with smart features (e.g., `/check`)
- **Complex (0.6-0.8)**: Full orchestration and deep analysis (e.g., `/task`, `/analyze`)

Thresholds control: auto-activation features, parallel processing, quality gates, and error recovery.


## Recent Updates (v0.4.2)

- **Enhanced Hooks System** - Comprehensive fixes for better workflow automation
- **Improved Testing** - Full test coverage for critical components
- **A1 Development** - Working on next-generation automatic intelligence system
- **Documentation Updates** - Clearer guidance and updated examples

## How It Works

1. **Project Analysis** - Scans for language, tests, complexity
2. **Context Generation** - Creates appropriate CLAUDE.md rules
3. **Command Setup** - Installs commands (local or global)
4. **Customization** - Allows per-project overrides
5. **Smart Updates** - Preserves your changes

### Example Workflows

- **Simple tasks**: Direct implementation with quality validation
- **Complex tasks**: Orchestrated workflow with parallel agents and quality gates
- **Auto-tracking**: Progress updates and conventional commits

### Command Customization

```bash
quaestor configure --init  # Create config
```

Edit `.quaestor/command-config.yaml` to add project-specific rules and enforcement levels.


## Ambient Rule Enforcement

Quaestor's rules work everywhere in CLAUDE.md, not just in commands. Rules guide Claude's behavior for complexity checking, delegation triggers, and quality standards across all interactions.

## Updating

```bash
# Check what would change
quaestor update --check

# Update with backup
quaestor update --backup

# Force update all files
quaestor update --force
```

Updates preserve your customizations in user-editable files.

## What's Coming Next

We're working on **A1** (Automatic Intelligence), a next-generation system that will bring:
- Event-driven architecture for improved performance
- Enhanced learning and adaptation capabilities
- Simplified codebase with modular extensions
- Advanced pattern recognition and workflow detection

A1 is currently in development and not yet ready for production use.

## Contributing

```bash
git clone https://github.com/jeanluciano/quaestor.git
cd quaestor
uv sync
uv run pytest
```

## License

MIT License

---

<div align="center">

[Documentation](https://github.com/jeanluciano/quaestor) · [Issues](https://github.com/jeanluciano/quaestor/issues)

</div>