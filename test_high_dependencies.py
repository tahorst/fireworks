from fireworks import LaunchPad, Firework, Workflow
from fireworks.core.rocket_launcher import rapidfire
from fireworks.examples.custom_firetasks.hello_world.hello_world_task import HelloTask

import yaml

FILENAME = ''


if __name__ == "__main__":
    # initialize the database
    with open(FILENAME) as f:
    	lp = LaunchPad(**yaml.load(f))  # you might need to modify the connection settings here
    # lp.reset()  # uncomment this line and set the appropriate parameters if you want to reset the database

    # create the workflow and store it in the database
    final_task = Firework([HelloTask()])
    other_tasks = [Firework([HelloTask()]) for i in range(500)]
    links = {task: [final_task] for task in other_tasks}
    my_wflow = Workflow([final_task] + other_tasks, links_dict=links)
    lp.add_wf(my_wflow)

    # run the workflow
    rapidfire(lp)
