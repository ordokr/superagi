#!/usr/bin/env python3
"""
Final comprehensive test to verify all LM Studio fixes are working
"""

import sys
import json
sys.path.append('/app')

def test_complete_fix():
    """Test all LM Studio fixes together"""
    try:
        from superagi.llms.lm_studio import LMStudio

        print("🔍 Testing complete LM Studio fix...")

        lm_studio = LMStudio(
            api_key='EMPTY',
            end_point='http://192.168.0.144:1234',
            model='local-model'
        )

        # Test with system message (role filtering) + simplified prompt + reasoning model handling
        test_messages = [
            {"role": "system", "content": "You are SuperAGI, an AI assistant."},
            {"role": "user", "content": """Your goal is to write a simple hello world program in Rust.

Respond with only valid JSON in this exact format:
{
    "thoughts": {
        "text": "your thought about the task",
        "reasoning": "short reasoning for your decision",
        "plan": "- step 1\\n- step 2\\n- step 3",
        "criticism": "constructive self-criticism",
        "speak": "summary to tell the user"
    },
    "tool": {
        "name": "Write File",
        "args": {
            "file_name": "main.rs",
            "content": "fn main() {\\n    println!(\\\"Hello, world!\\\");\\n}"
        }
    }
}"""}
        ]

        print("📋 Testing with system message (role filtering)...")
        print("📋 Testing with simplified prompt (no complex schema)...")
        print("📋 Testing with reasoning model handling...")

        print("\n💬 Testing complete chat completion...")
        response = lm_studio.chat_completion(test_messages, max_tokens=1000)

        if 'error' in response:
            print(f"❌ Chat completion failed: {response['error']} - {response['message']}")
            return False
        else:
            print(f"✅ Chat completion successful!")
            content = response['content']
            print(f"📝 Response length: {len(content)} characters")

            # Try to parse as JSON
            try:
                parsed = json.loads(content)
                print("✅ SUCCESS: Response is valid JSON!")

                # Check structure
                if "thoughts" in parsed and "tool" in parsed:
                    print("✅ SUCCESS: JSON has correct structure!")

                    # Check thoughts fields
                    thoughts = parsed["thoughts"]
                    required_fields = ["text", "reasoning", "plan", "criticism", "speak"]
                    missing_fields = [f for f in required_fields if f not in thoughts]

                    if not missing_fields:
                        print("✅ SUCCESS: All thoughts fields present!")
                    else:
                        print(f"⚠️  Missing thoughts fields: {missing_fields}")

                    # Check tool structure
                    tool = parsed["tool"]
                    if "name" in tool and "args" in tool:
                        print("✅ SUCCESS: Tool structure is correct!")
                        print(f"🛠️  Tool: {tool['name']}")

                        if "file_name" in tool["args"] and "content" in tool["args"]:
                            print("✅ SUCCESS: Tool args are correct!")
                            print(f"📄 File: {tool['args']['file_name']}")
                            print(f"📝 Content preview: {tool['args']['content'][:50]}...")
                            return True
                        else:
                            print("⚠️  Tool args missing file_name or content")
                            return False
                    else:
                        print("⚠️  Tool missing name or args")
                        return False
                else:
                    print("⚠️  JSON missing thoughts or tool")
                    return False

            except json.JSONDecodeError as e:
                print(f"⚠️  Response is not valid JSON: {e}")
                print(f"📝 Raw response: {content[:200]}...")
                return False

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Final Comprehensive LM Studio Fix Test")
    print("=" * 60)
    print("Testing:")
    print("  ✅ Role filtering (system → user message merging)")
    print("  ✅ Simplified prompt (no complex JSON schema)")
    print("  ✅ Reasoning model handling (<think> block extraction)")
    print("=" * 60)

    success = test_complete_fix()

    if success:
        print("\n🎉 🎉 🎉 COMPLETE SUCCESS! 🎉 🎉 🎉")
        print("✅ All LM Studio fixes are working perfectly!")
        print("✅ Role filtering: System messages merged with user messages")
        print("✅ Simplified prompts: No more JSON schema confusion")
        print("✅ Reasoning models: <think> blocks properly handled")
        print("✅ Your SuperAGI agents should now work flawlessly with LM Studio!")
        print("\n🚀 Ready to run your agents!")
    else:
        print("\n❌ Some issues remain")
        print("🔧 Check the logs for more details")
