#!/usr/bin/env python3
"""
Test script to verify the LM Studio role filtering fix
"""

import sys
sys.path.append('/app')

def test_lm_studio_role_filtering():
    """Test LM Studio with different message roles"""
    try:
        from superagi.llms.lm_studio import LMStudio
        
        print("🔍 Testing LM Studio role filtering fix...")
        
        lm_studio = LMStudio(
            api_key='EMPTY',
            end_point='http://192.168.0.144:1234',
            model='mistralai/mistral-7b-instruct-v0.3'
        )
        
        # Test with mixed roles (system, user, assistant)
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Please respond with 'Role filtering works!' to confirm the fix."},
        ]
        
        print("📋 Original messages:")
        for msg in test_messages:
            print(f"   {msg['role']}: {msg['content']}")
        
        print("\n💬 Testing chat completion with role filtering...")
        response = lm_studio.chat_completion(test_messages, max_tokens=50)
        
        if 'error' in response:
            print(f"❌ Chat completion failed: {response['error']} - {response['message']}")
            return False
        else:
            print(f"✅ Chat completion successful!")
            print(f"📝 Response: {response['content']}")
            return True
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing LM Studio Role Filtering Fix")
    print("=" * 50)
    
    success = test_lm_studio_role_filtering()
    
    if success:
        print("\n🎉 SUCCESS: LM Studio role filtering fix is working!")
        print("✅ Your agents should now work properly with LM Studio")
    else:
        print("\n❌ FAILED: Role filtering fix needs more work")
        print("🔧 Check the logs for more details")
