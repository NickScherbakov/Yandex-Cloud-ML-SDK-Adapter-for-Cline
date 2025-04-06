import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import AsyncYCloudML, YCloudML

# Загрузка переменных из .env файла
load_dotenv()

class YandexCloudClineAdapter:
    """Adapter for using Yandex Cloud ML SDK with Cline extension for VSCode."""
    
    def __init__(
        self, 
        folder_id: str = None,
        auth: str = None,
        async_mode: bool = True,
        temperature: float = 0.6,
        max_tokens: int = 2048
    ):
        """
        Initialize the adapter.
        
        Args:
            folder_id: Yandex Cloud folder ID (can also be set via YC_FOLDER_ID env var)
            auth: Authentication token (can also be set via YC_API_KEY or YC_IAM_TOKEN env vars)
            async_mode: Whether to use async API (default: True)
            temperature: Default temperature parameter for generation
            max_tokens: Default maximum tokens for generation
        """
        self.folder_id = folder_id or os.environ.get('YC_FOLDER_ID')
        if not self.folder_id:
            raise ValueError("Folder ID must be provided via parameter or YC_FOLDER_ID env var")
            
        self.auth = auth or os.environ.get('YC_API_KEY') or os.environ.get('YC_IAM_TOKEN')
        if not self.auth:
            raise ValueError("Authentication must be provided via parameter or YC_API_KEY/YC_IAM_TOKEN env vars")
        
        self.async_mode = async_mode
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize SDK
        if self.async_mode:
            self.sdk = AsyncYCloudML(folder_id=self.folder_id, auth=self.auth)
            self.model = self.sdk.models.completions('yandexgpt').configure(
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        else:
            self.sdk = YCloudML(folder_id=self.folder_id, auth=self.auth)
            self.model = self.sdk.models.completions('yandexgpt').configure(
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        
        self.sdk.setup_default_logging()
    
    def configure_model(self, 
                        model_name: str = 'yandexgpt',
                        temperature: float = None, 
                        max_tokens: int = None) -> None:
        """
        Configure the model parameters.
        
        Args:
            model_name: Name of the model to use
            temperature: Control randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
        """
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        if self.async_mode:
            self.model = self.sdk.models.completions(model_name).configure(
                temperature=temp,
                max_tokens=tokens
            )
        else:
            self.model = self.sdk.models.completions(model_name).configure(
                temperature=temp,
                max_tokens=tokens
            )
    
    async def generate_text_async(self, prompt: str) -> str:
        """
        Generate text using async API.
        
        Args:
            prompt: Text prompt for generation
            
        Returns:
            Generated text
        """
        if not self.async_mode:
            raise RuntimeError("Adapter initialized in sync mode, use generate_text instead")
        
        result = await self.model.run(prompt)
        return result[0].text
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using sync API.
        
        Args:
            prompt: Text prompt for generation
            
        Returns:
            Generated text
        """
        if self.async_mode:
            raise RuntimeError("Adapter initialized in async mode, use generate_text_async instead")
        
        result = self.model.run(prompt)
        return result[0].text
    
    async def chat_async(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate chat completion using async API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'text' keys
            
        Returns:
            Generated response text
        """
        if not self.async_mode:
            raise RuntimeError("Adapter initialized in sync mode, use chat instead")
        
        result = await self.model.run(messages)
        return result[0].text
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate chat completion using sync API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'text' keys
            
        Returns:
            Generated response text
        """
        if self.async_mode:
            raise RuntimeError("Adapter initialized in async mode, use chat_async instead")
        
        result = self.model.run(messages)
        return result[0].text
    
    def cline_handler(self, request_json: str) -> str:
        """
        Handle Cline extension requests.
        
        Args:
            request_json: JSON string with request parameters
            
        Returns:
            JSON string with response
        """
        request = json.loads(request_json)
        command = request.get('command')
        
        if command == 'generate':
            prompt = request.get('prompt', '')
            if self.async_mode:
                # For async in sync context, run event loop
                response_text = asyncio.run(self.generate_text_async(prompt))
            else:
                response_text = self.generate_text(prompt)
            
            return json.dumps({
                'status': 'success',
                'text': response_text
            })
            
        elif command == 'chat':
            messages = request.get('messages', [])
            if self.async_mode:
                # For async in sync context, run event loop
                response_text = asyncio.run(self.chat_async(messages))
            else:
                response_text = self.chat(messages)
            
            return json.dumps({
                'status': 'success',
                'text': response_text
            })
            
        elif command == 'configure':
            model_name = request.get('model', 'yandexgpt')
            temperature = request.get('temperature')
            max_tokens = request.get('max_tokens')
            
            self.configure_model(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return json.dumps({
                'status': 'success',
                'message': 'Model configured successfully'
            })
            
        else:
            return json.dumps({
                'status': 'error',
                'message': f'Unknown command: {command}'
            })
