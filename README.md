# Yandex Cloud ML SDK Adapter for Cline

This adapter integrates Yandex Cloud ML services with the Cline extension for VSCode. It provides a bridge between the extension's requests and the Yandex Cloud's AI models.

## Installation

```sh
pip install yandex-cloud-ml-sdk
```



## Usage Example

Here's how to use the adapter with Cline extension:

```python
# Example of integration
from yandex_cline_adapter import YandexCloudClineAdapter

# Initialize with your credentials
adapter = YandexCloudClineAdapter(
    folder_id="your_folder_id",  # or set YC_FOLDER_ID env var
    auth="your_api_key",         # or set YC_API_KEY env var
    async_mode=False             # Use sync mode for simplicity
)

# Example request from Cline extension
request = '''
{
    "command": "generate",
    "prompt": "Write a Python function to calculate Fibonacci numbers"
}
'''

# Process the request
response = adapter.cline_handler(request)
print(response)

# Chat example
chat_request = '''
{
    "command": "chat",
    "messages": [
        {"role": "system", "text": "You are a helpful coding assistant"},
        {"role": "user", "text": "How do I read a file in Python?"}
    ]
}
'''

chat_response = adapter.cline_handler(chat_request)
print(chat_response)
```

## Configuration

You can configure the adapter using:

1. Environment variables:
   - `YC_FOLDER_ID`: Your Yandex Cloud folder ID
   - `YC_API_KEY`: Your API key for authentication
   - `YC_IAM_TOKEN`: Alternative IAM token for authentication

2. Direct initialization parameters as shown in the example

## Customization

You may need to extend this adapter based on specific Cline extension requirements. The key method is `cline_handler()` which processes requests from the extension and returns appropriate responses.
