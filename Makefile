.PHONY: build run

build:
	docker build --no-cache -t github-pr-comments .

run:
	docker run \
	-e GITHUB_OWNER=kisphp-apps \
	-e GITHUB_REPO=iac-github \
	-e GITHUB_TOKEN=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 \
	-e GITHUB_PR_COMMENT_FILENAME=tfsec-output.txt \
	-e GITHUB_PR_NUMBER=17 \
	-it github-pr-comments bash
