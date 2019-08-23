import logging

from flask import request, Response, Flask

from linter.config import HOST, PORT, DEBUG
from utils.utils import Utils
LOGGER = Utils().user_path()
logging.basicConfig(filename=LOGGER, level=logging.DEBUG)

app = Flask(__name__)

def runner():
    app.run(host=HOST,port=PORT, debug=DEBUG, use_reloader=False)


@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    """Index page"""
    return 'Welcome'


@app.route("/lint", methods=["POST"])
def start_lint():
    try:
        action = request.json["action"]
        pull_request = request.json["pull_request"]
        number = pull_request["number"]
        base_repo_url = pull_request["base"]["repo"]["git_url"]
        head_repo_url = pull_request["head"]["repo"]["git_url"]
        user = pull_request["base"]["repo"]["owner"]["login"]
        repo = pull_request["base"]["repo"]["name"]
    except Exception as e:
        logging.error("Got an invalid JSON body. '%s'", e)
        return Response(status=403,
                        response="You must provide a valid JSON body\n")

    logging.info("Received GitHub pull request notification for "
                 "%s %s, (%s) from: %s",
                 base_repo_url, number, action, head_repo_url)


def close_review(user, repo, pull_request):
    try:
        logging.info("Scheduling cleanup for %s/%s", user, repo)
        #cleanup_pull_request.delay(user, repo, pull_request['number'])
    except:
        logging.error('Could not publish job to celery. '
                  'Make sure its running.')
    return Response(status=204)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False)