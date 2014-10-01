import praw
import time

posts = []


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
                    if url.startswith("https://github.com") or url.startswith("http://github.com") or url.startswith("https://wwww.github.com") or url.startswith("https://github.com") or url.startswith("http://git.io") or url.startswith("https://git.io") or ".github.io" in url:
                        #if post.link_flair_text == None:
                            #print "No flair " + str(post.title)
                            #l = getLanguage(url)

                        print "Valid post by : " + post.author.name + " " + url
                    else:
                        author = post.author.name
                        if author == "Diastro" or author == "curlymaster" or author == "Chris911":
                            continue
                        msg = '''The link you submitted does not point to a valid Github repository. If you think that this is a mistake, please contact the mods.'''
                        post.add_comment(msg)
                        post.remove()
                        print "Deleted : " + str(author) + " " + str(post.title) + " " + str(post.url)
                    posts.append(post)
        except Exception,e:
            print str(e)
            print "Error trying again in 120 seconds"
            time.sleep(120)
        time.sleep(60)
    return


if __name__ == "__main__":
    main()