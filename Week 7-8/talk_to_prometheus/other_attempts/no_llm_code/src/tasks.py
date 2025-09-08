# Tasks orchestration (teaching skeleton) - simulates CrewAI sequential flow
import agents

def run_pipeline(user_query: str, dry_run: bool = False) -> dict:
    planner = agents.PlanningAgent()
    plan = planner.make_plan(user_query)
    if dry_run:
        return { "plan": plan.dict() }
    executor = agents.ExecutorAgent()
    exec_result = executor.execute(plan)
    analyzer = agents.AnalyzerAgent(executor)
    analysis = analyzer.analyze(exec_result)
    return { "plan": plan.dict(), "exec_result": exec_result.dict(), "analysis": analysis.dict() }
