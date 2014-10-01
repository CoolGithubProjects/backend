import time
import json

import praw
import requests


posts = []
languages = ["python", "cpp", "c", "ruby", "d", "java", "javascript", "shell", "scala", "objective-c", \
             "haskell", "emacs-lisp", "perl", "assembly", "csharp", "fortran", "go", "php", "common-lisp" \
                                                                                            "erlang", "swift"]


def getLanguage(link):
    token = link.strip("/").split("/")
    user = token[-2]
    repo = token[-1]
    r = requests.get('https://api.github.com/repos/' + user + '/' + repo)
    if (r.ok):
        repoItem = json.loads(r.text or r.content)
        language = repoItem['language'].replace(" ", "-").lower()

        # quick fix for reddit css rules
        if language == "c#":
            return "csharp"
        elif language == "c++":
            return "cpp"

        return language
    else:
        print "Unable to get language for url [" + link + "]"
        return None


def main():
    username = raw_input("Bot username : ")
    password = raw_input("Bot password : ")
    r = praw.Reddit(user_agent='coolgithubprojects-bot01', disable_update_check=True)
    r.login(username, password)

    while True:
        try:
            submissions = r.get_subreddit('coolgithubprojects').get_new(limit=10)
            for post in submissions:
                if post not in posts:
                    url = post.url
                    if url.startswith("https://github.com") or url.startswith("http://github.com") or url.startswith(
                            "https://wwww.github.com") or url.startswith("https://github.com") or url.startswith(
                            "http://git.io") or url.startswith("https://git.io") or ".github.io" in url:
                        if post.link_flair_text == None:
                            lang = getLanguage(url)
                            if lang is not None and lang in languages:
                                post.set_flair(flair_text=lang.upper(), flair_css_class=lang)
                                print "Setting language flair to [" + lang + "] for url [" + url + "]"
                            else:
                                post.set_flair(flair_text="OTHER", flair_css_class="other")
                                print "Unsupported language [" + lang + "] for url [" + url + "]"
                        print "Valid post by : " + post.author.name + " " + url
                        posts.append(post)
                    else:
                        author = post.author.name
                        if author == "Diastro" or author == "curlymaster" or author == "Chris911":
                            posts.append(post)
                            continue
                        msg = '''The link you submitted does not point to a valid Github repository. If you think that this is a mistake, please contact the mods.'''
                        post.add_comment(msg)
                        post.remove()
                        print "Deleted : " + str(author) + " " + str(post.title) + " " + str(post.url)
        except Exception, e:
            print str(e)
            print "Error trying again in 120 seconds"
            time.sleep(60)
        time.sleep(15)
    return


if __name__ == "__main__":
    main()