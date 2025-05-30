import requests


# 配置信息
GITHUB_TOKEN = "11"  # GitHub个人访问令牌
UPSTREAM_OWNER = "Sjj1024"  # 上游仓库所有者
UPSTREAM_REPO = "PakePlus-iOS"  # 上游仓库名
FORK_OWNER = "1024dashen"  # 你的fork仓库所有者
FORK_REPO = "PakePlus-iOS"  # 你的fork仓库名

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_all_branches(owner, repo):
    """获取仓库所有分支"""
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"获取分支失败: {response.text}")
    return [branch["name"] for branch in response.json()]


def sync_branch(upstream_branch, fork_branch):
    """同步单个分支"""
    # 1. 检查fork中是否存在该分支
    fork_branch_url = f"https://api.github.com/repos/{FORK_OWNER}/{FORK_REPO}/branches/{fork_branch}"
    response = requests.get(fork_branch_url, headers=headers)

    # 如果分支不存在，先创建
    if response.status_code == 404:
        print(f"分支 {fork_branch} 不存在，创建新分支...")
        create_branch(fork_branch)

    # 2. 创建合并提交（始终接受上游更改）
    merge_url = f"https://api.github.com/repos/{FORK_OWNER}/{FORK_REPO}/merges"
    merge_data = {
        "base": fork_branch,
        "head": f"{UPSTREAM_OWNER}:{upstream_branch}",
        "commit_message": f"Auto-sync with upstream {upstream_branch} by PakePlus"
    }

    response = requests.post(merge_url, headers=headers, json=merge_data)

    if response.status_code == 201:
        print(f"成功合并 {upstream_branch} 到 {fork_branch}")
    elif response.status_code == 204:
        print(f"分支 {fork_branch} 已经是最新状态")
    else:
        print(f"合并失败: {response.text}")
        # 如果合并冲突，强制覆盖
        force_update_branch(upstream_branch, fork_branch)


def create_branch(branch_name):
    """在fork中创建新分支（基于上游分支）"""
    # 获取上游分支的最新提交
    upstream_ref_url = f"https://api.github.com/repos/{UPSTREAM_OWNER}/{UPSTREAM_REPO}/git/refs/heads/{branch_name}"
    response = requests.get(upstream_ref_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"获取上游分支引用失败: {response.text}")

    upstream_sha = response.json()["object"]["sha"]

    # 在fork中创建引用
    create_ref_url = f"https://api.github.com/repos/{FORK_OWNER}/{FORK_REPO}/git/refs"
    ref_data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": upstream_sha
    }

    response = requests.post(create_ref_url, headers=headers, json=ref_data)
    if response.status_code != 201:
        raise Exception(f"创建分支失败: {response.text}")
    print(f"成功创建分支 {branch_name}")


def force_update_branch(upstream_branch, fork_branch):
    """强制更新分支（解决冲突时使用）"""
    # 获取上游分支的最新提交
    upstream_ref_url = f"https://api.github.com/repos/{UPSTREAM_OWNER}/{UPSTREAM_REPO}/git/refs/heads/{upstream_branch}"
    response = requests.get(upstream_ref_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"获取上游分支引用失败: {response.text}")

    upstream_sha = response.json()["object"]["sha"]

    # 强制更新fork分支引用
    update_ref_url = f"https://api.github.com/repos/{FORK_OWNER}/{FORK_REPO}/git/refs/heads/{fork_branch}"
    ref_data = {
        "sha": upstream_sha,
        "force": True
    }

    response = requests.patch(update_ref_url, headers=headers, json=ref_data)
    if response.status_code != 200:
        raise Exception(f"强制更新分支失败: {response.text}")
    print(f"强制更新分支 {fork_branch} 到上游 {upstream_branch} 的最新状态")


def sync_all_branches():
    """同步所有分支"""
    print("开始同步所有分支...")
    # 获取上游所有分支
    upstream_branches = get_all_branches(UPSTREAM_OWNER, UPSTREAM_REPO)
    print(f"上游分支: {upstream_branches}")

    # 获取fork所有分支
    fork_branches = get_all_branches(FORK_OWNER, FORK_REPO)
    print(f"Fork分支: {fork_branches}")

    # 同步每个分支
    for branch in upstream_branches:
        print(f"\n正在同步分支: {branch}")
        sync_branch(branch, branch)

    print("\n同步完成")


if __name__ == "__main__":
    sync_all_branches()
