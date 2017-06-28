# -*- coding: utf-8 -*-
import requests
import bs4
import re
import json
import string
from datetime import datetime

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
                   7:{'Hold Set A 2016'},
               },
               "grid_name":{
                   "horizontal":string.ascii_uppercase[0:11],
                   "vertical":list(range(1, 19)),
               }
               }

HOLDS_CONF["grid_name"]["xy"]= [h+str(v) for v in HOLDS_CONF["grid_name"]["vertical"] for h in HOLDS_CONF["grid_name"]["horizontal"]]

def _get_hold_setup_key(setup):
    l = [k for k,v in HOLDS_CONF["setup"].items() if set(setup) == v]
    if len(l)==1:
        return l[0]
    elif len(l)>1:
        raise ValueError('Hold setup error')
    else:
        return False

def _new_problem(name, grade, holds_setup, SH, IH, FH, author, site_id = None):
    """ describe problem contents id"""
    problem = {
        "name":name,
        "grade":grade,
        "holds_setup":holds_setup,
        "holds":{"SH":SH,
                 "IH":IH,
                 "FH":FH},
        "author":author,
        "site_id":site_id,
    }
    #validate_problem()
    return problem

def _add_problem(problems, new):
    new['holds_setup_k'] = _get_hold_setup_key(new["holds_setup"])
    problems[new['site_id']] = new


def load_problems(problems_dir_path, site=False):
    if site:
        file_list = [f for f in problems_dir_path.iterdir() if f.match("site*.json")]
    else:
        file_list = [f for f in problems_dir_path.iterdir() if f.match("*.json")]
    problems={}
    setups = set()
    for file in file_list:
        try:
            print("Read problems from {}.".format(str(file)))
            file_content= json.load(open(str(file), 'r+'))
            problems_list = file_content['problems']
        except  KeyError:
            print("File not valid")
        else:
            for p in problems_list:
                _add_problem(problems,p)
    return problems

def get_setups(problems):
    setups = set()
    for k,p in problems.items():
        if p["holds_setup_k"]:
            setups.add(p["holds_setup_k"])
        else:
            setups.add(set(p["holds_setup"]))
    return setups

def problems_data(hold_setup_key, problems):
    current_hold_setup = HOLDS_CONF["setup"][hold_setup_key]
    data,data_by_hold = [],{}
    for k, v in problems.items():
        if set(v["holds_setup"]).issubset(current_hold_setup):
            d = {'id':k}
            d.update(v)
            d["holds_setup_short"] = [HOLDS_CONF["configurations"].get(name,{}).get('shortName') for name in sorted(d["holds_setup"])]
            d['favorite']=None
            data.append(d)
            for h in v['holds'].get('IH'):
                data_by_hold.setdefault(h,set([])).add(k)
            for h in v['holds'].get('FH'):
                data_by_hold.setdefault(h,set([])).add(k)
            for h in v['holds'].get('SH'):
                data_by_hold.setdefault(h,set([])).add(k)
    return data ,data_by_hold


#======================
##fetch from site
#======================

MOONBOARD_PROBLEMS_URL = "http://www.moonboard.com/problems/"

def _fetch_site_problems_ids():
    """get all problems id"""
    problems = {}
    r = requests.get(MOONBOARD_PROBLEMS_URL)
    w_soup = bs4.BeautifulSoup(r.content, 'lxml')
    problems_tags = w_soup.find_all(lambda tag: tag.name == 'div' and ('problem-id' and 'grade-val' in tag.attrs))
    for p in problems_tags:
        cl = p.get('class')
        problems[p.get('problem-id').encode('utf8')] = {#'grade_val': p.get('grade-val'),
            #'class': cl,
            'author': (" ".join(cl[4:])).strip()
        }
    return problems

def _new_site_problems_ids_and_author(current_problems={}):
    """ return new site_ids and author compared to current problem dict"""
    all_site_problems_ids = _fetch_site_problems_ids()
    current_problem_site_ids= [p['site_id'] for p in current_problems.values() if p['site_id'] is not None]
    new_site_problems_ids = set(all_site_problems_ids.keys()) - set(current_problem_site_ids)
    return {k: v for k, v in all_site_problems_ids.items() if k in new_site_problems_ids}

def _holds_from_site(site_holds):
    holds_d= {}
    for holdType in ['SH','IH','FH']:
        sortedKeys = sorted([k for k in site_holds.keys() if holdType in k])
        holds2 = [site_holds[k] for k in sortedKeys]
        holds_d[holdType] = [h for h in holds2 if h in HOLDS_CONF["grid_name"]["xy"]]
    return holds_d

def _fetch_site_problem_data(problem_id):
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
        'holds_setup': sorted([c.encode('utf8').strip() for c in s.children if c.name != 'div' and "Hold" in c]),
        'site_id':problem_id,
    }
    p_info.update(_holds_from_site(holds))

    return p_info

def fetch_and_save_new_site_problems(current_problems,save_dir_path, log_func, nmax=10):
    new_problems = []
    log_func('Fetch  new  site problems ids')

    new_problems_ids = _new_site_problems_ids_and_author(current_problems)
    n = 0
    site_id_errors = []
    i = 0
    log_func('Fetch {} site new problems data.'.format(len(new_problems_ids)))
    n_p = len(new_problems_ids)
    for k, p in new_problems_ids.items():
        try:
            p_d = _fetch_site_problem_data(k)
        except:
            site_id_errors.append(k)
        else:
            p.update(p_d)
            new_problems.append( _new_problem(**p))
            n += 1
        if n > nmax:
            log_func('Reached max iterations.')
            break
        i += 1
        log_func("{}/{}, {}%".format(n, n_p, int(n / n_p * 100)))

    # save
    now = datetime.now()
    new_file_name = "site_problems_{}.json".format(now.strftime('%Y-%m-%d_%H-%M-%S'))
    new_file = save_dir_path.joinpath(new_file_name)

    log_func(' New problems saved at {}.'.format(str(new_file)))
    d ={'date':now.isoformat(),
        'problems':new_problems,
        'report':{'errors_site_id':site_id_errors}
    }

    with open(str(new_file),'w+') as output:
        # Pickle dictionary using protocol 0.
        json.dump(d,output)
    #return info
    return new_file


##
if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Fetch problems from internet')
    parser.add_argument('--nmax',  type=int, default=1000,
                        help='maximum number of problems to fetch')

    args = parser.parse_args()
    import pathlib
    path = pathlib.Path('problems')
    current_site_problems = load_problems(path, site = True)
    print("Fetch and save new site problems")
    def log_func(s):
        print(s)
    fetch_and_save_new_site_problems(current_site_problems, path, log_func, nmax=args.nmax)