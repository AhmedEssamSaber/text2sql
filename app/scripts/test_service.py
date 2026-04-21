from app.llm.generator import SQLGenerator

def main():
    model_path = r"D:\Ai courses\text2sql\merged-model"

    generator = SQLGenerator(model_path)

    while True:
        question = input("\nEnter your question (or 'exit'): ")

        if question.lower() == "exit":
            break

        prompt = f"""You are an expert SQL generator.

### Rules:
- Return ONLY SQL query
- No explanation

### User Question:
{question}

### SQL Query:
"""

        result = generator.generate(prompt)

        print("\n===== SQL =====")
        print(result)


if __name__ == "__main__":
    main()