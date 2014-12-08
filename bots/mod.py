import time
import json
import os
import inspect
import ConfigParser

import praw
import requests

basePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.chdir(basePath)

posts = []
languages = ['mercury', 'objective-cpp', 'self', 'edn', 'rebol', 'xbase', 'eiffel', 'elixir', 'agda', 'perl6', 'mirah',
             'objective-j', 'gosu', 'component-pascal', 'go', 'visual-basic', 'php', 'cirru', 'verilog', 'red', 'volt',
             'lsl', 'coffeescript', 'latte', 'swift', 'c', 'isabelle', 'autoit', 'rust', 'sourcepawn', 'shen', 'tcl',
             'vhdl', 'oxygene', 'assembly', 'csharp', 'turing', 'processing', 'emacs-lisp', 'ooc', 'mask', 'emberscript',
             'nemerle', 'krl', 'ocaml', 'antlr', 'fsharp', 'smalltalk', 'pogoscript', 'livescript', 'javascript', 'slash',
             'erlang', 'objective-c', 'eagle', 'scheme', 'python', 'nimrod', 'chapel', 'dylan', 'alloy', 'pawn',
             'purescript', 'julia', 'haskell', 'io', 'rouge', 'dogescript', 'nesc', 'typescript', 'dart', 'frege',
             'aspectj', 'shell', 'arduino', 'supercollider', 'mtml', 'sas', 'd', 'opal', 'standard-ml',
             'coldfusion-cfc', 'pure-data', 'arc', 'nit', 'apl', 'sqf', 'glyph', 'java', 'scala', 'perl', 'factor',
             'haxe', 'forth', 'hy', 'ruby', 'lfe', 'autohotkey', 'boo', 'clojure', 'css', 'prolog', 'coldfusion',
             'harbour', 'blitzmax', 'piglatin', 'lasso', 'clean', 'propeller-spin', 'idl', 'ats', 'ada', 'nu', 'asp',
             'flux', 'vala', 'ecl', 'netlogo', 'qml', 'fantom', 'pike', 'r', 'unified-parallel-c', 'lua', 'wisp',
             'pascal', 'puppet', 'actionscript', 'ragel-in-ruby-host', 'zephir', 'dm', 'ioke', 'gnuplot', 'viml',
             'matlab', 'pan', 'lookml', 'max', 'common-lisp', 'xquery', 'systemverilog', 'groovy', 'e', 'parrot',
             'grammatical-framework', 'vcl', 'cpp', 'fortran', 'ags-script', 'tex', 'unrealscript', 'slim', 'fancy',
             'omgrofl', 'game-maker-language', 'racket']

def log(msg):
    print str(time.strftime("%d/%m/%Y %I:%M:%S")) + " - " + msg


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
        elif language == "objective-c++":
            return "objective-cpp"
        elif language == "f#":
            return "fsharp"

        return language
    else:
        print "Unable to get language for url [" + link + "]"
        return None

def main():
    configParser = ConfigParser.RawConfigParser(allow_no_value=False)
    configParser.read(basePath + '/config')
    username = configParser.get('mod-bot', 'username')
    password = configParser.get('mod-bot', 'password')

    r = praw.Reddit(user_agent='coolgithubprojects-bot01', disable_update_check=True)
    r.login(username, password)

    while True:
        try:
            submissions = r.get_subreddit('coolgithubprojects').get_new(limit=10)
            for post in submissions:
                if post not in posts:
                    url = post.url
                    if (url.startswith("https://github.com") or 
                        url.startswith("http://github.com") or 
                        url.startswith("https://wwww.github.com") or 
                        url.startswith("http://wwww.github.com") or 
                        url.startswith("http://git.io") or 
                        url.startswith("https://git.io") or  
                        ".github.io" in url):
                        if post.link_flair_text == None:
                            lang = getLanguage(url)
                            if lang is not None and lang in languages:
                                post.set_flair(flair_text=lang.upper(), flair_css_class=lang)
                                log("Setting language flair to [" + lang + "] for url [" + url + "]")
                            else:
                                post.set_flair(flair_text="OTHER", flair_css_class="other")
                                print "Unsupported language [" + lang + "] for url [" + url + "]"
                        log("Valid post by [" + post.author.name + "] [" + url + "]")
                        posts.append(post)
                    else:
                        author = post.author.name
                        if author == "Diastro" or author == "curlymaster" or author == "Chris911":
                            posts.append(post)
                            continue
                        msg = '''The link you submitted does not point to a valid Github repository. If you think that this is a mistake, please contact the mods.'''
                        post.add_comment(msg)
                        post.remove()
                        log("Deleted post by [" + str(author) + "] [" + str(post.url) + "]")
        except Exception, e:
            log("Error " + "[" + str(e) + "]")
            time.sleep(60)
        time.sleep(5)
    return


if __name__ == "__main__":
    main()
