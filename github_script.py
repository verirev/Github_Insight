import requests
from datetime import datetime, timezone, timedelta
import pprint
pp = pprint.PrettyPrinter(indent=2)

def common_getter(url:str, auth_tuple:tuple = ())->dict:
    """Takes url and returns dict as result
    """
    headers = {"Authorization": f"Bearer {auth_tuple[1]}"}
    headers['Accept'] = 'application/vnd.github+json'
    response_data = requests.get(url=url, headers=headers, auth=auth_tuple)
    return response_data.json()

def get_committer(committer_url:str, auth_tuple:tuple = ())->list:
    return common_getter(committer_url, auth_tuple)

def get_puller(committer_url:str, auth_tuple:tuple = ())->list:
    return common_getter(committer_url, auth_tuple)

def time_in_range(start,end, current):
    return start <= current <= end

def time_bool_check(i:dict, start_time:datetime, end_time:datetime):
    time_now = datetime.now()
    time_now_iso = time_now.strftime('%Y-%m-%dT%H:%M:%SZ')
    _created_at = i.get('created_at', time_now_iso)
    _updated_at = i.get('updated_at', time_now_iso)
    _closed_at = i.get('closed_at', time_now_iso)
    _merged_at = i.get('merged_at', time_now_iso)
    _updated_at = time_now_iso if bool(_updated_at) == False else _updated_at
    _closed_at = time_now_iso if bool(_closed_at) == False else _closed_at
    _merged_at = time_now_iso if bool(_merged_at) == False else _merged_at
    created_at = datetime.strptime(_created_at, '%Y-%m-%dT%H:%M:%SZ')
    updated_at = datetime.strptime(_updated_at, '%Y-%m-%dT%H:%M:%SZ')
    closed_at = datetime.strptime(_closed_at, '%Y-%m-%dT%H:%M:%SZ')
    merged_at = datetime.strptime(_merged_at, '%Y-%m-%dT%H:%M:%SZ')
    created_bool = time_in_range(start_time, end_time, created_at)
    updated_bool = time_in_range(start_time, end_time, updated_at)
    closed_bool = time_in_range(start_time, end_time, closed_at)
    merged_bool = time_in_range(start_time, end_time, merged_at)
    return created_bool or updated_bool or closed_bool or merged_bool

def save_commit_history(repo_owner_username, repo_name, start_time:datetime, end_time:datetime ):
    # current_time = datetime.now()
    # one_week_earlier = current_time -timedelta(days=80)
    # end_time = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    # start_time = one_week_earlier.strftime('%Y-%m-%dT%H:%M:%SZ')
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    # 2022-08-08T04:17:20Z
    # 2022-08-08T04:20:20Z
    from config import ACCESS_TOKEN
    auth_t = (repo_owner_username, ACCESS_TOKEN)
    commits_url_str = f'https://api.github.com/repos/{auth_t[0]}/{repo_name}/commits?since={start_time_str}=&until={end_time_str}'
    commit_list = get_committer(commits_url_str, auth_tuple=auth_t)
    # pp.pprint(commit_list)
    # print(commits_url_str)
    import pyexcel as pe
    output_list  = []
    for i in commit_list:
        commit_obj = i.get('commit', {})
        commit_sha = i.get('sha', '')
        commit_url = i.get('html_url', '')
        repo_author = i.get('author', {}).get('login', '')
        commit_author = commit_obj.get('author',{}).get('name', '')
        commit_time = commit_obj.get('author',{}).get('date', '')
        message_str = commit_obj.get('message','')
        _parents = i.get('parents', [])
        parents = _parents[0].get('html_url', '') if bool(len(_parents)) else ''
        single_list = [repo_name, repo_author, commit_sha, commit_url, commit_time, message_str, commit_author, parents ]
        output_list.append(single_list)
    output_list.insert(0,['Repository', 'Repo Author', 'Commit SHA', 'Commit URL', 'Commit Time', 'Commit Message', 'Commit Author', 'Commit Parents'])
    pe.save_as(array=output_list, dest_file_name=f'Commit-{repo_name}-{start_time}-{end_time}.xlsx')


def save_pull_history(repo_owner_username, repo_name, start_time:datetime, end_time:datetime, other_query_params:dict = {} ):
    # 2022-08-08T04:17:20Z
    # 2022-08-08T04:20:20Z
    from config import ACCESS_TOKEN
    auth_t = (repo_owner_username, ACCESS_TOKEN)
    query_builder = ''
    if bool(other_query_params):
        query_builder +='?'
        for key in list(other_query_params.keys()):
            query_builder +=f'{key}={other_query_params[key]}&'
    pull_url_str = f'https://api.github.com/repos/{auth_t[0]}/{repo_name}/pulls{query_builder}'
    _pull_list = get_puller(pull_url_str, auth_tuple=auth_t)
    import pyexcel as pe
    output_list  = []
    for i in _pull_list:
        time_bool_val = time_bool_check(i, start_time, end_time)
        if time_bool_val:
            pull_url = i.get('html_url', '')
            pull_id = i.get('id', '')
            diff_url = i.get('diff_url', '')
            patch_url = i.get('patch_url', '')
            issue_url = i.get('issue_url', '')
            state = i.get('state', '')
            title = i.get('title', '')
            body = i.get('body', '')
            head = i.get('head', {})
            base = i.get('base', {})
            head_sha = head.get('sha','')
            head_label = head.get('label','')
            base_sha = base.get('sha','')
            base_label = base.get('label','')
            user = i.get('user', {}).get('login', '')
            _created_at = i.get('created_at', '')
            _updated_at = i.get('updated_at', '')
            _closed_at = i.get('closed_at', '')
            _merged_at = i.get('merged_at', '')
            single_list = [repo_name, repo_owner_username, title, pull_url, pull_id, user, state, diff_url, patch_url, issue_url, body, head_label, head_sha, base_label, base_sha, _created_at, _updated_at, _closed_at, _merged_at ]
            output_list.append(single_list)
    output_list.insert(0,['Repository', 'Repo Author', 'Pull Title', 'Pull URL',  'Pull ID', 'User', 'STAT', 'Diff URL', 'Patch URL', 'Issue URL', 'Pull Body', 'Head Label', 'Head SHA', 'Base Label', 'Base SHA', 'Created at', 'Updated at', 'Closed at', 'Merged at'])
    pe.save_as(array=output_list, dest_file_name=f'Pull-{repo_name}-{start_time}-{end_time}.xlsx')

# save_pull_history('d3plus','d3plus', datetime.now()-timedelta(days=400), datetime.now()-timedelta(days=7))
