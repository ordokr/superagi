import json
import requests
from superagi.config.config import get_config
from superagi.lib.logger import logger
from superagi.llms.base_llm import BaseLlm


class LMStudio(BaseLlm):
    def __init__(self, temperature=0.6, max_tokens=get_config("MAX_MODEL_TOKEN_LIMIT"), top_p=1,
                 frequency_penalty=0, presence_penalty=0, number_of_results=1, model=None,
                 api_key='EMPTY', end_point=None):
        """
        Args:
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The maximum number of tokens.
            top_p (float): The top p.
            frequency_penalty (float): The frequency penalty.
            presence_penalty (float): The presence penalty.
            number_of_results (int): The number of results.
            api_key (str): The API key (not used for LM Studio but kept for compatibility).
            end_point (str): The LM Studio endpoint URL.
        """
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.number_of_results = number_of_results
        self.end_point = end_point or "http://192.168.0.144:1234"

        # Ensure endpoint has proper format
        if not self.end_point.startswith('http'):
            self.end_point = f"http://{self.end_point}"
        if not self.end_point.endswith('/v1'):
            if self.end_point.endswith('/'):
                self.end_point = f"{self.end_point}v1"
            else:
                self.end_point = f"{self.end_point}/v1"

    def chat_completion(self, messages, max_tokens=get_config("MAX_MODEL_TOKEN_LIMIT")):
        """
        Call the chat completion using LM Studio's OpenAI-compatible API.

        Args:
            messages (list): The messages.
            max_tokens (int): The maximum number of tokens.

        Returns:
            dict: The response.
        """
        try:
            headers = {
                'Content-Type': 'application/json',
            }

            # If API key is provided and not 'EMPTY', add it to headers
            if self.api_key and self.api_key != 'EMPTY':
                headers['Authorization'] = f'Bearer {self.api_key}'

            # Filter and convert messages for LM Studio compatibility
            # LM Studio only supports 'user' and 'assistant' roles
            filtered_messages = []
            system_content = ""

            for message in messages:
                role = message.get('role', '').lower()
                content = message.get('content', '')

                if role == 'system':
                    # Combine system messages into the first user message
                    system_content += content + "\n"
                elif role in ['user', 'assistant']:
                    filtered_messages.append({
                        'role': role,
                        'content': content
                    })
                else:
                    # Convert other roles to user messages
                    filtered_messages.append({
                        'role': 'user',
                        'content': f"[{role.upper()}]: {content}"
                    })

            # If we have system content, prepend it to the first user message
            if system_content and filtered_messages:
                for i, msg in enumerate(filtered_messages):
                    if msg['role'] == 'user':
                        filtered_messages[i]['content'] = system_content.strip() + "\n\n" + msg['content']
                        break
                else:
                    # No user message found, create one with system content
                    filtered_messages.insert(0, {
                        'role': 'user',
                        'content': system_content.strip()
                    })

            # Ensure we have at least one message
            if not filtered_messages:
                filtered_messages = [{'role': 'user', 'content': 'Hello'}]

            data = {
                'model': self.model or 'local-model',
                'messages': filtered_messages,
                'temperature': self.temperature,
                'max_tokens': int(max_tokens) if max_tokens else self.max_tokens,
                'top_p': self.top_p,
                'frequency_penalty': self.frequency_penalty,
                'presence_penalty': self.presence_penalty,
                'n': self.number_of_results,
                'stream': False
            }

            url = f"{self.end_point}/chat/completions"
            logger.info(f"Making request to LM Studio at: {url}")
            logger.info(f"Request data: {json.dumps(data, indent=2)}")

            response = requests.post(url, headers=headers, json=data, timeout=60)

            if response.status_code == 200:
                response_data = response.json()
                content = response_data["choices"][0]["message"]["content"]
                logger.info(f"LM Studio response: {content}")

                # Handle reasoning models that include <think>...</think> blocks
                # Extract only the JSON part after the thinking block
                if '<think>' in content and '</think>' in content:
                    # Find the end of the thinking block
                    think_end = content.find('</think>')
                    if think_end != -1:
                        # Extract content after the thinking block
                        json_content = content[think_end + 8:].strip()
                        logger.info(f"Extracted JSON after thinking block: {json_content[:200]}...")
                        return {"response": response_data, "content": json_content}

                return {"response": response_data, "content": content}
            else:
                error_msg = f"LM Studio API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {"error": "API_ERROR", "message": error_msg}

        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error to LM Studio at {self.end_point}: {str(e)}"
            logger.error(error_msg)
            return {"error": "CONNECTION_ERROR", "message": error_msg}
        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout error connecting to LM Studio: {str(e)}"
            logger.error(error_msg)
            return {"error": "TIMEOUT_ERROR", "message": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error with LM Studio: {str(e)}"
            logger.error(error_msg)
            return {"error": "UNEXPECTED_ERROR", "message": error_msg}

    def get_source(self):
        """
        Get the source.

        Returns:
            str: The source.
        """
        return "LM Studio"

    def get_api_key(self):
        """
        Returns:
            str: The API key.
        """
        return self.api_key

    def get_model(self):
        """
        Returns:
            str: The model.
        """
        return self.model

    def get_models(self):
        """
        Get available models from LM Studio.

        Returns:
            list: The models available.
        """
        try:
            headers = {'Content-Type': 'application/json'}
            if self.api_key and self.api_key != 'EMPTY':
                headers['Authorization'] = f'Bearer {self.api_key}'

            url = f"{self.end_point}/models"
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                models_data = response.json()
                return [model['id'] for model in models_data.get('data', [])]
            else:
                logger.error(f"Failed to fetch models from LM Studio: {response.status_code}")
                return [self.model] if self.model else ['local-model']

        except Exception as e:
            logger.error(f"Error fetching models from LM Studio: {str(e)}")
            return [self.model] if self.model else ['local-model']

    def verify_access_key(self, api_key=None):
        """
        Verify access to LM Studio endpoint.

        Args:
            api_key (str): API key to verify (optional for LM Studio).

        Returns:
            bool: True if accessible, False otherwise.
        """
        try:
            headers = {'Content-Type': 'application/json'}
            test_key = api_key or self.api_key
            if test_key and test_key != 'EMPTY':
                headers['Authorization'] = f'Bearer {test_key}'

            url = f"{self.end_point}/models"
            response = requests.get(url, headers=headers, timeout=10)

            return response.status_code == 200

        except Exception as e:
            logger.error(f"Error verifying LM Studio access: {str(e)}")
            return False

    def get_endpoint(self):
        """
        Returns:
            str: The endpoint URL.
        """
        return self.end_point
