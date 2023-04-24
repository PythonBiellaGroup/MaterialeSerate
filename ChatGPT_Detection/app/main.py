import typer
from app.src.openai import help

if __name__ == "__main__":
    typer.run(help)
    # select_models()
    # launch_request("Ciao! Come stai? Cosa puoi fare?", model="gpt-4",input_temperature=0.5, input_max_tokens=100)
