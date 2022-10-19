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
    repo_name = 'systems-notebook'
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
    pe.save_as(array=output_list, dest_file_name=f'{repo_name}-{start_time}-{end_time}.xlsx')
