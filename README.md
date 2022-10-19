# Github_script


# Commit History
Function name `save_commit_history`

`$python`

`>>>from github_script import save_commit_history`

`>>>from datetime import datetime`

`>>>repo_owner_username = 'repo_owner'`

`>>>repo_name = 'repo_name'`

`>>>start_time = datetime.now() - timedelta(days=7) # must be datetime`

`>>>end_time = datetime.now()`

`>>>save_commit_history(repo_owner_username, repo_name, start_time:datetime, end_time:datetime)`

# Pull history
Similar to Commit history. Function name `save_pull_history`
# Query parameters

## `state` **string**

Either `open`, `closed`, or `all` to filter by state.

Default: `open`

Can be one of: `open`, `closed`, `all`


## `head` **string**

Filter pulls by head user or head organization and branch name in the format of `user:ref-name` or `organization:ref-name`. For example: `github:new-script-format` or `octocat:test-branch`.

## `base` **string**

Filter pulls by base branch name. Example: `gh-pages`.

## `sort` **string**

What to sort results by. `popularity` will sort by the number of comments. `long-running` will sort by date created and will limit the results to pull requests that have been open for more than a month and have had activity within the past month.

Default: `created`

Can be one of: `created`, `updated`, `popularity`, `long-running`

## `direction` **string**

The direction of the sort. Default: `desc` when sort is `created` or sort is not specified, otherwise `asc`.

Can be one of: `asc`, `desc`

## `per_page` **integer**

The number of results per page (max 100).

Default: `30`

## `page` **integer**
Page number of the results to fetch.

Default: `1`

**These all has to be in a form of key, value python dictionary to be passed as function param to `save_pull_history` as `other_query_params`**