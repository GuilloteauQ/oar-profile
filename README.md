# OAR-Profile

A python script to submit simple synthetic cluster load to OAR.

## Usage

On the node running the OAR server, run the script as:

```sh
./oar-profile <PROFILE.JSON> [PATH]
```

where

- `<PROFILE.JSON>` is the json file representing the profile of the cluster (*mandatory*)

- `[PATH]` is the path to the folder you want the script files to be store, `/tmp` by default (*optional*)


An example:

```sh
./oar-profile impulse.json $HOME
```


## Profile file

The JSON file is built as follows:

- the first part is the jobs that we will use.

    - a job is composed of an execution time and a size of file to copy to the distributed file system

    - each job has a name to differentiate them

- the second part represents the submissions.

    - it is an array of submissions

    - a submission is composed of a waiting time after the previous submission, the amount of jobs to submit and the name of the jobs to submit


An example of JSON file representing a synthetic load:

```json
{
    "jobs": {
        "heavy": {
            "exec_time": 30,
            "file_size": 100
        },
        "light": {
            "exec_time": 30,
            "file_size": 10
        }
    },
    "submissions": [
        {
            "wait": 0,
            "amount": 10,
            "job_tag": "heavy"
        },
        {
            "wait": 100,
            "amount": 100,
            "job_tag": "light"
        },
        {
            "wait": 10,
            "amount": 150,
            "job_tag": "light"
        }
    ]
}
```
