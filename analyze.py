import requests
import json

OPENROUTER_API_KEY = "OPENROUTER_KEY"

YOUR_SITE_URL = "YOUR_SITE_URL"
YOUR_APP_NAME = "YOUR_APP_NAME"

# Function to analyze an image
def analyze_image(image_url):
    prompt = (
        "You are an image analysis function. Analyze the given image and provide a short description and relevant tags. "
        "Respond only in the following JSON format:\n\n"
        "{\n"
        '  "description": "A concise description of the image",\n'
        '  "tags": ["tag1", "tag2", "tag3"]\n'
        "}\n"
        "Only respond with JSON and do not include any additional text outside the JSON format."
    )

    data = {
        "model": "meta-llama/llama-3.2-90b-vision-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        "temperature": 0  # Set temperature to 0 for deterministic output
    }

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
            "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
        },
        data=json.dumps(data)
    )

    return response.json()

# Function to read the input file and fetch image URLs
def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

# Function to write the output to a new file
def append_to_output_file(filename, content):
    with open(filename, 'a') as file:
        file.write(content)

# Function to check if the raw response contains valid JSON content
def check_for_errors(response_json):
    try:
        content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        if content.startswith("{") and content.endswith("}"):
            parsed_content = json.loads(content)
            if "description" in parsed_content and "tags" in parsed_content:
                return False  # No errors
        return True  # Contains errors
    except (json.JSONDecodeError, KeyError):
        return True

# Main function
def main():
    input_filename = 'bbt.txt'
    output_filename = 'README2.md'

    lines = read_input_file(input_filename)
    initial_content = "# Big Bang Theory through an AI Lens (2024)\n\n"
    append_to_output_file(output_filename, initial_content)

    for line in lines:
        if line.startswith("###"):
            append_to_output_file(output_filename, line)
        elif line.startswith("![]"):
            image_num = int(line.split('_')[1].split('.')[0])
            image_url = f"https://raw.githubusercontent.com/u1i/bbt/master/img/bbt_{image_num:03}.png"

            while True:
                print(f"\nProcessing image {image_num} - {image_url}")

                response_json = analyze_image(image_url)
                
                # Convert response JSON to string for raw output
                raw_response_str = json.dumps(response_json, indent=2)
                print(f"\nLLM response:\n{raw_response_str}")

                if check_for_errors(response_json):
                    print("\nError detected. Suggest to retry.\n")
                    action = input("Enter 'r' to retry or 'p' to proceed: ")
                    if action.lower() == 'p':
                        output_content = f"![]({image_url})\n**Raw Response:** {raw_response_str}\n\n"
                        append_to_output_file(output_filename, output_content)
                        print(f"\nAppended raw response for image {image_num} to {output_filename}")
                        break
                    elif action.lower() == 'r':
                        print("\nRetrying...\n")
                else:
                    # Extract content
                    content = response_json["choices"][0]["message"]["content"]
                    parsed_content = json.loads(content)
                    description = parsed_content.get("description", "No description available")
                    tags = ", ".join(parsed_content.get("tags", []))

                    # Append valid response to the output file
                    output_content = f"![]({image_url})\n**Description:** \"{description}\"\n**Tags:** {tags}\n\n"
                    append_to_output_file(output_filename, output_content)
                    print(f"\nAppended proper response for image {image_num} to {output_filename}")
                    break

if __name__ == "__main__":
    main()
