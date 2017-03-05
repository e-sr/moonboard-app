import requests
import bs4
import re

from matplotlib.pyplot import hold
from tqdm import tqdm as tqdm_progress
import json

MOONBOARD_PROBLEMS_URL = "http://www.moonboard.com/problems/"

def get_all_problems_ids():
    """get all problems id"""
    problems = {}
    r = requests.get(MOONBOARD_PROBLEMS_URL)
    w_soup = bs4.BeautifulSoup(r.content, 'lxml')
    problems_tags = w_soup.find_all(lambda tag: tag.name == 'div' and ('problem-id' and 'grade-val' in tag.attrs))
    for p in problems_tags:
        cl = p.get('class')
        problems[p.get('problem-id')] = {'grade_val': p.get('grade-val'),
                                         'class': cl,
                                         'author': (" ".join(cl[4:])).strip()
                                         }
    return problems


def get_new_problems_ids(old_problems=None):
    problems = get_all_problems_ids()
    new_problems_keys = set(problems.keys()) - set(old_problems.keys())
    return {k: v for k, v in problems.items() if k in new_problems_keys}


def sort_holds(holds):
    holds_d= {}
    for holdType in ['SH','IH','FH']:
        sortedKeys = sorted([k for k in holds.keys() if holdType in k])
        holds2 = [holds[k] for k in sortedKeys]
        holds_d[holdType] = [h for h in holds2 if h is not ""]
    return holds_d

def get_problem_data(problem_id):
    url = MOONBOARD_PROBLEMS_URL + "?p={}/".format(problem_id)
    r = requests.get(url)
    web_soup = bs4.BeautifulSoup(r.content, 'lxml')
    summary = web_soup.findAll('div', attrs={'class': 'summary'})
    if len(summary) > 2:
        raise ValueError
    s = summary[1]
    holds= {hold.get('id').strip(): hold.get('name').strip() for hold in s.find_all(id=re.compile("^FH|^IH|^SH"))}

    p_info = {'name': s.find('h1', attrs={'class': 'post-title'}).decode_contents().strip(),
              'grade': s.find('div', attrs={'id': 'font_grade'}).decode_contents().strip().lower(),
              'hold_sets': [c.strip() for c in s.children if c.name != 'div' and "Hold" in c],
              'holds': sort_holds(holds)
              }
    return p_info


def validate_problem(problems_data):
    return True


def update_problems(problems, nmax=10000):
    print('fetch problems ids')
    new_problems = get_new_problems_ids(problems)
    n = 0
    errors = []
    added = []
    print('fetch single problems')
    for k, p in tqdm_progress(new_problems.items()):
        try:
            p_d = get_problem_data(k)
        except:
            errors.append(k)
        else:
            if validate_problem(p_d):
                problems[k] = p
                problems[k].update(p_d)
                added.append(k)
                n += 1
            else:
                errors.append(k)
        if n > nmax:
            break
    # save
    print("Save to file")
    with open('problems.json', 'w+') as output:
        # Pickle dictionary using protocol 0.
        json.dump(problems, output)
    return errors, added

##
if __name__=="__main__":
    print('get moonboard problems \n==============')
    try:
        print("Read problems from 'problems.json'")
        PROBLEMS = json.load(open('problems.json', 'r+'))
    except FileNotFoundError:
        print("File not found")
        PROBLEMS = {}
        print('Empty problems dict')
    else:
        print("Problems founds: {}".format(len(PROBLEMS)))


    print("Update problems")
    errors, added = update_problems(PROBLEMS,nmax=100)

    print('=========\nTotal number of problems:', len(PROBLEMS), '\nAdded:', added, '\nErrors:', errors)






