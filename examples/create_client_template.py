from http import client
from typing import List

from redash_python import Redash
from typer import Argument, Typer

app = Typer(help="Create client dashboard template on redash", no_args_is_help=True)


@app.command(no_args_is_help=True)
def create_client_template(
    api_host: str = Argument(None, envvar="API_HOST", help="Redash API host"),
    api_key: str = Argument(None, envvar="API_KEY", help="Redash API key"),
    client_name: str = Argument(None, help="Client name"),
    template_tags: List[str] = Argument(None, help="Template tags"),
    to_remove_keywords: List[str] = Argument(
        None, help="Keywords to remove widgets with"
    ),
) -> None:
    """
    Create client dashboard template based on another template with given `template_tags` with widgets containing `to_remove_keywords` in their viualization name removed.

    Args:
        api_host: Redash API host
        api_key: Redash API key
        client_name: Client name
        template_tags: tags of template to clone from
        to_remove_tags: keywords to remove widgets from new dashboard with

    Usage:
    ```bash
        python examples/create_client_template.py --api_host https://redash.example.com --api_key 1234567890 --client_name test --template_tags template prod
    ```

    """
    rd = Redash(api_host, api_key)
    ds = rd.dashboards
    omig_template = ds.get_by_tags(template_tags).pop()

    new_id = ds.duplicate(omig_template.get("id"), new_name=f"{client} template").get(
        "id"
    )

    # set tags
    ds.update(new_id, tags=["template", client_name.lower()])

    for widget in ds.get(new_id).get("widgets"):
        if widget.get("visualization"):  # skip text widgets
            if any(
                target in widget.get("visualization").get("name").lower()
                for target in to_remove_keywords
            ):
                rd.widgets.delete(widget.get("id"))

    print(f"Created {client} template with id {new_id}")


if __name__ == "__main__":
    app()
