# Github_script


### Commit History

`$python`

`>>>from utils import save_commit_history`

`>>>from datetime import datetime`

`>>>repo_owner_username = 'repo_owner'`

`>>>repo_name = 'repo_name'`

`>>>start_time = datetime.now() - timedelta(days=7) # must be datetime`

`>>>end_time = datetime.now()`

`>>>save_commit_history(repo_owner_username, repo_name, start_time:datetime, end_time:datetime)`
