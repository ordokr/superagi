# LM Studio Integration with SuperAGI

## Overview
This guide explains how to connect SuperAGI to your LM Studio instance running on `http://192.168.0.144:1234`.

## Available Models in Your LM Studio
Based on the scan, your LM Studio instance has the following models available:
- `mistralai/mistral-7b-instruct-v0.3`
- `watt-tool-8b`
- `text-embedding-nomic-embed-text-v1.5`
- `visionreasoner-7b`

## Setup Instructions

### 1. Add LM Studio as a Model Provider

1. **Open SuperAGI GUI**: Navigate to http://localhost:3000
2. **Go to Settings**: Click on the settings/configuration section
3. **Add Model Provider**: 
   - Provider Name: `LM Studio`
   - API Key: `EMPTY` (or leave blank - LM Studio doesn't require authentication by default)
   - Endpoint: `http://192.168.0.144:1234`

### 2. Configure Models

After adding the provider, SuperAGI will automatically detect and add the available models:
- **mistralai/mistral-7b-instruct-v0.3**: General purpose instruction-following model
- **watt-tool-8b**: Tool-use specialized model
- **visionreasoner-7b**: Vision and reasoning model

### 3. Create Agents with LM Studio Models

1. **Create New Agent**
2. **Select Model**: Choose one of the LM Studio models from the dropdown
3. **Configure Agent**: Set up your agent with the desired tools and instructions

## Model Recommendations

### For General Tasks
- **Model**: `mistralai/mistral-7b-instruct-v0.3`
- **Use Case**: General conversation, text generation, analysis
- **Context Length**: 4096 tokens (default)

### For Tool Usage
- **Model**: `watt-tool-8b`
- **Use Case**: Agents that need to use tools and APIs
- **Context Length**: 4096 tokens (default)

### For Vision Tasks
- **Model**: `visionreasoner-7b`
- **Use Case**: Image analysis, visual reasoning
- **Context Length**: 4096 tokens (default)

## Troubleshooting

### Connection Issues
If you can't connect to LM Studio:
1. Ensure LM Studio is running on `192.168.0.144:1234`
2. Check that the LM Studio server is configured to accept external connections
3. Verify network connectivity between SuperAGI container and LM Studio host

### Model Loading Issues
If models don't appear:
1. Restart the SuperAGI backend: `docker compose restart backend`
2. Check backend logs: `docker logs superagi-backend-1`
3. Verify LM Studio models are loaded and ready

### Performance Optimization
For better performance:
1. Ensure LM Studio has sufficient GPU memory allocated
2. Adjust context length based on your use case
3. Monitor GPU utilization during agent runs

## API Endpoints Supported
Your LM Studio instance supports these OpenAI-compatible endpoints:
- `GET /v1/models` - List available models
- `POST /v1/chat/completions` - Chat completions
- `POST /v1/completions` - Text completions  
- `POST /v1/embeddings` - Text embeddings

## Example Agent Configuration

```json
{
  "name": "LM Studio Assistant",
  "model": "mistralai/mistral-7b-instruct-v0.3",
  "provider": "LM Studio",
  "endpoint": "http://192.168.0.144:1234",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

## Next Steps
1. Test the connection by creating a simple agent
2. Experiment with different models for different use cases
3. Monitor performance and adjust settings as needed
