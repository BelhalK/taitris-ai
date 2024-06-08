from taitriscore.actions import CreateTaskList
from taitriscore.llm import LLM
from taitriscore.logs import logger
from taitriscore.roles import Role


class Planner(Role):
    def __init__(
        self,
        objective,
        name="David",
        profile="Planner. Planning an influencer marketing campaign",
        desc="I am a lead generator for your influencers marketing campaign. My name is David. I"
        "will take your campaign objective and create a prioritized list of tasks to do so."
        " I will only reply in bullet points."
        "The tasks will always be prioritized.",
        store=None,
    ):
        self.objective = objective
        super().__init__(name, profile, desc=desc)
        self._set_store(store)

    async def task_execution_agent(self, objective, task, completed_tasks):
        completed_task_bullets = "\n".join(
            [f"  - {todo['task']}: {todo['result']}" for todo in completed_tasks]
        )
        ExecutionOutputTemplate = f"""
        Perform one task based on the following objective: {objective}.

        Take into account these previously completed tasks:
        {completed_task_bullets}

        Your task: {task}
        Response:
        """
        return ExecutionOutputTemplate

    async def task_creation_agent(
        self, objective, last_task, last_task_result, task_list
    ):
        TaskCreationTemplate = f"""
        You are to use the result from an execution agent to create new tasks with the following objective: {objective}.
        The last completed task has the result:
        {last_task_result}
        This result was based on this task description: {last_task}.

        These are {len(task_list)} incomplete tasks: {', '.join(task_list)}

        Based on the result, return a list of tasks to be completed in order to meet the objective.
        These new tasks must not overlap with incomplete tasks.
        """
        return TaskCreationTemplate

    async def task_prioritization_agent(self, objective, task_list):
        task_bullets = "\n".join([f"  - {task}" for task in task_list])
        PrioritizationOutputTemplate = f"""
        You are tasked with prioritizing the following tasks:
        {task_bullets}

        Consider the ultimate objective of your team: {objective}.
        """
        return PrioritizationOutputTemplate

    async def generate_tasks_list(self, objective):
        tasks = ["Develop a task list for your Objective."]
        completed_tasks = []

        max_rounds = 2
        for r in range(1, max_rounds + 1):
            logger.info(f"Round - {r}")
            for t in tasks:
                logger.info(f"- {t}")

            # Step 1: Pull the first incomplete task
            task = tasks.pop(0)

            # Agent complete the task based on the context
            todo = {}
            todo["task"] = task
            tmp_todo = await self.task_execution_agent(
                objective, todo, completed_tasks[-5:]
            )
            res = await self._llm.aask(tmp_todo)
            todo["result"] = res["choices"][0]["message"]["content"]

            # Step 2: Store the result in completed task
            completed_tasks.append(todo)

            # Step 3: Create new tasks re-prioritize task list
            newtodo = await self.task_creation_agent(
                objective, todo["task"], todo["result"], tasks
            )
            new_task = await self._llm.aask(newtodo)
            new_tasks = [new_task["choices"][0]["message"]["content"]]

            logger.info("Adding new tasks to task_storage")
            for t in new_tasks:
                logger.info(f"- {t}")

            # Re-prioritize tasks
            finaltodo = await self.task_prioritization_agent(
                objective, new_tasks + tasks
            )
            tasks = await self._llm.aask(finaltodo)
            tasks = tasks["choices"][0]["message"]["content"]

            logger.info(tasks)

            tasks = [tasks]
            # if not len(tasks):
            #     logger.info('Done')
            #     break
        return tasks

    def _set_store(self, store):
        action = CreateTaskList(objective=self.objective)
        self._init_actions([action])
        # self._init_actions([])
