#!/usr/bin/env python3
"""
Test script to verify LM Studio integration with SuperAGI
"""

import sys
import os
sys.path.append('/home/tim/SuperAGI')

from superagi.llms.lm_studio import LMStudio

def test_lm_studio_connection():
    """Test basic connection to LM Studio"""
    print("🔍 Testing LM Studio Connection...")

    # Initialize LM Studio client
    lm_studio = LMStudio(
        api_key='EMPTY',
        end_point='http://192.168.0.144:1234',
        model='mistralai/mistral-7b-instruct-v0.3',
        temperature=0.7,
        max_tokens=100
    )

    # Test 1: Check if we can get models
    print("\n📋 Test 1: Fetching available models...")
    try:
        models = lm_studio.get_models()
        print(f"✅ Available models: {models}")
    except Exception as e:
        print(f"❌ Failed to fetch models: {e}")
        return False

    # Test 2: Verify endpoint access
    print("\n🔗 Test 2: Verifying endpoint access...")
    try:
        access_ok = lm_studio.verify_access_key()
        if access_ok:
            print("✅ Endpoint is accessible")
        else:
            print("❌ Endpoint is not accessible")
            return False
    except Exception as e:
        print(f"❌ Failed to verify endpoint: {e}")
        return False

    # Test 3: Test chat completion
    print("\n💬 Test 3: Testing chat completion...")
    try:
        messages = [
            {"role": "user", "content": "Hello! Please respond with just 'Hello from LM Studio!' to confirm the connection is working."}
        ]

        response = lm_studio.chat_completion(messages, max_tokens=50)

        if 'error' in response:
            print(f"❌ Chat completion failed: {response['error']} - {response['message']}")
            return False
        else:
            print(f"✅ Chat completion successful!")
            print(f"📝 Response: {response['content']}")
    except Exception as e:
        print(f"❌ Chat completion error: {e}")
        return False

    print("\n🎉 All tests passed! LM Studio integration is working correctly.")
    return True

def test_superagi_integration():
    """Test SuperAGI integration with LM Studio"""
    print("\n🔧 Testing SuperAGI Integration...")

    try:
        from superagi.llms.llm_model_factory import build_model_with_api_key
        from superagi.models.models import Models

        # Test LLM factory
        print("🏭 Testing LLM Model Factory...")
        llm = build_model_with_api_key(
            provider_name='LM Studio',
            api_key='EMPTY'
        )

        if llm:
            print("✅ LLM Factory successfully created LM Studio instance")
            print(f"📊 Model: {llm.get_model()}")
            print(f"🔗 Endpoint: {llm.get_endpoint()}")
        else:
            print("❌ LLM Factory failed to create LM Studio instance")
            return False

    except Exception as e:
        print(f"❌ SuperAGI integration test failed: {e}")
        return False

    print("✅ SuperAGI integration test passed!")
    return True

if __name__ == "__main__":
    print("🚀 Starting LM Studio Integration Tests")
    print("=" * 50)

    # Test basic connection
    connection_ok = test_lm_studio_connection()

    if connection_ok:
        # Test SuperAGI integration
        integration_ok = test_superagi_integration()

        if integration_ok:
            print("\n🎊 SUCCESS: LM Studio is fully integrated with SuperAGI!")
            print("\n📋 Next Steps:")
            print("1. Open SuperAGI GUI at http://localhost:3000")
            print("2. Go to Settings > Models")
            print("3. Add 'LM Studio' as a provider")
            print("4. Set endpoint to: http://192.168.0.144:1234")
            print("5. Set API key to: EMPTY (or leave blank)")
            print("6. Create agents using LM Studio models")
        else:
            print("\n❌ PARTIAL SUCCESS: Connection works but integration needs fixes")
    else:
        print("\n❌ FAILED: Cannot connect to LM Studio")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure LM Studio is running on 192.168.0.144:1234")
        print("2. Check that LM Studio server accepts external connections")
        print("3. Verify network connectivity between containers and LM Studio")
