import random

commit_list = ["我支持你", "了解一下", "发帖辛苦", "我喜欢这个", "点赞支持", "感谢分享", "你很棒",
               "我很喜欢", "感谢你的发帖", "还有更骚的", "你很厉害"]
commit = random.choices(commit_list, k=5)
print(commit)