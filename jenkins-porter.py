import argparse
import os
import requests
import os

def execute(args):
    if args.action == "copy":
        crumb = get_crumb(args.user_target, args.password_target, args.target)
        for name, config in get_all_configs(args.origin, args.user_origin, args.password_origin).items():
            read_response(create_job(args.target, name, config, args.user_target, args.password_target, crumb))
    
    elif args.action == "save":
        create_folder(args.folder)
        for name, config in get_all_configs(args.origin, args.user_origin, args.password_origin).items():
            create_config_file(args.folder, name, config)
    
    elif args.action == "restore":
        crumb = get_crumb(args.user_target, args.password_target, args.target)
        for name, config in load_all_configs(args.folder).items():
            read_response(create_job(args.target, name, config, args.user_target, args.password_target, crumb))

    elif args.action == "clean":
        crumb = get_crumb(args.user_target, args.password_target, args.target)
        for name in get_all_configs(args.target, args.user_target, args.password_target):
            read_response(delete_job(args.target, name, args.user_target, args.password_target, crumb))

    else:
        print("Wrong arguments !!!")

def read_response(response):
    if response.status_code == 200:
        print("\t\tDone !")
    else:
        print("\tResponse: {}".format(response.text))

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="Action: copy, save or restore")
    parser.add_argument("-o", "--origin", help="Jenkins Origin Server url")
    parser.add_argument("-t", "--target", help="Jenkins Target Server url")
    parser.add_argument("-uo", "--user_origin", help="Jenkins Origin Server user")
    parser.add_argument("-po", "--password_origin", help="Jenkins Origin Server password")
    parser.add_argument("-ut", "--user_target", help="Jenkins Target Server user")
    parser.add_argument("-pt", "--password_target", help="Jenkins Target Server password")
    parser.add_argument("-f", "--folder", help="Folder for saving / from restoring jobs")
    return parser.parse_args()

def welcome(origin, target):
    os.system("clear")
    print("*** Jenkins Porter will copy your jobs from {} to {} ***\n".format(origin, target))

def get_all_configs(origin, user, password):
    jobs = get_jobs(origin, user, password)
    return get_configs(origin, jobs, user, password)

def get_jobs(origin, user, password):
    print("\n* Getting all the jobs from {}\n".format(origin))
    r = requests.get("http://{}/api/json".format(origin), auth=(user, password))
    return r.json()["jobs"]

def get_configs(origin, jobs, user, password):
    print("\n*** Getting all the configurations from {} ***".format(origin))
    return {job["name"]: get_config(job["name"], job["url"], user, password) for job in jobs}

def get_config(name, url, user, password):
    print("\t- Configuration of {}".format(name))
    return requests.get("{}/config.xml".format(url), auth=(user, password)).text

def create_job(server, name, config, user, password, crumb):
    print("\t- Creating {} job in {}".format(name, server))
    [crumb_key, crumb_value] = crumb
    headers = {'Content-Type': 'application/xml', crumb_key: crumb_value}
    return requests.post("http://{}/createItem?name={}".format(server, name), data=config, auth=(user, password), headers=headers)

def create_folder(folder):
    if not os.path.exists(folder) or not os.path.isdir:
        os.makedirs(folder)

def create_config_file(folder, name, config):
    with open(os.path.join(folder, name + ".xml"), "w") as f:
        f.write(config)

def load_all_configs(folder):
    configs = {}
    for config_file in os.listdir(folder):
        name = config_file.split(".")[0]
        with open(os.path.join(folder, config_file), "r") as f:
            configs[name] = f.read()
    return configs

def get_crumb(user, password, server):
    url = 'http://{}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'.format(server)
    response = requests.get(url, auth=(user, password))
    if response.status_code == 200:
        return response.text.split(":")
    else:
        raise Exception(response.text)

def delete_job(server, name, user, password, crumb):
    print("\t- Deleting {} job in {}".format(name, server))
    [crumb_key, crumb_value] = crumb
    headers = {crumb_key: crumb_value}
    return requests.post("http://{}/job/{}/doDelete".format(server, name), data="", auth=(user, password), headers=headers)


if __name__ == "__main__":
    args = get_arguments()
    welcome(args.origin, args.target)
    execute(args)