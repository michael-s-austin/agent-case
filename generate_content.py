from call_function import available_functions, call_function
from google import genai
from google.genai import types
from prompts import system_prompt


def generate_content(
    client: genai.Client, messages: list[types.Content], verbose: bool, user_prompt: str
) -> str | None:
    """
    Executes the agent's reasonoing loop. 
    Calls the LLM, processes necessary tool calls, updates conversation memory, and returns the final response once task completed.
    """
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if not response.usage_metadata:
            raise RuntimeError("There is no usage metadata available.")

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            function_results = []

            for function_call in response.function_calls:
                try:
                    function_call_result = call_function(function_call, verbose)

                    if not function_call_result.parts:
                        raise Exception(f"Error: No parts found")

                    if not function_call_result.parts[0].function_response:
                        raise Exception(f"Error: No parts found")

                    if not function_call_result.parts[0].function_response.response:
                        raise Exception(f"Error: No parts found")

                    function_results.append(function_call_result.parts[0])

                    if verbose:
                        print(
                            f" -> {function_call_result.parts[0].function_response.response}"
                        )

                except Exception as e:
                    return f"Error: {e}"

            messages.append(types.Content(role="user", parts=function_results))

        else:
            return response.text

    raise Exception(f"Error: Agent loop ran for maximum cycles")
