# SuperAGI Custom Setup with LM Studio Integration

This is a customized SuperAGI setup with LM Studio integration, enhanced file writing capabilities, and vector database support.

## 🚀 Features

### ✅ LM Studio Integration
- **7 LM Studio models** configured and working
- **Local LLM support** with proper API endpoints
- **Custom LM Studio provider** with logo and branding
- **Hardcoded provider option** in Settings > Models UI

### ✅ Enhanced File Writing
- **Automatic directory creation** for proper project structure
- **Support for subdirectories**: `src/`, `tests/`, `docs/`, `assets/`, `config/`, `scripts/`, etc.
- **No more "directory not found" errors**
- **Proper resource management** and file tracking

### ✅ Vector Database Support
- **Qdrant vector database** configured and running
- **URL**: `http://super__qdrant:6333`
- **Default collection**: `superagi-collection`
- **Ready for knowledge management and RAG**

### ✅ Fixed Agent Execution
- **Celery worker** properly configured
- **Agent executions** work seamlessly with local models
- **JSON schema prompt issues** resolved
- **Stable agent performance**

## 🛠️ Setup Instructions

### Prerequisites
- Docker and Docker Compose
- LM Studio running on `192.168.0.144:1234`
- WSL2 (if on Windows)

### Quick Start
1. Clone this repository
2. Copy `config_template.yaml` to `config.yaml`
3. Run: `docker-compose up -d`
4. Access SuperAGI at `http://localhost:3000`

### LM Studio Models Available
1. **Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf**
2. **Qwen2.5-7B-Instruct-Q4_K_M.gguf**
3. **llama-3.2-3b-instruct-q4_k_m.gguf**
4. **granite-3.0-8b-instruct-q4_k_m.gguf**
5. **Phi-3.5-mini-instruct-Q4_K_M.gguf**
6. **gemma-2-9b-it-q4_k_m.gguf**
7. **Llama-3.2-1B-Instruct-Q4_K_M.gguf**

## 📁 File Structure

### Workspace Organization
```
workspace/
├── input/           # Input files for agents
├── output/          # Agent-generated files
│   └── {agent_name}_{id}/
│       └── {execution_name}_{id}/
│           ├── src/         # Source code
│           ├── tests/       # Test files
│           ├── docs/        # Documentation
│           ├── assets/      # Static assets
│           ├── config/      # Configuration
│           ├── scripts/     # Build scripts
│           ├── lib/         # Libraries
│           ├── bin/         # Binaries
│           └── examples/    # Examples
└── template/        # Template directories
```

## 🔧 Custom Modifications

### Files Modified
- `superagi/llms/lm_studio.py` - LM Studio integration
- `superagi/resource_manager/file_manager.py` - Enhanced file writing
- `gui/pages/Content/Models/ModelForm.js` - LM Studio UI integration
- `docker-compose.yaml` - Added Qdrant service
- Multiple configuration and helper files

### Scripts Added
- `setup_vector_db.py` - Vector database setup
- `fix_workspace_structure.py` - Workspace structure creation
- `test_file_writing.py` - File writing verification
- `add_qdrant_config.py` - Qdrant configuration

## 🎯 Usage Examples

### Creating Agents
1. Go to SuperAGI UI (`http://localhost:3000`)
2. Create new agent
3. Select LM Studio model from dropdown
4. Agent can now write files to proper directory structure

### File Writing
Agents can write files like:
- `src/main.rs` - Rust source code
- `tests/test.py` - Python tests
- `docs/README.md` - Documentation
- `config/settings.json` - Configuration files

### Vector Database
- Access Qdrant at `http://localhost:6333`
- Use for knowledge management and RAG applications
- Integrated with SuperAGI's resource system

## 🐛 Troubleshooting

### Agent Stuck on "Thinking..."
```bash
docker restart superagi-celery-1
```

### File Writing Errors
The enhanced file manager automatically creates directories, so this should no longer be an issue.

### LM Studio Connection Issues
1. Ensure LM Studio is running on `192.168.0.144:1234`
2. Check Windows Firewall settings
3. Verify WSL can access Windows network

## 📊 Performance Notes
- **LM Studio models** work best with proper GPU acceleration
- **Celery worker** processes one agent execution at a time
- **Vector database** is ready for production use
- **File operations** are optimized for project structure creation

## 🔒 Security
- This is a **private repository** with custom configurations
- **No API keys** are committed to version control
- **Local LLM setup** keeps data private
- **Docker isolation** provides security boundaries

## 📝 License
Based on SuperAGI with custom modifications for LM Studio integration and enhanced functionality.
