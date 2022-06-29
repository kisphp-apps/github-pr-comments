# Github PR collapsible comments

Post comments on PRs and issues and delete the old ones that were created before. It will delete only the messages that it wrote before.
For example, this tool is useful to post tfsec report for a terraform repository.

## Inputs

## `pr_number`
**Required** The PR number where to post the message to.

## `filename`
**Required** The filename path that will be read and post is content as comment.

## `title`
**Optional** A short description for the collapsible comment.

## Example usage

```yaml
- uses: kisphp-apps/github-pr-comments@pr-comments
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    pr_number: ${{ github.event.number }}
    filename: "tfsec-output.txt"
    title: "tfsec report"
```
