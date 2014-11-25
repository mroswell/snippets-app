import psycopg2
import logging, argparse,sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values ({!r}, {!r})".format(name, snippet)
    cursor.execute(command)
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet a "no snippet" error will be logged.

    Returns the snippet.
    """
    logging.info("FIXME: Getting snippet - get({!r})".format(name))
    cursor = connection.cursor()
    command = "select keyword, message from snippets where keyword={!r};".format(name)
    cursor.execute(command)
    retrieved_snippet = cursor.fetchone()
    connection.commit()
    logging.debug("Snippet retrieved")
    return retrieved_snippet[1]

def delete(name):
    """
    Delete a snippet with an associated name.

    """
    logging.error("FIXME: Unimplemented - delete({!r}, {!r}".format(name,snippet))

def patch(name, snippet):
    """
    Update a snippet with an associated name
    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - patch({!r},{!r}".format(name, snippet))
    return name, snippet

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    put_parser = subparsers.add_parser("get", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")

    arguments = parser.parse_args(sys.argv[1:])
   # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))


if __name__ == "__main__":
    main()
