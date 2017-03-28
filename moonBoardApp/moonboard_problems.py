import requests
import bs4
import re
import json
import string

HOLDS_CONF = { "sets":["A","B","OS"],
               "configurations":{
                   'Hold Set B 2016':{"shortName":"B 2016", "set":"B", "placement":{}},
                   'Hold Set A 2016':{"shortName":"A 2016", "set":"A", "placement":{}},
                   'Original School Holds 2016':{"shortName":"OS 2016", "set":"OS", "placement":{}}
               },
               "setup":{
                   1:{'Hold Set B 2016', 'Hold Set A 2016', 'Original School Holds 2016'},
                   2:{'Hold Set B 2016', 'Hold Set A 2016'},
                   3:{'Hold Set B 2016', 'Original School Holds 2016'},
                   4:{'Hold Set A 2016', 'Original School Holds 2016'},
                   5:{'Hold Set B 2016'},
                   6:{'Original School Holds 2016'},
                   7:{'Hold Set A 2016'}
               },
               "grid":{
                   "vertical":string.ascii_uppercase[0:11],
                   "horizontal":list(range(1, 19)),
               }
               }

HOLDS_CONF["grid"]["xy"]= [v+str(h) for v in HOLDS_CONF["grid"]["vertical"] for h in HOLDS_CONF["grid"]["horizontal"]]

MOONBOARD_PROBLEMS_URL = "http://www.moonboard.com/problems/"
PROBLEMS = {}

def load_problems(path):
    try:
        print("Read problems from 'problems.json'")
        problems = json.load(open(path, 'r+'))
    except IOError:
        print("File not found")
        problems = {}
        print('Empty problems dict')
    else:
        print("Problems founds: {}".format(len(problems)))
    return problems

def _new_problem(name, grade,holds_setup,SH,IH,FH,author, type="personal", site_id=None):
    if type not in ["site","personal"]:
        type = None
    problem = {
        "name":name,
        "grade":grade,
        "holds_setup":holds_setup,
        "holds":{"SH":SH,
                 "IH":IH,
                 "FH":FH},
        "author":author,
        "site_id":site_id,
        "type":type,
    }
    #validate_problem()
    return problem

def _add_problem(problems, new):
    #todo
    problems[new['site_id']]=new


###====================
def site_get_all_problems_ids():
    """get all problems id"""
    problems = {}
    r = requests.get(MOONBOARD_PROBLEMS_URL)
    w_soup = bs4.BeautifulSoup(r.content, 'lxml')
    problems_tags = w_soup.find_all(lambda tag: tag.name == 'div' and ('problem-id' and 'grade-val' in tag.attrs))
    for p in problems_tags:
        cl = p.get('class')
        problems[p.get('problem-id')] = {#'grade_val': p.get('grade-val'),
            #'class': cl,
            'author': (" ".join(cl[4:])).strip()
        }
    return problems

def site_get_new_problems_ids(old_problems=None):
    problems = site_get_all_problems_ids()
    new_problems_keys = set(problems.keys()) - set(old_problems.keys())
    return {k: v for k, v in problems.items() if k in new_problems_keys}

def site_sort_holds(holds):
    holds_d= {}
    for holdType in ['SH','IH','FH']:
        sortedKeys = sorted([k for k in holds.keys() if holdType in k])
        holds2 = [holds[k] for k in sortedKeys]
        holds_d[holdType] = [h for h in holds2 if h in HOLDS_CONF["grid"]["xy"]]
    return holds_d

def site_get_problem_data(problem_id):
    url = MOONBOARD_PROBLEMS_URL + "?p={}/".format(problem_id)
    r = requests.get(url)
    web_soup = bs4.BeautifulSoup(r.content, 'lxml')
    summary = web_soup.findAll('div', attrs={'class': 'summary'})
    if len(summary) > 2:
        raise ValueError
    s = summary[1]
    holds= {hold.get('id').strip(): hold.get('name').strip() for hold in s.find_all(id=re.compile("^FH|^IH|^SH"))}

    p_info = {
        'name': s.find('h1', attrs={'class': 'post-title'}).decode_contents().strip(),
        'grade': s.find('div', attrs={'id': 'font_grade'}).decode_contents().strip().lower(),
        'holds_setup': sorted([c.strip() for c in s.children if c.name != 'div' and "Hold" in c]),
        'type':'site',
        'site_id':problem_id,

    }
    p_info.update(site_sort_holds(holds))
    return p_info


def site_update_problems(problems, log_func, nmax=10):
    #problems['updated'] = str(datetime.datetime.now())
    log_func('fetch problems ids')
    new_problems = site_get_new_problems_ids(problems)
    n = 0
    errors = []
    added = []
    i=0
    log_func('fetch new problems')
    n_p = len(new_problems)
    for k, p in new_problems.items():
        try:
            p_d = site_get_problem_data(k)
        except:
            errors.append(k)
        else:
            p.update(p_d)
            new = _new_problem(**p)
            _add_problem(problems,new)
            added.append(k)
            n += 1
        if n > nmax:
            break

        i+=1
        log_func("{}/{}, {}%".format(n,n_p,int(n/n_p*100)))
    # save
    log_func("Save to file")
    with open('problems.json', 'w+') as output:
        # Pickle dictionary using protocol 0.
        json.dump(problems, output)
    return errors, added

##
if __name__=="__main__":
    PROBLEMS = load_problems('problems.json')
    print("Update problems")
    def log_func(s):
        print(s)
    errors, added = site_update_problems(PROBLEMS,log_func,nmax=1000)

    print('=========\nTotal number of problems:', len(PROBLEMS), '\nAdded:', added, '\nErrors:', errors)
