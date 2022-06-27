# Github PR collapsible comments

Post comments on PRs and issues and delete the old ones that were created before. It will delete only the messages that it wrote before.
For example, this tool is useful to post tfsec report for a terraform repository.

## Inputs

## `message`

**Required** The message to be added to the PR.

## Example usage

```yaml
uses: kisphp-apps/github-pr-comments
with:
  message: "this is my message"
```