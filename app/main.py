import json
import os
from typing import Dict, List
from subprocess import call
import time
import sys

DEBUG = 0

class Job:
    job_id = 0
    def __init__(self, tag: str, exec_time: int, file_size: int):
        self.job_id = Job.job_id
        self.tag = tag
        self.exec_time = exec_time
        self.file_size = file_size

        Job.job_id += 1

    def generate_exec_file(self, path):
        out_name = job_filename(self.tag, path)
        f = open(out_name, "w")
        # TODO: entete ? -> normelement pas la peine comme "oarsub 'sh file'"
        f.write("sleep {}\n".format(self.exec_time))
        # f.write("dd if=/dev/zero of=//mnt/nfs0/file-nfs-{}-${{OAR_JOB_ID}} bs={}M count=1 oflag=direct\n".format(self.tag, self.file_size))
        f.write("dd if=/dev/zero of=/srv/shared/file-nfs-{}-${{OAR_JOB_ID}} bs={}M count=1 oflag=direct\n".format(self.tag, self.file_size))
        # TODO: the question now is: is it possible that the OAR JOB ID is the one from the top level deploy oar job ?
        f.close()

    def generate_oar_command(self, path):
        # TODO: Caution ! walltime can be smaller than exec time !
        return "/run/wrappers/bin/oarsub \"sh {}\"".format(job_filename(self.tag, path))

    def __str__(self):
        return "Job(exec: {}, file_size: {})".format(self.exec_time, self.file_size)

class Submission:
    def __init__(self, wait: int, amount: int, job_tag: str):
        self.waiting_time = wait
        self.amount = amount
        self.job_tag = job_tag

    def get_wait(self):
        return self.waiting_time

    def get_amount(self):
        return self.amount

    def get_job_tag(self):
        return self.job_tag

    def __str__(self):
        return "{}x{wait: {}, : tag: {}}".format(self.amount, self.waiting_time, self.job_tag)


class Profile:
    def __init__(self, jobs: Dict[str, Job], submissions: List[Submission]):
        self.jobs = jobs
        for j_tag in self.jobs:
            self.jobs[j_tag] = Job(j_tag, jobs[j_tag]["exec_time"], jobs[j_tag]["file_size"])
        self.submissions = [Submission(s["wait"], s["amount"], s["job_tag"]) for s in submissions]

    def generate_all_exec_files(self, path):
        for j in self.jobs.values():
            j.generate_exec_file(path)

    def run(self, path):
        last_submission_time = int(time.time())
        for submission in self.submissions:
            current_time = int(time.time())
            if current_time - last_submission_time < submission.get_wait():
                sleep_time = submission.get_wait() - (current_time - last_submission_time)
                print("sleeping for {} secs".format(sleep_time))
                if DEBUG == 0:
                    time.sleep(sleep_time)

            job = self.jobs[submission.get_job_tag()]
            oar_command = job.generate_oar_command(path)
            for _ in range(submission.get_amount()):
                if DEBUG == 0:
                    # call([oar_command])
                    os.system(oar_command)
                else:
                    print(oar_command)
            last_submission_time = current_time

    def __str__(self) -> str:
        return "Profile(jobs: {}, subs: {})".format(self.jobs, self.submissions)

    def draw(self, filename: str):
        #TODO
        pass

def job_filename(tag, path):
    return "{}/job_{}.sh".format(path, tag)


def main():
    args = sys.argv
    filename = args[1]
    if len(args) <= 2:
        path = "/tmp"
    else:
        path = args[2]

    with open(filename) as f:
        json_data = json.load(f)
        profile = Profile(json_data["jobs"], json_data["submissions"])

    profile.generate_all_exec_files(path)
    profile.run(path)

    return 0;

if __name__ == "__main__":
    main()
