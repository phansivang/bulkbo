import requests

url = "https://verificationapi-v1.sinch.com/verification/v1/verifications"
payload="{\n  \"identity\": {\n  \"type\": \"number\",\n  \"endpoint\": \"+85566362218\"\n  },\n  \"method\": \"sms\"\n}"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic ODIxNGFhNGQtNTkzYS00NDBiLTlmMTQtYzU3MmViYzFjZDhiOmhBRFhoS09uUkVhTGV2dmJLamw4L1E9PQ=='
}
response = requests.request("POST", url, headers=headers, data=payload)

print(response.elapsed)