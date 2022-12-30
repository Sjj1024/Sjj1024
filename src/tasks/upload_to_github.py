import requests

url = "https://api.github.com/repos/Sjj1024/Sjj1024/contents/.github/workflows/hello.yml"

payload = "{\r\n  \"message\": \"add a py file\",\r\n  \"content\": \"aW1wb\"\r\n}"
headers = {
  'Accept': 'application/vnd.github+json',
  'Authorization': 'Bearer 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',
  'X-GitHub-Api-Version': '2022-11-28',
  'Content-Type': 'text/plain'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
