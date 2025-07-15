import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from config import MAX_ITERS
from call_function import (
  available_functions,
  call_function,
)

def main():
  load_dotenv()

  # Příkaz pro AI od uživatele s parametry 'python3 main.py "otazka" --verbose'
  is_verbose = "--verbose" in sys.argv
  args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
  if not args:
    print("AI Code Assistant")
    print('\nUsage: python main.py "your prompt here" [--verbose]')
    print('Example: python main.py "How do I build a calculator app?"')
    sys.exit(1)

  api_key = os.environ.get("GEMINI_API_KEY")
  client = genai.Client(api_key=api_key)
  
  user_prompt = " ".join(args)
  if is_verbose:
    print(f"User prompt: {user_prompt}")

  # List promptů pro AI, první vznáší uživatel, další prompty se sem appendují automaticky v kódu níže
  messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
  ]

  iters = 0
  while True:
    iters += 1
    if iters > MAX_ITERS:
      print(f"Maximum iterations ({MAX_ITERS}) reached.")
      sys.exit(1)

    try:
      final_response = generate_content(client, messages, is_verbose)
      if final_response:
        print("Final response:")
        print(final_response)
        break
    except Exception as e:
      print(f"Error in generate_content: {e}")


def generate_content(client, messages, is_verbose):
  """Calling AI model

  Args:
      client (objekt): genai client for calling of ai
      messages (list): list of strings, prompts for AI for one conversation
      is_verbose (bool): format of model answer (if verbose, then longer and explanatory)

  Returns:
      object: response object form AI
  """
  # callling of ai model
  response = client.models.generate_content(
      model='gemini-2.0-flash-001', 
      contents=messages,
      config=types.GenerateContentConfig(
        tools=[available_functions],
        # passing functions to prompts
        system_instruction=system_prompt
        # passing system prompt as invisible first prompt
      ),      
  )

  # pokud odpověď "verbose", pak vytiskne počty tokenů
  if is_verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
  
  # zachytává odpověď modelu a appenduje do promptů (messages) pro model
  # když finální odpověď, je i toto finální odpověď
  # ale pokud se volá funkce, pak tato odpověď je něco jako "potřebuji zavolat funkci... " a konverzace pokračuje
  if response.candidates:
    for candidate in response.candidates:
      function_call_content = candidate.content
      messages.append(function_call_content)

  # pokud model nevolá funkce (available_functions) pak vrátí prostě odpověď jako text
  # tohle je návratová hodnota celé funkce
  if not response.function_calls:
    return response.text

  # volání funkcí (available_functions), odopvědi jednotlivých volání ukládáme do function_responses
  function_responses = []
  for function_call_part in response.function_calls:
    # reálné volání funkce, výsledek volání uložen do function_call_result a appendován do function_responses
    function_call_result = call_function(function_call_part)
    # odpověď by měla mít .parts[0].function_response, pokud nemá, vyhodí chybu
    if (
      not function_call_result.parts
      or not function_call_result.parts[0].function_response
    ): 
      raise Exception("empty function call result")
    if is_verbose:
      print(f"-> {function_call_result.parts[0].function_response.response}")
    function_responses.append(function_call_result.parts[0])

  if not function_responses:
    raise Exception("no function responses generated, exiting.")

  # do konverzace (promptů pro AI - messages list) appendujeme výsledky volání funkcí  
  messages.append(
    types.Content(
      role="tool",
      parts=function_responses    
    )
  )

if __name__ == "__main__":
  main()
