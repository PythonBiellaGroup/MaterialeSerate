import openai
import typer
# from loguru import logger
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from app.src.config import settings

openai.organization = settings.OPENAI_ORGANIZATION
openai.api_key = settings.OPENAI_API_KEY

app = typer.Typer()

app.command()
def help():
    print("Ciao benvenuto su Python Biella Group OPENAI Example CLI")
    print("What do you want to do?")
    print("- \t [bold green]request[/bold green] to launch a request")
    print("- \t [bold green]models[/bold green] to select a model")
    selection = typer.prompt("Seleziona una delle opzioni sopra elencate")
    if selection.lower().strip() == "request":
        launch_request()
    if selection.lower().strip() == "models":
        select_models()
    else:
        print("Non hai selezionato nessuna delle opzioni elencate, riprova")
    
    return None

app.command()
def launch_request(
    message_content: str = "",
    model: str = "gpt-4",
    input_max_tokens: int = 8000,
    input_temperature: float = 0.5,
):
    
    # type prompts
    model = typer.prompt(f"Che tipo di modello vuoi usare? (default {model})", default="gpt-4", type=str)
    message_content = typer.prompt("Cosa vuoi chiedere?", type=str)
    input_max_tokens = typer.prompt(f"Numero massimo di token? (default {input_max_tokens})", default=8000, type=int)
    input_temperature = typer.prompt(f"Temperatura? (default {input_temperature})", default=0.5, type=float)
    
    messages = [{"role": "user", "content": message_content}]
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Sto generando la risposta...", total=None)
        completion = openai.ChatCompletion.create(
            model=model, messages=messages, max_tokens=input_max_tokens, temperature=input_temperature)
    message = completion.choices[0].message.content
    
    # logger.debug(message)
    print(message)
    return message

app.command()
def select_models():
    model_list = openai.Model.list()
    # logger.debug(model_list)
    print(model_list)
    return model_list
