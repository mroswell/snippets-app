import psycopg2
import logging, argparse,sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet, hide='f', show='t'):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
#    cursor = connection.cursor()
    command = "insert into snippets values ({!r}, {!r}, {!r})".format(name, snippet, hide)
#    command_hide = "update snippets set hidden = 't' where keyword = {!r}".format(name)
#    command_show = "update snippets set hidden = 'f' where keyword = {!r}".format(name)
#    command = "update snippets set message={!r} where keyword={!r}".format(snippet, name)
#    cursor.execute(command)
    # try:
    #     command = "insert into snippets values ({!r}, {!r})".format(name, snippet)
    #     cursor.execute(command)
    # except psycopg2.IntegrityError as e:
    #     connection.rollback()
    #     command = "update snippets set message={!r} where keyword={!r}".format(snippet, name)
    #     cursor.execute(command)
#    connection.commit()
    with connection, connection.cursor() as cursor:
        cursor.execute(command)


    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet a "no snippet" error will be logged.

    Returns the snippet.
    """
    logging.info("Getting snippet - get({!r})".format(name))
    command = "select keyword, message from snippets where keyword={!r} AND where not hidden;".format(name)
#    cursor = connection.cursor()
#    cursor.execute(command)
#    retrieved_snippet = cursor.fetchone()
#    connection.commit()

    with connection, connection.cursor() as cursor:
        cursor.execute(command)
        row = cursor.fetchone()

    logging.debug("Snippet retrieved")
 #   if retrieved_snippet == None:
    if not row:
        return logging.error("no snippet")
    else:
        return row[1]

def catalog():
    """retrieve all the snippet names"""
    command = "select keyword from snippets order by keyword where not hidden;"
    with connection, connection.cursor() as cursor:
        cursor.execute(command)
        rows = cursor.fetchall()
    if not rows:
        return logging.error("no snippets")
    else:
        return rows

def search(term):
    """search snippets by search term"""
    command = "select keyword, message from snippets where message like '%{}%' order by keyword;".format(term)
    with connection, connection.cursor() as cursor:
        cursor.execute(command)
        rows = cursor.fetchall()
    if not rows:
        return logging.error("no snippets match {}".format(term))
    else:
        return rows

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
    put_parser.add_argument("--hide", help="set the hidden flag", action="store_true")
    put_parser.add_argument("--show", help="reset the hidden flag to false", action="store_true")

 #   parser.add_argument("--hide", help="set the hidden flag")

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    put_parser = subparsers.add_parser("get", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")

    # subparser for the catalog
    logging.debug("constructiong catalog subparser")
    put_parser = subparsers.add_parser("catalog", help="list of all snippet names")

    # subparser for search
    logging.debug("constructiong search subparser")
    put_parser = subparsers.add_parser("search", help="snippet search")
    put_parser.add_argument("term", help="Search term")

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
    elif command == "catalog":
        for kw in catalog():
            for item in kw:
                print item
    elif command == "search":
        for sn in search(**arguments):
            print "{}: {}".format(sn[0], sn[1])

if __name__ == "__main__":
    main()
