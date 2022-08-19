from redash_python import Redash
from typer import Argument, Typer

app = Typer(
    name="Churn Prediction Migration",
    help="clanup for updated churn pipeline.",
    no_args_is_help=True,
)


@app.command()
def clean(
    host_url: str = Argument(None, envvar="REDASH_HOST", help="Redash host"),
    api_key: str = Argument(None, envvar="REDASH_API_KEY", help="Redash api key"),
) -> None:
    """
    Clean up all the customer dashboards on redash
    """

    rd = Redash(host_url, api_key)

    admin_tags = ["admin", "template", "maintenance"]
    user_ques = rd.queries.get_by_tags(tags=admin_tags, without=True)
    user_dashs = rd.dashboards.get_by_tags(tags=admin_tags, without=True)

    if not user_ques:
        print("No user Queries found!")
    else:
        list(map(rd.queries.delete, [q.get("id") for q in user_ques]))
        print("Archived all user queries")

    if not user_dashs:
        print("No user Dashboards found!")
    else:
        list(map(rd.dashboards.delete, [d.get("id") for d in user_dashs]))
        print("Archived all user dashboards")


if __name__ == "__main__":
    app()
