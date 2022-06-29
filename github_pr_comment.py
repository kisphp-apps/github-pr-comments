#!/usr/bin/env python3

import json
import os
import sys
import urllib3


class RequestManager:
    def __init__(self, github_repositoy, github_token):
        self.http = urllib3.PoolManager()
        self.headers = {
            'Accept': "application/vnd.github.v3+json",
            'Authorization': f'token {github_token}'
        }
        self.github_base_url = f"https://api.github.com/repos/{github_repositoy}/issues"

    def get_comments(self, issue_number):
        """
          curl \
          -H "Accept: application/vnd.github.v3+json" \
          -H "Authorization: token <TOKEN>" \
          https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments
                """
        r = self.http.request('GET', f"{self.github_base_url}/{issue_number}/comments", headers=self.headers)
        if r.status != 200:
            return None

        return json.loads(r.data.decode('utf-8'))

    def delete_comment(self, comment_id):
        """
        curl \
  -X DELETE \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token <TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/issues/comments/COMMENT_ID
        """
        print(f'delete comment: {comment_id}')
        url = f"{self.github_base_url}/comments/{comment_id}"
        return self.http.request('DELETE', url, headers=self.headers)

    def post_comment(self, issue_number, message):
        """
        curl \
          -X POST \
          -H "Accept: application/vnd.github.v3+json" \
          -H "Authorization: token <TOKEN>" \
          https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments \
          -d '{"body":"Me too"}'
        """
        url = f"{self.github_base_url}/{issue_number}/comments"

        body_content = json.dumps({
            "body": message
        })

        print(f"Post message url: {url}")
        response = self.http.request('POST', url, headers=self.headers, body=body_content)

        print(f'Response status: {response.status}')
        print(f'Response reason: {response.reason}')


class GithubPrManager:
    PR_COMMENT_MARKUP = '<!--PR_COMMENT-->'
    GITHUB_COMMENT_MAX_CHARS = 241000

    def __init__(self, request_manager: RequestManager):
        self.request = request_manager

    def post_comment(self, issue_id, filename, comment_title):
        with open(filename, 'r') as file:
            content = file.read()

        if os.getenv('GITHUB_PR_SKIP_DELETE') != True:
            print('get comments')
            for comment in self._get_issue_comments(issue_id):
                print(f'found comment {comment.get("id")}')
                if (GithubPrManager.PR_COMMENT_MARKUP) in comment.get('body'):
                    print(f'delete comment {comment.get("id")}')
                    self._delete_issue_comment(comment.get('id'))

        for message in self.split_content(content):
            print(f'post the comment to issue {issue_id}')
            pre_start = ''
            pre_end = ''
            if bool(os.getenv('GITHUB_PR_COMMENT_PRE')) is True:
                pre_start = '<pre>'
                pre_end = '</pre>'

            comment_message = f"""
{comment_title}
{GithubPrManager.PR_COMMENT_MARKUP}
<details>
  <summary>Click to expand!</summary>

  {pre_start}{message}{pre_end}
</details>

"""
            self.request.post_comment(issue_id, comment_message)

    def split_content(self, content):
        print(self.GITHUB_COMMENT_MAX_CHARS)
        if len(content) < self.GITHUB_COMMENT_MAX_CHARS:
            return [content]

        split_content = []
        while len(content) > 0:
            sliced = content[:self.GITHUB_COMMENT_MAX_CHARS]
            split_content.append(sliced)
            content = content[self.GITHUB_COMMENT_MAX_CHARS:]

        return split_content

    def _get_issue_comments(self, issue_id):
        comments = self.request.get_comments(issue_id)

        return comments or []

    def _delete_issue_comment(self, comment_id):
        return self.request.delete_comment(comment_id)


if __name__ == '__main__':
    rm = RequestManager(
        os.getenv('GITHUB_REPOSITORY'),
        os.getenv('GITHUB_TOKEN')
    )
    g = GithubPrManager(rm)
    g.post_comment(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3]
    )
