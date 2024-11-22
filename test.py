import openai

openai.api_key = "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"


try:
    response = openai.Model.list()
    print("API Key is working. Models available:")
    print(response)
except Exception as e:
    print(f"Error with API Key: {e}")
