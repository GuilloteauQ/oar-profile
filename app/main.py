import json
from typing import Dict, List
from subprocess import call
import time

DEBUG = 1

class Job:
    def __init__(self, tag: str, exec_time: int, file_size: int):
        self.tag = tag
        self.exec_time = exec_time
        self.file_size = file_size

    def generate_exec_file(self):
        out_name = job_filename(self.tag)
        f = open(out_name, "w")
        # TODO: entete ?
        f.write("sleep {}\n".format(self.exec_time))
        # TODO: dd
        f.close()

    def generate_oar_command(self):
        # TODO: Caution ! walltime can be smaller than exec time !
        return "oarsub \"sh {}\"".format(job_filename(self.tag))

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

    def generate_all_exec_files(self):
        #TODO: add a path
        for j in self.jobs.values():
            j.generate_exec_file()

    def run(self):
        last_submission_time = int(time.time())
        for submission in self.submissions:
            current_time = int(time.time())
            if current_time - last_submission_time < submission.get_wait():
                sleep_time = submission.get_wait() - (current_time - last_submission_time)
                print("sleeping for {} secs".format(sleep_time))
                if DEBUG == 0:
                    time.sleep(sleep_time)

            job = self.jobs[submission.get_job_tag()]
            oar_command = job.generate_oar_command()
            for _ in range(submission.get_amount()):
                if DEBUG == 0:
                    call([oar_command])
                else:
                    print(oar_command)
            last_submission_time = current_time

    def __str__(self) -> str:
        return "Profile(jobs: {}, subs: {})".format(self.jobs, self.submissions)

def job_filename(tag):
    return "/tmp/job_{}.sh".format(tag)


def main():
    print("OAR-Profile")
    with open("./example.json") as f:
        json_data = json.load(f)
        profile = Profile(json_data["jobs"], json_data["submissions"])

    profile.generate_all_exec_files()
    profile.run()

    return 0;

if __name__ == "__main__":
    main()
